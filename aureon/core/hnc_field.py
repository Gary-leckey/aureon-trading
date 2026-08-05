"""
The canonical HNC field — one shared reading, not thirteen private ones.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The organism had ~13 independent ``LambdaEngine`` instances, each computing its own
``symbolic_life_score`` / ``coherence_gamma`` with nothing reconciling them. The HNC
live daemon (driven by real world data) now publishes the authoritative field on the
thought bus as ``symbolic.life.pulse``. This module is the single place to READ that
field, so a system that only wants "the current shared coherence" reads the one
canonical value instead of spinning a private engine — the field becomes shared
logic, not a per-module opinion.

Read path uses ``recall(topic_prefix)`` (filters by topic) so a high-volume bus
(baton.link heartbeats, etc.) can never evict the pulse from a recency window. Fully
guarded and offline-safe: with no bus / no pulse, ``read_canonical_field()`` returns
an ``available=False`` field rather than raising.

**Freshness is part of being real.** These readers cross process boundaries through
persisted trace files, and a file on disk has no idea how old it is. Without a bound,
``available=True`` meant only "a row exists somewhere", so a coherence figure written
days ago was served to a dashboard as the organism's current state — a stale number
presented as live is a false reading, not a cautious one. Every row is therefore
stamped when published and ignored once older than :data:`FIELD_MAX_AGE_S`; a row with
no timestamp has unknowable age and is refused. When nothing fresh is flowing the
readers report ``available=False``, which is the honest answer.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any


#: How old a field row may be and still count as "the current field", in seconds.
#: Tunable via ``AUREON_HNC_FIELD_MAX_AGE_S``; the default is deliberately short —
#: the HNC daemon pulses continuously, so anything older than a few minutes means the
#: producer has stopped and the honest report is "unavailable", not a stale number.
def _max_age_s() -> float:
    try:
        v = float(os.environ.get("AUREON_HNC_FIELD_MAX_AGE_S", "") or 300.0)
        return v if v > 0 else 300.0
    except (TypeError, ValueError):
        return 300.0


FIELD_MAX_AGE_S = 300.0


def _row_is_fresh(row: Any, now: float | None = None) -> bool:
    """True when ``row`` carries a timestamp within the freshness window.

    Fails CLOSED: a row with no timestamp, or an unparseable one, has unknowable age
    and is refused. Being unable to prove a reading is current is not a reason to
    present it as current.
    """
    if not isinstance(row, dict):
        return False
    ts = row.get("ts", row.get("timestamp", row.get("time")))
    if not isinstance(ts, (int, float)):
        return False
    now = time.time() if now is None else now
    age = now - float(ts)
    return -60.0 <= age <= _max_age_s()      # small negative tolerance for clock skew


@dataclass(frozen=True)
class CanonicalField:
    """A snapshot of the organism's shared HNC field."""

    available: bool = False
    symbolic_life_score: float | None = None
    coherence_gamma: float | None = None
    consciousness_psi: float | None = None
    consciousness_level: str | None = None
    lambda_t: float | None = None
    source: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "available": self.available,
            "symbolic_life_score": self.symbolic_life_score,
            "coherence_gamma": self.coherence_gamma,
            "consciousness_psi": self.consciousness_psi,
            "consciousness_level": self.consciousness_level,
            "lambda_t": self.lambda_t,
            "source": self.source,
        }


_EMPTY = CanonicalField()


def read_canonical_field(bus: Any = None) -> CanonicalField:
    """Read the latest ``symbolic.life.pulse`` — the one shared field.

    Pass ``bus`` to read from a specific ThoughtBus; otherwise the global
    singleton is used. Never raises; returns an unavailable field when there is
    no bus, no pulse, no score, and no cross-process trace.

    Cross-process bridge: the HNC live daemon, the operator, and the organism
    daemon each run as SEPARATE processes with their own in-memory bus, so a
    pulse published in one is invisible to the others. The daemon also persists
    the field to ``state/hnc_live_trace.jsonl`` every step; when the local bus
    has no pulse, we fall back to the last line of that trace so the live field
    reaches every process. Path overridable via ``AUREON_HNC_TRACE_PATH``.
    """
    try:
        from aureon.core.aureon_thought_bus import get_thought_bus, payload_of

        b = bus if bus is not None else get_thought_bus()
        if b is not None and hasattr(b, "recall"):
            pulses = b.recall("symbolic.life.pulse", limit=1) or []
            if pulses:
                p = payload_of(pulses[-1])
                sls = p.get("symbolic_life_score")
                if sls is not None:
                    return CanonicalField(
                        available=True,
                        symbolic_life_score=float(sls),
                        coherence_gamma=p.get("coherence_gamma"),
                        consciousness_psi=p.get("consciousness_psi"),
                        consciousness_level=p.get("consciousness_level"),
                        lambda_t=p.get("lambda_t"),
                        source=p.get("source"),
                    )
    except Exception:  # noqa: BLE001 — a missing field is a value, never a crash
        pass
    # Cross-process fallback: the HNC daemon's persisted trace.
    return _read_field_from_trace()


def _read_field_from_trace() -> CanonicalField:
    """Read the latest field from the HNC daemon's persisted trace file, so the
    live field crosses process boundaries (separate daemons, separate buses).
    Guarded; returns an unavailable field when the trace is absent/empty."""
    import json
    import os
    from pathlib import Path

    try:
        path = os.environ.get("AUREON_HNC_TRACE_PATH") or str(
            Path(__file__).resolve().parents[2] / "state" / "hnc_live_trace.jsonl")
        p = Path(path)
        if not p.exists():
            return _EMPTY
        last = ""
        with p.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    last = line
        if not last:
            return _EMPTY
        row = json.loads(last)
        sls = row.get("symbolic_life_score")
        if sls is None:
            return _EMPTY
        # A trace file cannot say how old it is. Without this the last line written —
        # possibly days ago, by a daemon that has since stopped — was reported as the
        # organism's live field.
        if not _row_is_fresh(row):
            return _EMPTY
        return CanonicalField(
            available=True,
            symbolic_life_score=float(sls),
            coherence_gamma=row.get("coherence_gamma"),
            consciousness_psi=row.get("consciousness_psi"),
            consciousness_level=row.get("consciousness_level"),
            lambda_t=row.get("lambda_t"),
            source="hnc_trace_file",
        )
    except Exception:  # noqa: BLE001
        return _EMPTY


def publish_subfield(source: str, state: Any, bus: Any = None) -> None:
    """Publish a producer's LOCAL field as a namespaced sub-field.

    The organism has many legitimate ``LambdaEngine`` producers (the Queen's
    cortex, source-law, metacognition, sentient loop, mycelium mind, the human
    loop). Each computes a real local field; reconciling them into one would
    destroy that. Instead each publishes its field here as
    ``symbolic.life.subfield`` so the organism can SENSE every sub-field — the
    fields become connected (visible on the shared bus) without losing their
    local computation. Guarded / no-op on any error.
    """
    payload = {
        "source": source,
        # Stamped at publish so a reader can tell a live sub-field from a dead
        # producer's last one. Rows without this are refused as unknowable-age, so
        # omitting it would silently drop the producer out of the blend.
        "ts": time.time(),
        "symbolic_life_score": getattr(state, "symbolic_life_score", None),
        "coherence_gamma": getattr(state, "coherence_gamma", None),
        "consciousness_level": getattr(state, "consciousness_level", None),
    }
    try:
        from aureon.core.aureon_thought_bus import Thought, get_thought_bus

        b = bus if bus is not None else get_thought_bus()
        if b is not None:
            b.publish(Thought(source=source, topic="symbolic.life.subfield", payload=dict(payload)))
    except Exception:  # noqa: BLE001 — visibility is best-effort, never fatal
        pass
    # Cross-process bridge: sub-field producers (Queen engines, consciousness,
    # auris) live in other processes than the blend readers (organism daemon,
    # operator SaaS). Mirror to a dedicated trace so every sub-field reaches the
    # whole-body consensus, not just same-process ones.
    try:
        from aureon.core.bus_trace import append_trace

        append_trace("symbolic_subfield", dict(payload))
    except Exception:  # noqa: BLE001
        pass


def canonical_field_reading(confidence: float = 0.9, bus: Any = None) -> Any:
    """The canonical field as a ``SubsystemReading`` — the Pattern-A merge, shared.

    Every local ``LambdaEngine`` producer (Queen cortex, source-law,
    metacognition, sentient loop, mycelium mind, human loop, Auris throne,
    pursuit, the ICS) closes its β·Λ(t−τ) loop by appending this reading to its
    own inputs before ``step()`` — the shared field informs the local one
    without replacing it. Returns ``None`` when the field is dark or stale
    (freshness fails closed upstream) — never a placeholder, because Γ consumes
    reading VALUES regardless of confidence.
    """
    try:
        from aureon.core.aureon_lambda_engine import SubsystemReading

        cf = read_canonical_field(bus)
        if cf.available and cf.symbolic_life_score is not None:
            return SubsystemReading(
                name="hnc_canonical_field",
                value=max(0.0, min(1.0, float(cf.symbolic_life_score))),
                confidence=max(0.0, min(1.0, float(confidence))),
                state=str(cf.consciousness_level or "live"),
            )
    except Exception:  # noqa: BLE001 — a missing field is a value, never a crash
        pass
    return None


def read_subfields(bus: Any = None) -> dict[str, dict[str, Any]]:
    """All recently-published local sub-fields, keyed by source — the organism's
    view of every field its producers are computing."""
    out: dict[str, dict[str, Any]] = {}

    def _absorb(src: Any, p: dict[str, Any], *, require_ts: bool) -> None:
        """Absorb one sub-field row.

        Freshness is checked per row, not per file: one live producer must not make a
        long-dead producer's last reading look current just by sharing the trace.

        ``require_ts`` differs by TRANSPORT, because what is knowable differs:

        * a **persisted trace row** carries no evidence of its own age, so an unstamped
          one is refused — that was the observed defect (75 rows, none stamped, served as
          the live field in a process with no producer running);
        * a **bus payload** arrives through ``recall(limit=…)`` on an in-memory ring
          buffer, so the bus itself bounds recency. Demanding a stamp there was stricter
          than the defect warranted and silently dropped live in-process producers out of
          the blend. A stamp is still honoured when present: a bus payload that says it
          is stale is refused.
        """
        if not src:
            return
        if require_ts:
            if not _row_is_fresh(p):
                return
        else:
            ts = p.get("ts", p.get("timestamp", p.get("time")))
            if isinstance(ts, (int, float)) and not _row_is_fresh(p):
                return
        out[str(src)] = {
            "symbolic_life_score": p.get("symbolic_life_score"),
            "coherence_gamma": p.get("coherence_gamma"),
            "consciousness_level": p.get("consciousness_level"),
        }

    # Cross-process sub-fields first (oldest), so same-process (freshest) wins on
    # collision — a producer in another process still reaches the blend.
    try:
        from aureon.core.bus_trace import read_trace

        for row in read_trace("symbolic_subfield", limit=200):
            _absorb(row.get("source"), row, require_ts=True)
    except Exception:  # noqa: BLE001
        pass
    try:
        from aureon.core.aureon_thought_bus import get_thought_bus, payload_of

        b = bus if bus is not None else get_thought_bus()
        if b is not None and hasattr(b, "recall"):
            for t in b.recall("symbolic.life.subfield", limit=200) or []:
                p = payload_of(t)
                _absorb(p.get("source"), p, require_ts=False)
    except Exception:  # noqa: BLE001
        pass
    return out


@dataclass(frozen=True)
class BlendedField:
    """A consensus across the canonical field and every local sub-field —
    the organism's whole-body view of its own coherence."""

    available: bool = False
    symbolic_life_score: float | None = None   # mean across all contributors
    coherence_gamma: float | None = None
    contributors: int = 0                       # how many fields agreed to blend
    divergence: float | None = None             # max-min spread of sub-scores
    sources: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "available": self.available,
            "symbolic_life_score": self.symbolic_life_score,
            "coherence_gamma": self.coherence_gamma,
            "contributors": self.contributors,
            "divergence": self.divergence,
            "sources": list(self.sources),
        }


def blend_field(bus: Any = None) -> BlendedField:
    """Blend the canonical field with every published sub-field into one
    consensus. The mean is the whole-body coherence; ``divergence`` (max-min
    spread) says how much the body's fields disagree — a high spread means the
    organism is of two minds and consumers should be cautious. Degrades to the
    canonical value alone when no sub-fields are present; unavailable when
    nothing is flowing. Never raises.
    """
    canonical = read_canonical_field(bus)
    subs = read_subfields(bus)

    scores: list[float] = []
    gammas: list[float] = []
    sources: list[str] = []
    if canonical.available and canonical.symbolic_life_score is not None:
        scores.append(canonical.symbolic_life_score)
        sources.append("canonical")
        if canonical.coherence_gamma is not None:
            gammas.append(canonical.coherence_gamma)
    for name, sub in sorted(subs.items()):
        sls = sub.get("symbolic_life_score")
        if sls is not None:
            try:
                scores.append(float(sls))
                sources.append(name)
                g = sub.get("coherence_gamma")
                if g is not None:
                    gammas.append(float(g))
            except (TypeError, ValueError):
                continue

    if not scores:
        return BlendedField()
    return BlendedField(
        available=True,
        symbolic_life_score=sum(scores) / len(scores),
        coherence_gamma=(sum(gammas) / len(gammas)) if gammas else None,
        contributors=len(scores),
        divergence=(max(scores) - min(scores)) if len(scores) > 1 else 0.0,
        sources=tuple(sources),
    )


def reconcile_gamma(local_coherence: float, bus: Any = None) -> float:
    """Conservatively reconcile a locally computed coherence with the canonical Γ.

    The LOWER of the two wins, so the organism's shared field can only TIGHTEN
    a live trading gate, never loosen it. Offline-safe: when the canonical
    field is unavailable (or carries no Γ) the local figure passes through
    unchanged — never a substituted or invented value. This is the one seam
    every live-order-path module uses to stay on the same field as the rest
    of the organism (b46 logic-train burn-down).
    """
    try:
        local = float(local_coherence)
    except (TypeError, ValueError):
        return local_coherence
    try:
        field = read_canonical_field(bus)
        if getattr(field, "available", False) and field.coherence_gamma is not None:
            gamma = max(0.0, min(1.0, float(field.coherence_gamma)))
            return min(local, gamma)
    except Exception:  # noqa: BLE001 — the shared field must never break a live order path
        pass
    return local


__all__ = [
    "CanonicalField", "read_canonical_field", "publish_subfield",
    "read_subfields", "BlendedField", "blend_field", "reconcile_gamma",
]
