"""
Universal Prompt Router — one door, pinned rule by rule.

Pins: classification comes from the goal-capability map and excludes the two
always-present default routes; a dark map is a NAMED blocker, never a guessed
classification; ≥2 families convenes a deterministic swarm council whose lead
family is measured (never invented); the response envelope is enforced on
every CognitionResult (sources or "general knowledge, no repo hit", conscience
verdict, trace id, honest ok/honest_unavailable/fault status); and the routing
stage is advisory — it never breaks answering.
"""

from __future__ import annotations

import pytest

from aureon.operator import prompt_router as pr
from aureon.operator.schemas import CognitionResult, GroundingContext


@pytest.fixture(autouse=True)
def _dark_field(monkeypatch, tmp_path):
    monkeypatch.setenv("AUREON_HNC_TRACE_PATH", str(tmp_path / "hnc.jsonl"))


# ── classification ────────────────────────────────────────────────────────


def test_single_family_prompt_is_not_complex():
    cap = pr.classify_prompt("write a short research summary of the HNC papers")
    assert cap["status"] == "ok"
    assert "safe_research_corpus" in cap["families"]
    assert "memory_and_state" not in cap["families"]      # defaults excluded
    assert "organism_wiring" not in cap["families"]
    assert cap["blockers"] == []


def test_multi_family_prompt_is_complex():
    cap = pr.classify_prompt(
        "research the VAT accounting treatment and plan a margin trade around it")
    fams = set(cap["families"])
    assert {"safe_trading_cognition", "safe_accounting_context",
            "safe_research_corpus"} <= fams
    assert cap["complex"] is True
    # risk labels ride through from the map, unchanged
    by_route = {r["route"]: r for r in cap["routes"]}
    assert by_route["safe_trading_cognition"]["requires_human"] is True


def test_dark_capability_map_is_a_named_blocker(monkeypatch):
    import aureon.autonomous.aureon_goal_capability_map as gcm

    def _boom(goal):
        raise RuntimeError("map dark")

    monkeypatch.setattr(gcm, "recommend_goal_routes", _boom)
    cap = pr.classify_prompt("anything")
    assert cap["status"] == "unavailable"
    assert cap["complex"] is False
    assert any("unreachable" in b for b in cap["blockers"])


# ── the routing council ───────────────────────────────────────────────────


def test_council_is_deterministic_and_lead_is_measured():
    fams = ["safe_trading_cognition", "safe_accounting_context"]
    a = pr.swarm_council("plan the trade and account for it", fams)
    b = pr.swarm_council("plan the trade and account for it", fams)
    assert a == b                                          # same prompt, same march
    assert a is not None
    assert a["lead"] in fams
    assert a["steps"] == pr.COUNCIL_STEPS
    assert set(a["clusters"]) == set(fams)                 # one cluster per family
    assert a["decisions_total"] == pr.COUNCIL_STEPS * len(fams)
    assert "deterministic" in a["boundary"]


def test_council_refuses_below_two_families():
    assert pr.swarm_council("just one thing", ["safe_research_corpus"]) is None
    assert pr.swarm_council("nothing", []) is None


def test_different_prompts_convene_different_councils():
    fams = ["safe_trading_cognition", "safe_accounting_context"]
    a = pr.swarm_council("first prompt about a trade and the accounts", fams)
    b = pr.swarm_council("a totally different question on trade accounting", fams)
    assert a is not None and b is not None
    assert a["clusters"] != b["clusters"]                  # context is the REAL prompt


# ── the enforced response envelope ────────────────────────────────────────


def _result(**kw) -> CognitionResult:
    return CognitionResult(prompt="p", **kw)


def test_status_classification_is_honest():
    assert _result(text="a real answer").status() == "ok"
    assert _result(text="[ERROR] LLM HTTP disabled by audit/offline mode").status() \
        == "honest_unavailable"
    assert _result(text="[cognition error] boom").status() == "fault"
    # a veto is the pipeline working as designed — ok, with blocked carrying it
    vetoed = _result(text="🦗 vetoed", blocked=True, conscience_verdict="VETO")
    assert vetoed.status() == "ok"
    assert vetoed.envelope()["conscience"] == {"verdict": "VETO", "blocked": True}


def test_envelope_names_sources_or_states_none():
    grounded = _result(text="answer", grounded=True, grounding=GroundingContext(
        sources=[{"title": "docs/THE_SYNTHESIS.md", "path": "docs/THE_SYNTHESIS.md"}]))
    env = grounded.envelope()
    assert env["sources"][0]["path"] == "docs/THE_SYNTHESIS.md"
    assert env["sources_statement"] == "1 repo packet(s) cited"

    bare = _result(text="general answer").envelope()
    assert bare["sources"] == []
    assert bare["sources_statement"] == "general knowledge, no repo hit"
    assert bare["capability"]["status"] == "unavailable"   # nothing classified → honest


def test_envelope_carries_council_coherence_and_rides_to_dict():
    fams = ["safe_trading_cognition", "safe_accounting_context"]
    council = pr.swarm_council("trade and account", fams)
    res = _result(text="answer",
                  capability={"status": "ok", "families": fams, "complex": True},
                  swarm=council)
    env = res.envelope()
    assert env["coherence"]["source"] == "swarm_council"
    assert env["coherence"]["lead_family"] in fams
    assert set(env["coherence"]["gamma_by_cluster"]) == set(fams)
    d = res.to_dict()
    assert d["envelope"] == env                            # every consumer sees it
    assert d["trace_id"] == env["trace_id"]


def test_operator_response_wears_the_same_envelope():
    from aureon.operator.schemas import OperatorResponse, ProviderAnswer

    ok = OperatorResponse(text="answer", answers=[ProviderAnswer(provider="p", ok=True)])
    env = ok.envelope()
    assert env["status"] == "ok"
    assert env["sources_statement"] == "general knowledge, no repo hit"
    assert ok.to_dict()["envelope"] == env

    # every line down → the switchboard is honestly unavailable, never invented
    down = OperatorResponse(text="", answers=[ProviderAnswer(provider="p", ok=False),
                                              ProviderAnswer(provider="q", ok=False)])
    assert down.status() == "honest_unavailable"


# ── wired through cognition: the one door classifies and councils ─────────


class _FlatAdapter:
    """No tools, one canned answer — keeps the loop offline and instant."""

    model = "flat"

    def prompt(self, messages, system="", tools=None, max_tokens=4096,
               temperature=0.7, **k):
        from aureon.inhouse_ai.llm_adapter import LLMResponse

        return LLMResponse(text="the answer", stop_reason="end_turn", model=self.model)

    def stream(self, *a, **k):
        from aureon.inhouse_ai.llm_adapter import StreamChunk

        yield StreamChunk(done=True)


def test_cognition_routes_every_prompt_and_councils_the_complex():
    from aureon.operator.cognition import AureonCognition

    cog = AureonCognition(adapter=_FlatAdapter(), join_mesh=False, conscience=None,
                          mesh_broadcast=False)
    res = cog.reason("research the VAT accounting rules then plan a margin trade")
    assert res.capability is not None and res.capability["complex"] is True
    assert res.swarm is not None
    assert res.swarm["lead"] in res.capability["families"]
    env = res.to_dict()["envelope"]
    assert env["status"] == "ok"
    assert env["capability"]["complex"] is True

    simple = cog.reason("how do I bake a sponge cake?")
    assert simple.capability is not None
    assert simple.capability["complex"] is False
    assert simple.swarm is None                            # no council for the simple


def test_routing_failure_never_breaks_answering(monkeypatch):
    from aureon.operator import cognition as cog_mod
    from aureon.operator.cognition import AureonCognition

    cog = AureonCognition(adapter=_FlatAdapter(), join_mesh=False, conscience=None,
                          mesh_broadcast=False)

    def _boom(prompt):
        raise RuntimeError("router down")

    monkeypatch.setattr(pr, "classify_prompt", _boom)
    res = cog.reason("research accounting and a trade")
    assert res.text == "the answer"                        # the answer still lands
    assert any(e["phase"] == "route" for e in res.errors)  # the failure is recorded
    assert cog_mod is not None
