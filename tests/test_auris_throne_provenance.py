"""
Dr Auris Throne must not report the dataclass defaults as a reading of the sky.

``CosmicState`` gives every field a plausible resting value — ``schumann_hz = 7.83``,
``schumann_coherence = 0.5``, ``cosmic_score = 0.5``, ``earth_blessing = 0.5``, ``kp_index =
0.0`` — so a state assembled with NOTHING connected looked exactly like a quiet, measured
sky. Worse, the Λ(t) step fed those defaults into the Lambda engine unconditionally and then
published the result as the ``dr_auris_throne`` sub-field, so a fabricated cosmic
contribution entered the organism's shared HNC consensus and reached the grounded-action
gate and the Queen's world sense.

The numbers still have their defaults — consumers depend on the shape — but every cycle now
records which sources actually answered, ``data_available`` is False when none did, and the
Λ(t) step is skipped rather than run on defaults.
"""

from __future__ import annotations

import pytest

pytest.importorskip("aureon.intelligence.dr_auris_throne")

from aureon.intelligence.dr_auris_throne import CosmicState, DrAurisThrone  # noqa: E402


def _throne(**sources) -> DrAurisThrone:
    """A throne with its source functions set explicitly, skipping __init__'s discovery."""
    throne = DrAurisThrone.__new__(DrAurisThrone)
    throne._space_weather_fn = sources.get("space_weather")
    throne._schumann_fn = sources.get("blessing")
    throne._schumann_reading_fn = sources.get("schumann")
    throne._earth_gate_fn = sources.get("earth_gate")
    throne._lambda_engine = sources.get("lambda_engine")
    return throne


class _Lambda:
    """Records whether it was stepped, and with what."""

    def __init__(self):
        self.steps = []

    def step(self, readings, volatility=0.0):
        self.steps.append((readings, volatility))
        return type("_S", (), {
            "lambda_t": 1.23, "consciousness_psi": 0.4,
            "coherence_gamma": 0.9, "consciousness_level": "AWARE",
            "symbolic_life_score": 0.5,
        })()


# ── the empty sky ───────────────────────────────────────────────────────────────

def test_a_state_with_no_source_is_not_available(_=None):
    state = _throne()._analyze_cosmos()
    assert state.data_available is False
    assert state.sources_live == []
    assert set(state.sources_unavailable) == {
        "space_weather", "earth_blessing", "schumann", "earth_gate"}


def test_lambda_is_not_computed_from_the_defaults(_=None):
    """The original defect: Λ(t) computed from 0.5/0.5/0.0 and published as the cosmic
    sub-field, so the shared HNC consensus absorbed a number nobody measured."""
    engine = _Lambda()
    state = _throne(lambda_engine=engine)._analyze_cosmos()
    assert engine.steps == [], "the engine must not be stepped on defaults"
    assert state.lambda_t == 0.0
    assert state.coherence_gamma == 0.0
    assert any("no planetary source" in line for line in state.reasoning)


def test_no_subfield_is_published_when_nothing_answered(monkeypatch):
    published = []
    import aureon.core.hnc_field as hnc_field

    monkeypatch.setattr(hnc_field, "publish_subfield",
                        lambda source, state, bus=None: published.append(source))
    _throne(lambda_engine=_Lambda())._analyze_cosmos()
    assert published == []


# ── a real reading ──────────────────────────────────────────────────────────────

def test_one_real_source_makes_the_state_available(_=None):
    state = _throne(blessing=lambda: (0.82, "coherent"))._analyze_cosmos()
    assert state.data_available is True
    assert state.sources_live == ["earth_blessing"]
    assert state.earth_blessing == pytest.approx(0.82)


def test_lambda_runs_once_a_real_source_answers(_=None):
    """The bound must not silence the real case — with a live source Λ(t) still computes."""
    engine = _Lambda()
    state = _throne(blessing=lambda: (0.82, "coherent"), lambda_engine=engine)._analyze_cosmos()
    assert len(engine.steps) == 1
    assert state.lambda_t == pytest.approx(1.23)
    assert state.consciousness_level == "AWARE"


def test_space_weather_readings_are_recorded_as_live(_=None):
    state = _throne(space_weather=lambda: {
        "kp_index": 6, "kp_category": "Storm", "solar_wind_speed": 620.0,
        "bz_component": -8.4, "solar_flares_24h": 2, "cosmic_score": 0.3,
    })._analyze_cosmos()
    assert "space_weather" in state.sources_live
    assert state.kp_index == 6
    assert any("Geomagnetic storm" in line for line in state.reasoning)
    assert any("substorm risk" in line for line in state.reasoning)


def test_a_source_that_raises_is_recorded_unavailable_not_live(_=None):
    def _boom():
        raise RuntimeError("NOAA unreachable")

    state = _throne(space_weather=_boom, blessing=_boom, schumann=_boom,
                    earth_gate=_boom)._analyze_cosmos()
    assert state.data_available is False
    assert set(state.sources_unavailable) == {
        "space_weather", "earth_blessing", "schumann", "earth_gate"}


def test_a_source_returning_the_wrong_shape_is_not_counted_as_live(_=None):
    state = _throne(space_weather=lambda: None, earth_gate=lambda: "open")._analyze_cosmos()
    assert "space_weather" in state.sources_unavailable
    assert "earth_gate" in state.sources_unavailable
    assert state.data_available is False


# ── what consumers see ──────────────────────────────────────────────────────────

def test_provenance_travels_in_the_published_payload(_=None):
    published = []

    class _Bus:
        def publish(self, thought):
            published.append(thought)

    throne = _throne(blessing=lambda: (0.82, "coherent"))
    throne._thought_bus = _Bus()
    throne._cycle_count = 1
    state = throne._analyze_cosmos()
    throne._publish_state(state)

    # _publish_state emits the full cosmic state and then a short advisory thought, so
    # select by topic rather than taking whichever landed last.
    states = [t for t in published if t.topic == "auris.throne.cosmic_state"]
    assert states, "the cosmic state must still reach the bus"
    payload = states[-1].payload
    assert payload["data_available"] is True
    assert payload["sources_live"] == ["earth_blessing"]
    assert "space_weather" in payload["sources_unavailable"]


def test_a_bare_cosmic_state_reports_itself_unavailable(_=None):
    """Anything constructing a CosmicState directly gets the honest answer too."""
    assert CosmicState().data_available is False
    assert CosmicState(sources_live=["schumann"]).data_available is True
