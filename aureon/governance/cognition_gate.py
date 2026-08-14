"""Fail-closed adapter between cognition and two-rune governance receipts.

This module is deliberately inert until a caller supplies two independent,
trusted receipt producers.  It never reads the ThoughtBus, the advisory prompt
router, HNC, Auris, or a provider directly, and it grants no route authority.
Its only jobs are to bind one immutable cognition proposal to exact digests,
invoke each governance voice once, and validate their dual-key join.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any, Protocol, runtime_checkable

from aureon.governance.crown_voice import (
    CROWN_SCHEMA,
    validate_crown_voice_receipt,
)
from aureon.governance.dual_key import (
    DUAL_KEY_SCHEMA,
    join_dual_key,
    validate_dual_key_receipt,
)
from aureon.swarm.auris_node_receipts import (
    DEFAULT_MAX_AGE_S,
    validate_auris_node_receipt,
)
from aureon.swarm.druidic_council import (
    FUTURE_SKEW_S,
    REQUIRED_SEATS,
    validate_council_receipt,
)

PROPOSAL_SCHEMA = "aureon.cognition_governance_proposal.v1"
DISABLED_SCHEMA = "aureon.cognition_governance_disabled.v1"
_DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")

_QUEEN_DECISION = {
    "APPROVED": "APPROVE",
    "CONCERNED": "HOLD",
    "TEACHING_MOMENT": "HOLD",
    "VETO": "ABORT",
}
_AUTHORITY_FAMILIES = frozenset({
    "office_admin_workweek",
    "safe_accounting_context",
    "safe_trading_cognition",
})
_AUTHORITY_ROUTE_KEYS = frozenset({
    "live_input_env_required",
    "live_mutation_gates",
    "manual_filing_required",
    "restart_handoff_required",
    "submit_env_required",
})
_FALSE_FLAGS = (
    "action_eligible",
    "accounting_eligible",
    "learning_eligible",
    "action_gate_passed",
    "actionable",
    "operational_eligible",
    "provider_eligible",
    "eligible_for_action",
    "eligible_for_accounting",
    "eligible_for_learning",
    "economic_mutation",
)


@dataclass(frozen=True)
class CognitionGovernanceRequest:
    """Immutable proposal material presented to each trusted voice supplier."""

    schema: str
    prompt_digest: str
    proposal_digest: str
    proposal_json: str
    provider_receipt_ids: tuple[str, ...]
    provider_moment_digest: str
    provider_source_timestamp: str
    target_provider_receipt_ids: tuple[str, ...]
    target_provider_moment_digest: str
    target_provider_source_timestamp: str
    queen_verdict: str


@dataclass(frozen=True)
class TrustedCouncilEvidence:
    """Council receipt plus the full validated Auris-node bodies it used."""

    council_receipt: Mapping[str, Any]
    auris_node_receipts: tuple[Mapping[str, Any], ...]


@runtime_checkable
class TrustedCouncilReceiptSupplier(Protocol):
    """Allowlisted composition-root adapter for the independent Council voice.

    Structural conformance is not authentication. Production must inject an
    allowlisted local adapter; request data and plugins may never choose it.
    """

    supplier_id: str

    def supply_council_evidence(
        self,
        request: CognitionGovernanceRequest,
    ) -> TrustedCouncilEvidence:
        """Return the Council receipt and all four retained node receipts."""


@runtime_checkable
class TrustedCrownReceiptSupplier(Protocol):
    """Allowlisted composition-root adapter for the independent Crown voice."""

    supplier_id: str

    def supply_crown_receipt(
        self,
        request: CognitionGovernanceRequest,
    ) -> Mapping[str, Any]:
        """Return one strict CROWN_SCHEMA receipt for this proposal."""


def _false_flags() -> dict[str, bool]:
    return dict.fromkeys(_FALSE_FLAGS, False)


def _no_data(reason: str) -> dict[str, Any]:
    """Return a numeric-free HOLD that cannot be mistaken for a receipt."""

    return {
        "schema": DUAL_KEY_SCHEMA,
        "receipt_type": "druid_queen_dual_key",
        "receipt_id": None,
        "decision": "HOLD",
        "reason": reason,
        "data_status": "no_data",
        "truth_status": "no_data",
        "freshness_status": "no_data",
        "equation_inputs_complete": False,
        "generated_values": False,
        "input_receipt_ids": [],
        "rune_voices": [],
        "lineage_alignment": "unavailable",
        "harmonic_outcome": "HOLD",
        "route_authorization_required": True,
        **_false_flags(),
    }


def _json_value(value: Any, path: str = "proposal") -> Any:
    """Normalize JSON material without inventing string representations."""

    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"{path}_must_be_finite")
        return value
    if isinstance(value, Mapping):
        normalized: dict[str, Any] = {}
        for key, nested in value.items():
            if not isinstance(key, str):
                raise ValueError(f"{path}_keys_must_be_strings")
            normalized[key] = _json_value(nested, f"{path}.{key}")
        return normalized
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [
            _json_value(nested, f"{path}[{index}]")
            for index, nested in enumerate(value)
        ]
    raise ValueError(f"{path}_must_be_json_material")


def _tool_call(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        tool = value.get("tool")
        arguments = value.get("arguments", {})
        blocked = value.get("blocked", False)
    else:
        tool = getattr(value, "tool", None)
        arguments = getattr(value, "arguments", {})
        blocked = getattr(value, "blocked", False)
    if not isinstance(tool, str) or not tool.strip():
        raise ValueError("tool_name_required")
    if not isinstance(arguments, Mapping) or type(blocked) is not bool:
        raise ValueError("valid_tool_call_required")
    return {
        "tool": tool.strip(),
        "arguments": _json_value(arguments, "tool.arguments"),
        "blocked": blocked,
    }


def _provider_moment(
    acquisition: Mapping[str, Any] | None,
) -> tuple[list[str], str, str, dict[str, Any]]:
    if not isinstance(acquisition, Mapping):
        raise ValueError("provider_moment_acquisition_required")
    raw_ids = acquisition.get("provider_receipt_ids")
    if not isinstance(raw_ids, list) or not raw_ids:
        raise ValueError("provider_receipt_ids_required")
    provider_ids = [_nonblank(value, "provider_receipt_id") for value in raw_ids]
    if provider_ids != sorted(set(provider_ids)):
        raise ValueError("provider_receipt_ids_must_be_sorted_unique")
    provider_digest = _nonblank(
        acquisition.get("provider_moment_digest"),
        "provider_moment_digest",
    )
    if _DIGEST_RE.fullmatch(provider_digest) is None:
        raise ValueError("provider_moment_digest_must_be_sha256")
    raw_source_time = acquisition.get("provider_source_timestamp")
    if raw_source_time is None:
        legacy_source_time = acquisition.get("source_timestamp")
        if (
            isinstance(legacy_source_time, bool)
            or not isinstance(legacy_source_time, (int, float))
            or not math.isfinite(float(legacy_source_time))
        ):
            raise ValueError("provider_source_timestamp_required")
        source_time = _source_timestamp_text(legacy_source_time)
    else:
        source_time = _canonical_decimal_text(raw_source_time)
    normalized = dict(_json_value(dict(acquisition), "acquisition"))
    normalized.pop("source_timestamp", None)
    normalized["provider_receipt_ids"] = provider_ids
    normalized["provider_moment_digest"] = provider_digest
    normalized["provider_source_timestamp"] = source_time
    return provider_ids, provider_digest, source_time, normalized


def _governance_provider_moments(
    acquisition: Mapping[str, Any] | None,
) -> tuple[
    list[str],
    str,
    str,
    list[str],
    str,
    str,
    dict[str, Any],
]:
    """Separate the field moment which seats voices from the route target moment.

    Existing cognition proposals carry one provider moment and therefore use it
    for both roles. Economic proposals may additionally carry an explicit
    ``field_provider_*`` triple. The ordinary ``provider_*`` triple always
    remains the target acquisition and is hash-bound in the proposal.
    """

    target_ids, target_digest, target_time, normalized = _provider_moment(acquisition)
    assert isinstance(acquisition, Mapping)
    field_names = (
        "field_provider_receipt_ids",
        "field_provider_moment_digest",
        "field_provider_source_timestamp",
    )
    field_presence = tuple(name in acquisition for name in field_names)
    if any(field_presence) and not all(field_presence):
        raise ValueError("complete_field_provider_moment_required")
    if not any(field_presence):
        return (
            target_ids,
            target_digest,
            target_time,
            target_ids,
            target_digest,
            target_time,
            normalized,
        )
    field_acquisition = {
        "provider_receipt_ids": acquisition["field_provider_receipt_ids"],
        "provider_moment_digest": acquisition["field_provider_moment_digest"],
        "provider_source_timestamp": acquisition["field_provider_source_timestamp"],
    }
    field_ids, field_digest, field_time, _ = _provider_moment(field_acquisition)
    normalized["field_provider_receipt_ids"] = field_ids
    normalized["field_provider_moment_digest"] = field_digest
    normalized["field_provider_source_timestamp"] = field_time
    return (
        field_ids,
        field_digest,
        field_time,
        target_ids,
        target_digest,
        target_time,
        normalized,
    )


def _canonical_decimal_text(value: Any) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError("provider_source_timestamp_must_be_canonical_decimal_text")
    if "e" in value.lower() or value.startswith("+"):
        raise ValueError("provider_source_timestamp_must_be_canonical_decimal_text")
    try:
        number = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(
            "provider_source_timestamp_must_be_canonical_decimal_text"
        ) from exc
    if not number.is_finite():
        raise ValueError("provider_source_timestamp_must_be_finite")
    canonical = format(number, "f")
    if "." in canonical:
        canonical = canonical.rstrip("0").rstrip(".")
    if Decimal(canonical) == 0:
        canonical = "0"
    if value != canonical:
        raise ValueError("provider_source_timestamp_must_be_canonical_decimal_text")
    return canonical


def _source_timestamp_text(value: Any) -> str:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("source_timestamp_must_be_finite")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("source_timestamp_must_be_finite")
    canonical = format(Decimal(str(number)), "f")
    if "." in canonical:
        canonical = canonical.rstrip("0").rstrip(".")
    if Decimal(canonical) == 0:
        canonical = "0"
    return _canonical_decimal_text(canonical)


def build_cognition_governance_request(
    *,
    prompt: str,
    answer: str,
    tool_calls: Sequence[Any] = (),
    capability: Mapping[str, Any] | None = None,
    bake: Mapping[str, Any] | None = None,
    acquisition: Mapping[str, Any] | None = None,
    queen_verdict: str,
) -> CognitionGovernanceRequest:
    """Bind the exact proposed answer and measured turn ledger to SHA-256."""

    if not isinstance(prompt, str) or not isinstance(answer, str):
        raise ValueError("prompt_and_answer_must_be_text")
    verdict = str(queen_verdict or "").strip().upper()
    if verdict not in _QUEEN_DECISION:
        raise ValueError("recognized_queen_verdict_required")
    (
        field_provider_ids,
        field_provider_digest,
        field_source_time,
        target_provider_ids,
        target_provider_digest,
        target_source_time,
        normalized_acquisition,
    ) = _governance_provider_moments(acquisition)
    proposal = {
        "schema": PROPOSAL_SCHEMA,
        "prompt": prompt,
        "answer": answer,
        "tool_calls": [_tool_call(item) for item in tool_calls],
        "capability": _json_value(dict(capability or {}), "capability"),
        "bake": _json_value(dict(bake or {}), "bake"),
        "acquisition": normalized_acquisition,
    }
    canonical = json.dumps(
        proposal,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    return CognitionGovernanceRequest(
        schema=PROPOSAL_SCHEMA,
        prompt_digest=hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        proposal_digest=hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        proposal_json=canonical,
        provider_receipt_ids=tuple(field_provider_ids),
        provider_moment_digest=field_provider_digest,
        provider_source_timestamp=field_source_time,
        target_provider_receipt_ids=tuple(target_provider_ids),
        target_provider_moment_digest=target_provider_digest,
        target_provider_source_timestamp=target_source_time,
        queen_verdict=verdict,
    )


def _nonblank(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value.strip()


def _validated_council_evidence(
    supplier: TrustedCouncilReceiptSupplier,
    evidence: Any,
    *,
    now: float,
    max_age_s: float,
) -> tuple[dict[str, Any], list[str], str, float, str]:
    if not isinstance(evidence, TrustedCouncilEvidence):
        raise ValueError("trusted_council_evidence_required")
    supplier_id = _nonblank(supplier.supplier_id, "council_supplier_id")
    council = validate_council_receipt(
        evidence.council_receipt,
        now=now,
        max_age_s=max_age_s,
    )
    raw_nodes = evidence.auris_node_receipts
    if not isinstance(raw_nodes, tuple) or len(raw_nodes) != len(REQUIRED_SEATS):
        raise ValueError("four_retained_auris_node_receipts_required")
    nodes = [
        validate_auris_node_receipt(node, now=now, max_age_s=max_age_s)
        for node in raw_nodes
    ]
    if [node["seat"] for node in nodes] != list(REQUIRED_SEATS):
        raise ValueError("stable_auris_node_order_required")
    if len({node["receipt_id"] for node in nodes}) != len(REQUIRED_SEATS):
        raise ValueError("distinct_auris_node_receipts_required")
    if {node["resolver_id"] for node in nodes} != {supplier_id}:
        raise ValueError("council_supplier_resolver_binding_required")
    provider_id_sets = {
        tuple(node["provider_receipt_ids"])
        for node in nodes
    }
    provider_digests = {node["provider_moment_digest"] for node in nodes}
    if len(provider_id_sets) != 1 or len(provider_digests) != 1:
        raise ValueError("one_exact_node_provider_moment_required")
    for summary, node in zip(council["seat_summaries"], nodes, strict=True):
        if (
            summary["seat"] != node["seat"]
            or summary["agent_id"] != node["agent_id"]
            or summary["gamma"] != node["gamma"]
            or summary["auris_node_receipt_id"] != node["receipt_id"]
            or node["hnc_receipt_id"] != council["hnc_receipt_id"]
            or node["auris_receipt_id"] != council["auris_receipt_id"]
            or node["source_timestamp"] != council["source_timestamp"]
        ):
            raise ValueError("council_seat_must_bind_full_auris_node_receipt")
    return (
        council,
        list(next(iter(provider_id_sets))),
        next(iter(provider_digests)),
        float(council["source_timestamp"]),
        supplier_id,
    )


def _validated_crown_evidence(
    supplier: TrustedCrownReceiptSupplier,
    request: CognitionGovernanceRequest,
    *,
    now: float,
    max_age_s: float,
) -> tuple[dict[str, Any], str]:
    supplier_id = _nonblank(supplier.supplier_id, "crown_supplier_id")
    raw_crown = supplier.supply_crown_receipt(request)
    if not isinstance(raw_crown, Mapping) or raw_crown.get("schema") != CROWN_SCHEMA:
        raise ValueError("strict_crown_voice_receipt_required")
    crown = validate_crown_voice_receipt(
        raw_crown,
        now=now,
        max_age_s=max_age_s,
    )
    if crown.get("resolver_id") != supplier_id:
        raise ValueError("crown_supplier_resolver_binding_required")
    return crown, supplier_id


def evaluate_cognition_governance(
    *,
    prompt: str,
    answer: str,
    queen_verdict: str,
    queen_evaluated: bool,
    council_receipt_supplier: TrustedCouncilReceiptSupplier | None,
    crown_receipt_supplier: TrustedCrownReceiptSupplier | None,
    tool_calls: Sequence[Any] = (),
    capability: Mapping[str, Any] | None = None,
    bake: Mapping[str, Any] | None = None,
    acquisition: Mapping[str, Any] | None = None,
    now: float | None = None,
    max_age_s: float = DEFAULT_MAX_AGE_S,
) -> dict[str, Any]:
    """Invoke two trusted voices once and validate their exact harmonic join.

    Any missing dependency, invalid proposal material, supplier failure, Queen
    mismatch, stale receipt, or lineage mismatch becomes numeric-free no-data.
    The returned receipt remains evidence-only even when its decision is ACCEPT.
    """

    if queen_evaluated is not True:
        return _no_data("evaluated_queen_voice_required")
    if (
        not isinstance(council_receipt_supplier, TrustedCouncilReceiptSupplier)
        or not isinstance(crown_receipt_supplier, TrustedCrownReceiptSupplier)
    ):
        return _no_data("independent_council_and_crown_suppliers_required")
    if council_receipt_supplier is crown_receipt_supplier:
        return _no_data("independent_council_and_crown_suppliers_required")
    try:
        request = build_cognition_governance_request(
            prompt=prompt,
            answer=answer,
            tool_calls=tool_calls,
            capability=capability,
            bake=bake,
            acquisition=acquisition,
            queen_verdict=queen_verdict,
        )
        expected_crown_decision = _QUEEN_DECISION[request.queen_verdict]
        current = time.time() if now is None else now
        age_limit = Decimal(str(max_age_s))
        current_decimal = Decimal(str(current))
        request_source_times = (
            Decimal(request.provider_source_timestamp),
            Decimal(request.target_provider_source_timestamp),
        )
        if (
            not math.isfinite(float(current))
            or not age_limit.is_finite()
            or age_limit <= 0
            or any(
                source_time > current_decimal + Decimal(str(FUTURE_SKEW_S))
                or current_decimal - source_time > age_limit
                for source_time in request_source_times
            )
        ):
            raise ValueError("fresh_request_provider_moment_required")
        council_bundle = council_receipt_supplier.supply_council_evidence(
            request,
        )
        (
            council,
            provider_ids,
            provider_digest,
            provider_source_time,
            council_supplier_id,
        ) = _validated_council_evidence(
            council_receipt_supplier,
            council_bundle,
            now=current,
            max_age_s=max_age_s,
        )
        if (
            tuple(provider_ids) != request.provider_receipt_ids
            or provider_digest != request.provider_moment_digest
            or _source_timestamp_text(provider_source_time)
            != request.provider_source_timestamp
        ):
            raise ValueError("council_provider_moment_must_match_request_acquisition")
        crown, crown_supplier_id = _validated_crown_evidence(
            crown_receipt_supplier,
            request,
            now=current,
            max_age_s=max_age_s,
        )
        if council_supplier_id.casefold() == crown_supplier_id.casefold():
            raise ValueError("independent_council_and_crown_suppliers_required")
        if (
            crown.get("decision") != expected_crown_decision
            or crown.get("queen_verdict") != request.queen_verdict
            or crown.get("queen_evaluated") is not True
        ):
            raise ValueError("crown_receipt_must_match_evaluated_queen")
        if (
            crown.get("provider_receipt_ids") != provider_ids
            or crown.get("provider_moment_digest") != provider_digest
            or _source_timestamp_text(crown.get("source_timestamp"))
            != request.provider_source_timestamp
        ):
            raise ValueError("council_and_crown_provider_moment_mismatch")
        council_identities = {
            council_supplier_id.casefold(),
            *(
                str(item["agent_id"]).strip().casefold()
                for item in council["seat_summaries"]
            ),
        }
        crown_identities = {
            str(crown[field]).strip().casefold()
            for field in (
                "resolver_id",
                "issuer_id",
                "crown_identity",
                "verdict_source_id",
            )
        }
        if council_identities.intersection(crown_identities):
            raise ValueError("council_and_crown_identity_must_be_independent")
        joined = join_dual_key(
            council,
            crown,
            now=current,
            max_age_s=max_age_s,
        )
        if joined.get("receipt_id") is None:
            return _no_data(str(joined.get("reason") or "dual_key_join_failed"))
        validated = validate_dual_key_receipt(
            joined,
            now=current,
            max_age_s=max_age_s,
        )
        if (
            validated["prompt_digest"] != request.prompt_digest
            or validated["proposal_digest"] != request.proposal_digest
            or tuple(validated["provider_receipt_ids"])
            != request.provider_receipt_ids
            or validated["provider_moment_digest"]
            != request.provider_moment_digest
            or validated["provider_source_timestamp"]
            != request.provider_source_timestamp
            or _source_timestamp_text(validated["source_timestamp"])
            != request.provider_source_timestamp
        ):
            raise ValueError("runtime_proposal_lineage_mismatch")
        return validated
    except (AttributeError, KeyError, TypeError, ValueError):
        return _no_data("complete_fresh_runtime_bound_two_rune_receipts_required")
    except Exception:
        return _no_data("governance_supplier_unavailable")


def authority_route_requires_governance(
    capability: Mapping[str, Any] | None,
) -> bool:
    """Conservatively identify routes that may not use compatibility mode."""

    if not isinstance(capability, Mapping) or capability.get("status") != "ok":
        return True
    families = capability.get("families")
    routes = capability.get("routes")
    if not isinstance(families, list) or not isinstance(routes, list):
        return True
    if any(str(value) in _AUTHORITY_FAMILIES for value in families):
        return True
    for route in routes:
        if not isinstance(route, Mapping):
            return True
        if route.get("requires_human") is True:
            return True
        if str(route.get("risk") or "").strip().lower() == "high":
            return True
        if any(route.get(key) not in (None, False, "", []) for key in _AUTHORITY_ROUTE_KEYS):
            return True
    return False


def explicit_disabled_governance(
    capability: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Describe an explicit compatibility opt-out without granting authority."""

    if authority_route_requires_governance(capability):
        return _no_data("governance_cannot_be_disabled_for_authority_route")
    return {
        "schema": DISABLED_SCHEMA,
        "receipt_type": "cognition_governance_disabled",
        "receipt_id": None,
        "decision": "DISABLED",
        "reason": "explicit_non_authority_compatibility_mode",
        "data_status": "disabled",
        "truth_status": "configuration",
        "freshness_status": "not_applicable",
        "equation_inputs_complete": False,
        "generated_values": False,
        "input_receipt_ids": [],
        "route_authorization_required": True,
        **_false_flags(),
    }


__all__ = [
    "CognitionGovernanceRequest",
    "DISABLED_SCHEMA",
    "PROPOSAL_SCHEMA",
    "TrustedCouncilEvidence",
    "TrustedCouncilReceiptSupplier",
    "TrustedCrownReceiptSupplier",
    "authority_route_requires_governance",
    "build_cognition_governance_request",
    "evaluate_cognition_governance",
    "explicit_disabled_governance",
]
