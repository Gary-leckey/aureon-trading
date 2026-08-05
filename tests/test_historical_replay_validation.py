"""The HNC + Auris stack fires on REAL open historical data — no API keys.

Replays the bundled provenance-stamped Kraken public OHLC datasets (real
exchange history) through the real components and pins the calibration
verdicts: signals observed, capital preserved in downtrends, honest
blockers when a dataset is missing, deterministic artifacts.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from aureon.analytics.historical_replay_validation import (
    DATA_DIR,
    SYMBOLS,
    compute_replay_validation,
    load_ohlc,
    replay_symbol,
)

_HAVE_DATA = all((DATA_DIR / f"kraken_ohlc_{s}_60m.json").exists() for s in SYMBOLS)

pytestmark = pytest.mark.skipif(
    not _HAVE_DATA,
    reason="bundled open datasets missing — refetch with "
           "`python -m aureon.analytics.historical_replay_validation --refresh`",
)


def test_datasets_are_real_and_provenance_stamped():
    for sym in SYMBOLS:
        payload = load_ohlc(sym)
        assert payload is not None
        prov = payload["provenance"]
        assert "Kraken public" in prov["source"]
        assert "not synthetic" in prov["kind"]
        assert len(payload["candles"]) >= 500, "a real month of hourly candles"


def test_replay_produces_real_hnc_and_auris_observables():
    payload = load_ohlc("BTCUSD")
    r = replay_symbol(payload)
    # the Auris nodes actually moved on the real data — not a constant
    assert r.auris_coherence_max > r.auris_coherence_min
    assert 0.0 < r.auris_coherence_mean < 1.0
    # the field computed a real Γ and the observer classified the timeline
    assert 0.0 < r.gamma_mean < 1.0
    assert sum(r.observer_regime_counts.values()) == r.candles
    assert r.vol_assessments_ok > 0, "the sentinel measured real expansion risk"
    # fee-inclusive accounting is self-consistent
    assert r.fees_paid_pct == pytest.approx(
        r.n_position_changes * 0.26, abs=1e-6)


def test_validation_verdicts_on_bundled_data():
    report = compute_replay_validation()
    assert not report.blockers
    assert report.total_candles >= 1500
    assert report.any_symbol_produced_signals, (
        "the stack must fire at least one entry signal on this real month"
    )
    assert report.capital_preserved_in_downtrends, (
        "the gated strategy must never draw down MORE than buy-and-hold"
    )
    for s in report.symbols:
        assert s["max_drawdown_pct"] <= s["buy_hold_max_drawdown_pct"] + 1e-9


def test_missing_dataset_is_a_named_blocker(tmp_path):
    report = compute_replay_validation(data_dir=tmp_path)
    assert len(report.blockers) == len(SYMBOLS)
    assert all("refetch" in b for b in report.blockers)
    assert report.symbols == []
    assert report.any_symbol_produced_signals is False


def test_replay_is_deterministic():
    payload = load_ohlc("SOLUSD")
    assert replay_symbol(payload).to_dict() == replay_symbol(payload).to_dict()


def test_corrupt_dataset_refused(tmp_path):
    bad = tmp_path / "kraken_ohlc_BTCUSD_60m.json"
    bad.write_text("{not json", encoding="utf-8")
    assert load_ohlc("BTCUSD", data_dir=tmp_path) is None


def test_artifact_written_by_cli_matches_module(tmp_path):
    from aureon.analytics.historical_replay_validation import write_replay_report

    report = compute_replay_validation()
    out = write_replay_report(report, tmp_path / "replay.json")
    loaded = json.loads(Path(out.out_path).read_text(encoding="utf-8"))
    assert loaded["any_symbol_produced_signals"] == report.any_symbol_produced_signals
    assert loaded["boundary"] == report.boundary
