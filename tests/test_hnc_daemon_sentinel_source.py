"""P3 daemon-source contract: max_age honesty expiry + bit-identity for unset sources.

``SourceState.max_age_s`` exists because the daemon's cached ``last_reading``
otherwise never expires — a dark sentinel's last risk figure would linger in
Γ forever, a stale number presented as live. The expiry is OPT-IN: every
pre-existing source registers with the default (None) and must behave
bit-identically to the never-expires original.

Also covers the two P3 mappers' honesty edges (no_data / WARMING → None) —
the fetcher side of the "Γ consumes values, not confidences" rule.
"""

from __future__ import annotations

import time
from types import SimpleNamespace

import pytest

from aureon.core.aureon_lambda_engine import SubsystemReading
from aureon.core.hnc_live_daemon import (
    HNCLiveDaemon,
    SourceState,
    _map_harmonic_observer,
    _map_volatility_sentinel,
)

# ── SourceState.reading_for_compute ─────────────────────────────────────────


def _reading(name: str = "x", value: float = 0.6) -> SubsystemReading:
    return SubsystemReading(name=name, value=value, confidence=0.8, state="test")


def test_fresh_reading_is_served_within_max_age():
    st = SourceState(name="volatility_sentinel", interval_s=5, max_age_s=120.0)
    st.last_reading = _reading()
    st.last_fetch_ts = t0 = time.time()
    assert st.reading_for_compute(t0 + 60.0) is st.last_reading


def test_expired_reading_is_dropped_from_compute():
    st = SourceState(name="volatility_sentinel", interval_s=5, max_age_s=120.0)
    st.last_reading = _reading()
    st.last_fetch_ts = t0 = time.time()
    assert st.reading_for_compute(t0 + 120.1) is None, (
        "a reading older than max_age_s must leave Γ, not linger"
    )


def test_unset_max_age_is_bit_identical_never_expires():
    """The default (None) preserves the original behaviour exactly: a reading
    survives arbitrarily long — the pre-existing 11 sources are untouched."""
    st = SourceState(name="schumann", interval_s=600)
    assert st.max_age_s is None
    st.last_reading = _reading("schumann")
    st.last_fetch_ts = t0 = time.time()
    ten_years = 10 * 365 * 24 * 3600.0
    assert st.reading_for_compute(t0 + ten_years) is st.last_reading


def test_no_reading_yet_is_none_either_way():
    assert SourceState(name="a", interval_s=5).reading_for_compute(time.time()) is None
    assert SourceState(name="b", interval_s=5, max_age_s=60.0).reading_for_compute(
        time.time()) is None


# ── register_source plumbs max_age_s through ────────────────────────────────


def _bare_daemon() -> HNCLiveDaemon:
    """A daemon shell with ONLY the registration plumbing — no default-source
    wiring, no bridges, no observer, no network."""
    d = object.__new__(HNCLiveDaemon)
    d._sources = {}
    d._fetchers = {}
    return d


def test_register_source_default_is_none():
    d = _bare_daemon()

    async def fetch():
        return None

    d.register_source("custom", 30, fetch)
    assert d._sources["custom"].max_age_s is None
    assert d._sources["custom"].interval_s == 30


def test_register_source_stores_max_age():
    d = _bare_daemon()

    async def fetch():
        return None

    d.register_source("volatility_sentinel", 5, fetch, max_age_s=120.0)
    st = d._sources["volatility_sentinel"]
    assert st.max_age_s == pytest.approx(120.0)


# ── mapper honesty edges ────────────────────────────────────────────────────


def test_map_volatility_sentinel_refuses_riskless_ok_row():
    """Even a status=ok object with a None risk maps to None — the value is
    what enters Γ, and there is no value."""
    a = SimpleNamespace(status="ok", volatility_risk=None, confidence=0.5, factors=())
    assert _map_volatility_sentinel(a) is None


def test_map_harmonic_observer_warming_is_none():
    obs = SimpleNamespace(regime=lambda: "WARMING", coherence_score=lambda: 0.0)
    assert _map_harmonic_observer(obs) is None
    assert _map_harmonic_observer(None) is None


def test_map_harmonic_observer_caps_confidence():
    """The FFT-of-Λ loop is self-referential: it informs the field, it must
    never dominate it — confidence is pinned at 0.6."""
    obs = SimpleNamespace(regime=lambda: "QUIET", coherence_score=lambda: 0.83)
    r = _map_harmonic_observer(obs)
    assert r is not None
    assert r.name == "harmonic_spectrum"
    assert r.value == pytest.approx(0.83)
    assert r.confidence == pytest.approx(0.6)
    assert r.state == "QUIET"
