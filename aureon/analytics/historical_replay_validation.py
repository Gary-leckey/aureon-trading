#!/usr/bin/env python3
"""Historical replay validation — the HNC + Auris stack on REAL open data, no API keys.

Proof-of-life for the whole P1–P5 chain: load an OPEN historical dataset
(Kraken's public unauthenticated OHLC endpoint — real exchange market data,
provenance stamped in the file), replay it chronologically through the REAL
production components, watch the signals fire on the historical timeline,
benchmark the calibration, and report the revenue metrics those signals
would have produced. When the calibration reads correct here, the switch to
live is configuration, not code: the very same sentinel/daemon/gates consume
the ws_cache live exchange feeds (P3 wiring) instead of this file.

What replays (the real components, not mocks)
---------------------------------------------
* ``VolatilitySentinel`` — EWMA expansion risk per close (P2), the veto line
  at ``VOL_RISK_BLOCK`` (P4).
* ``AurisEngine`` — the 9 Auris nodes' coherence per candle (P5-reconciled;
  with no live field flowing during replay the node blend passes through,
  honestly).
* ``MultiExchangeOrchestrator._calculate_coherence`` — the probability-matrix
  coherence with the P4 structure-fixed energy term (churn no longer scores).
* ``LambdaEngine`` — Λ(t), Γ, ψ stepped from the measured readings.
* ``HarmonicObserver`` — the FFT-of-Λ(t) timeline regime (P3).

Revenue metrics (measured on the same real series, fees included)
-----------------------------------------------------------------
A deterministic long/flat walk: decide at each close, hold to the next.
LONG when the probability coherence is above its own sigmoid midline,
momentum is positive, and the sentinel is NOT vetoing; flat otherwise.
Kraken taker fee charged on every position change. Reported against
buy-and-hold AND against the same strategy WITHOUT the sentinel veto, so the
veto's contribution is isolated and measured, never asserted.

Honesty
-------
The dataset is REAL exchange history (never synthetic here); a missing file
is a named blocker; the veto contribution can legitimately be ~0 in a calm
month and is reported as measured. Deterministic: same dataset in, byte-same
artifact out.
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

__all__ = [
    "REPLAY_BOUNDARY",
    "TAKER_FEE_RATE",
    "DATA_DIR",
    "SYMBOLS",
    "load_ohlc",
    "replay_symbol",
    "compute_replay_validation",
    "write_replay_report",
    "main",
]

REPLAY_BOUNDARY = (
    "Historical replay of REAL open exchange data (Kraken public OHLC, no API key) through the real "
    "HNC/Auris/sentinel components. It measures signals, calibration, and fee-inclusive revenue on the "
    "recorded timeline; it fabricates no prices, arms no live orders, and is NOT a claim about any person."
)

#: Kraken spot taker fee (base tier) — charged per position change.
TAKER_FEE_RATE = 0.0026

_REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = _REPO_ROOT / "data" / "historical"
SYMBOLS = ("BTCUSD", "ETHUSD", "SOLUSD")


@dataclass(frozen=True)
class SymbolReplay:
    """Everything measured while one symbol's history flowed through the stack."""

    symbol: str
    candles: int
    provenance: dict[str, Any]
    # HNC / Auris observables on the real timeline
    auris_coherence_mean: float
    auris_coherence_min: float
    auris_coherence_max: float
    gamma_mean: float
    lambda_final: float
    observer_regime_counts: dict[str, int]
    vol_risk_max: float
    vol_assessments_ok: int
    # signals on the historical timeline
    long_candles: int
    entry_signals: int
    veto_candles: int
    veto_windows: int
    veto_high_vol_precision: float | None
    # fee-inclusive revenue metrics
    strategy_return_pct: float
    strategy_no_veto_return_pct: float
    buy_hold_return_pct: float
    veto_contribution_pct: float
    max_drawdown_pct: float
    buy_hold_max_drawdown_pct: float
    n_position_changes: int
    fees_paid_pct: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReplayValidationReport:
    """The consolidated no-keys proof: HNC + Auris firing on real history."""

    symbols: list[dict[str, Any]]
    total_candles: int
    any_symbol_produced_signals: bool
    capital_preserved_in_downtrends: bool
    any_veto_fired: bool
    switch_to_live_note: str
    boundary: str = REPLAY_BOUNDARY
    blockers: list[str] = field(default_factory=list)
    out_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_ohlc(symbol: str, data_dir: Path | None = None) -> dict[str, Any] | None:
    """Load one symbol's provenance-stamped real dataset. Missing → None."""
    path = (data_dir or DATA_DIR) / f"kraken_ohlc_{symbol}_60m.json"
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 — a corrupt dataset is a blocker, never fabricated
        return None
    if not payload.get("candles"):
        return None
    return payload


def _equity_walk(closes: list[float], positions: list[int]) -> tuple[float, float, int, float]:
    """Fee-inclusive long/flat equity walk. ``positions[i]`` is held over the
    move closes[i] → closes[i+1]. Returns (return_pct, max_drawdown_pct,
    n_position_changes, fees_paid_pct)."""
    equity = 1.0
    peak = 1.0
    max_dd = 0.0
    changes = 0
    fees = 0.0
    prev_pos = 0
    for i, pos in enumerate(positions):
        if pos != prev_pos:
            equity *= (1.0 - TAKER_FEE_RATE)
            fees += TAKER_FEE_RATE
            changes += 1
            prev_pos = pos
        if pos and closes[i] > 0:
            equity *= closes[i + 1] / closes[i]
        peak = max(peak, equity)
        max_dd = max(max_dd, (peak - equity) / peak)
    if prev_pos:  # close the final position at the last price
        equity *= (1.0 - TAKER_FEE_RATE)
        fees += TAKER_FEE_RATE
        changes += 1
    return ((equity - 1.0) * 100.0, max_dd * 100.0, changes, fees * 100.0)


def replay_symbol(payload: dict[str, Any]) -> SymbolReplay:
    """Run one symbol's real history through the real components, chronologically."""
    from aureon.core.aureon_lambda_engine import LambdaEngine, SubsystemReading
    from aureon.intelligence.volatility_sentinel import (
        VOL_RISK_BLOCK,
        VolatilitySentinel,
    )
    from aureon.observer.harmonic_observer import HarmonicObserver
    from aureon.trading.aureon_auris_trader import AurisEngine, MarketSnapshot
    from aureon.trading.aureon_unified_ecosystem import MultiExchangeOrchestrator

    symbol = str(payload.get("symbol", "?"))
    candles = payload["candles"]
    closes = [float(c["close"]) for c in candles]

    sentinel = VolatilitySentinel(symbols=[symbol])
    auris = AurisEngine()
    engine = LambdaEngine()
    engine._state_path = Path("/dev/null")  # replay must not touch live state
    observer = HarmonicObserver(publish_to_bus=False, trace_interval_s=3600.0)
    prob_host = object.__new__(MultiExchangeOrchestrator)

    auris_scores: list[float] = []
    gammas: list[float] = []
    regimes: dict[str, int] = {}
    vol_risk_max = 0.0
    vol_ok = 0
    lambda_final = 0.0

    positions: list[int] = []          # with sentinel veto
    positions_no_veto: list[int] = []  # same gates minus the veto
    veto_flags: list[bool] = []
    entry_signals = 0
    prev_long = False

    for i, c in enumerate(candles):
        ts = float(c["ts"])
        close = float(c["close"])
        change_pct = ((close - closes[i - 1]) / closes[i - 1] * 100.0) if i else 0.0

        # The coherence formulas' production contract is the 24h TICKER
        # (change24h, 24h high/low, 24h quote volume) — feed them the same
        # quantities computed over the trailing 24 real candles, exactly what
        # the live exchanges' 24hr endpoints report.
        w = candles[max(0, i - 23):i + 1]
        high_24h = max(float(x["high"]) for x in w)
        low_24h = min(float(x["low"]) for x in w)
        open_24h = float(w[0]["open"])
        change_24h = ((close - open_24h) / open_24h * 100.0) if open_24h > 0 else 0.0
        range_24h_pct = ((high_24h - low_24h) / low_24h * 100.0) if low_24h > 0 else 0.0
        quote_volume_24h = sum(float(x["volume"]) * float(x["close"]) for x in w)

        # 1. Volatility sentinel — predicted expansion risk (P2/P4)
        sentinel.ingest_price(symbol, close, ts=ts)
        assessment = sentinel.assess(symbol)
        risk = None
        if assessment.status == "ok" and assessment.volatility_risk is not None:
            risk = float(assessment.volatility_risk)
            vol_risk_max = max(vol_risk_max, risk)
            vol_ok += 1
        vetoed = risk is not None and risk >= VOL_RISK_BLOCK
        veto_flags.append(vetoed)

        # 2. Auris 9-node coherence on the real candle (P5) — the trader's own
        # normalization scheme, fed 24h ticker stats as in production.
        snap = MarketSnapshot(
            symbol=symbol, price=close,
            volume=min(1.0, quote_volume_24h / 10_000_000.0),
            volatility=min(1.0, range_24h_pct / 25.0),
            momentum=max(-1.0, min(1.0, change_24h / 15.0)),
            spread=min(1.0, range_24h_pct / 2.0),
            timestamp=ts,
        )
        auris_coh = float(auris.calculate_coherence(snap))
        auris_scores.append(auris_coh)

        # 3. Probability-matrix coherence (P4 structure-fixed formula), driven
        # with its 24h-ticker contract. The volume arg matches the ecosystem's
        # scanner feed (thousands-scale units against the /50000 crypto S-term).
        ticker = {"price": close, "high": high_24h, "low": low_24h}
        prob_coh = float(MultiExchangeOrchestrator._calculate_coherence(
            prob_host, change_24h, quote_volume_24h / 1000.0, ticker, "crypto"))

        # 4. Λ(t) heartbeat from the measured readings (Γ = 1−|σ/μ|)
        readings = [
            SubsystemReading("auris_nodes", auris_coh, 0.9, "9-node blend"),
            SubsystemReading("probability_matrix", prob_coh, 0.8, "ecosystem coherence"),
            SubsystemReading("momentum", max(0.0, min(1.0, 0.5 + change_pct / 30.0)),
                             0.7, f"{change_pct:+.2f}%"),
        ]
        if risk is not None:
            readings.append(SubsystemReading(
                "volatility_sentinel", max(0.0, 1.0 - risk), 0.8, f"risk={risk:.2f}"))
        state = engine.step(readings)
        gammas.append(float(state.coherence_gamma))
        lambda_final = float(state.lambda_t)

        # 5. FFT-of-Λ timeline regime (P3)
        observer.ingest(ts, state.lambda_t)
        regime = str(observer.regime())
        regimes[regime] = regimes.get(regime, 0) + 1

        # 6. The signal on the historical timeline: the probability formula
        # above its own sigmoid midline, positive 24h momentum, sentinel clear.
        base_long = prob_coh > 0.5 and change_24h > 0.0
        long_now = base_long and not vetoed
        positions.append(1 if long_now else 0)
        positions_no_veto.append(1 if base_long else 0)
        if long_now and not prev_long:
            entry_signals += 1
        prev_long = long_now

    # decide-at-close, hold-to-next: the final decision has no next candle
    positions = positions[:-1]
    positions_no_veto = positions_no_veto[:-1]

    ret, max_dd, changes, fees = _equity_walk(closes, positions)
    ret_nv, _dd_nv, _ch_nv, _f_nv = _equity_walk(closes, positions_no_veto)
    buy_hold = (closes[-1] / closes[0] - 1.0) * 100.0
    _bh_ret, bh_dd, _bh_ch, _bh_f = _equity_walk(closes, [1] * (len(closes) - 1))

    # veto calibration: how often a veto candle sits in the top realized-vol
    # decile of the same series (measured precision, only when vetoes exist)
    ranges = sorted(((float(c["high"]) - float(c["low"])) / float(c["low"])
                     for c in candles if float(c["low"]) > 0), reverse=True)
    veto_precision: float | None = None
    n_veto = sum(1 for v in veto_flags if v)
    if n_veto and ranges:
        top_decile = ranges[max(0, len(ranges) // 10 - 1)]
        hits = sum(
            1 for c, v in zip(candles, veto_flags, strict=True)
            if v and float(c["low"]) > 0
            and (float(c["high"]) - float(c["low"])) / float(c["low"]) >= top_decile
        )
        veto_precision = round(hits / n_veto, 6)

    veto_windows = sum(
        1 for i, v in enumerate(veto_flags) if v and (i == 0 or not veto_flags[i - 1]))

    return SymbolReplay(
        symbol=symbol,
        candles=len(candles),
        provenance=dict(payload.get("provenance", {})),
        auris_coherence_mean=round(sum(auris_scores) / len(auris_scores), 6),
        auris_coherence_min=round(min(auris_scores), 6),
        auris_coherence_max=round(max(auris_scores), 6),
        gamma_mean=round(sum(gammas) / len(gammas), 6),
        lambda_final=round(lambda_final, 6),
        observer_regime_counts=dict(sorted(regimes.items())),
        vol_risk_max=round(vol_risk_max, 6),
        vol_assessments_ok=vol_ok,
        long_candles=sum(positions),
        entry_signals=entry_signals,
        veto_candles=n_veto,
        veto_windows=veto_windows,
        veto_high_vol_precision=veto_precision,
        strategy_return_pct=round(ret, 4),
        strategy_no_veto_return_pct=round(ret_nv, 4),
        buy_hold_return_pct=round(buy_hold, 4),
        veto_contribution_pct=round(ret - ret_nv, 4),
        max_drawdown_pct=round(max_dd, 4),
        buy_hold_max_drawdown_pct=round(bh_dd, 4),
        n_position_changes=changes,
        fees_paid_pct=round(fees, 4),
    )


def compute_replay_validation(data_dir: Path | None = None) -> ReplayValidationReport:
    """Replay every bundled symbol; missing datasets are named blockers."""
    results: list[SymbolReplay] = []
    blockers: list[str] = []
    for sym in SYMBOLS:
        payload = load_ohlc(sym, data_dir)
        if payload is None:
            blockers.append(
                f"{sym}: dataset missing/unreadable at data/historical/"
                f"kraken_ohlc_{sym}_60m.json — refetch with --refresh (no key needed)")
            continue
        results.append(replay_symbol(payload))

    return ReplayValidationReport(
        symbols=[r.to_dict() for r in results],
        total_candles=sum(r.candles for r in results),
        any_symbol_produced_signals=any(r.entry_signals > 0 for r in results),
        # a symbol in a falling month SHOULD stay flat — zero entries there is
        # the gate working, measured as drawdown avoided vs buy-and-hold
        capital_preserved_in_downtrends=all(
            r.max_drawdown_pct <= r.buy_hold_max_drawdown_pct for r in results),
        any_veto_fired=any(r.veto_candles > 0 for r in results),
        switch_to_live_note=(
            "Live cut-over is configuration, not code: the P3 daemon source feeds the same "
            "VolatilitySentinel from ws_cache/ws_prices.json (live exchange feeds), and the P4/P5 "
            "gates read the same canonical field — replace this file replay with the running daemon."),
        blockers=blockers,
    )


def refresh_datasets(data_dir: Path | None = None) -> list[str]:
    """Re-fetch the open Kraken OHLC datasets (public endpoint, no API key)."""
    import urllib.request

    out_dir = data_dir or DATA_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    kraken_pairs = {"BTCUSD": "XBTUSD", "ETHUSD": "ETHUSD", "SOLUSD": "SOLUSD"}
    for name, pair in kraken_pairs.items():
        url = f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval=60"
        with urllib.request.urlopen(url, timeout=30) as r:
            payload = json.load(r)
        if payload.get("error"):
            raise RuntimeError(f"kraken error for {name}: {payload['error']}")
        result = payload["result"]
        key = next(k for k in result if k != "last")
        candles = [
            {"ts": int(c[0]), "open": float(c[1]), "high": float(c[2]),
             "low": float(c[3]), "close": float(c[4]), "vwap": float(c[5]),
             "volume": float(c[6]), "trades": int(c[7])}
            for c in result[key]
        ]
        doc = {
            "provenance": {
                "source": "Kraken public market-data API (no API key required)",
                "url": url,
                "kraken_pair_key": key,
                "interval_minutes": 60,
                "fetched_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "license_note": "public exchange market data, retrieved from the open unauthenticated endpoint",
                "kind": "REAL historical OHLCV — not synthetic",
            },
            "symbol": name[:3] + "/" + name[3:],
            "candles": candles,
        }
        path = out_dir / f"kraken_ohlc_{name}_60m.json"
        path.write_text(json.dumps(doc), encoding="utf-8")
        written.append(str(path))
    return written


def write_replay_report(report: ReplayValidationReport,
                        out_json: Path) -> ReplayValidationReport:
    out_json.parent.mkdir(parents=True, exist_ok=True)
    payload = report.to_dict()
    payload["out_path"] = str(out_json)
    out_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    return ReplayValidationReport(**{**report.to_dict(), "out_path": str(out_json)})


def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description=REPLAY_BOUNDARY)
    ap.add_argument("--out", type=Path, default=None,
                    help="write the JSON artifact here (default: print summary)")
    ap.add_argument("--refresh", action="store_true",
                    help="re-fetch the open Kraken datasets first (no key needed)")
    args = ap.parse_args(argv)

    if args.refresh:
        for p in refresh_datasets():
            print(f"fetched {p}")

    report = compute_replay_validation()
    if args.out is not None:
        report = write_replay_report(report, args.out)
        print(f"wrote {report.out_path}")

    for s in report.symbols:
        print(f"\n{s['symbol']}  ({s['candles']} real candles)")
        print(f"  Auris 9-node coherence  mean={s['auris_coherence_mean']:.3f} "
              f"range=[{s['auris_coherence_min']:.3f}, {s['auris_coherence_max']:.3f}]")
        print(f"  HNC field               Γ mean={s['gamma_mean']:.3f}  "
              f"Λ final={s['lambda_final']:.3f}  regimes={s['observer_regime_counts']}")
        print(f"  Sentinel                max risk={s['vol_risk_max']:.3f}  "
              f"vetoes={s['veto_candles']} candle(s) in {s['veto_windows']} window(s)"
              + (f"  top-decile-vol precision={s['veto_high_vol_precision']}"
                 if s['veto_high_vol_precision'] is not None else ""))
        print(f"  Signals                 {s['entry_signals']} entries, "
              f"{s['long_candles']} long candles")
        print(f"  Revenue (fees incl.)    strategy={s['strategy_return_pct']:+.2f}%  "
              f"no-veto={s['strategy_no_veto_return_pct']:+.2f}%  "
              f"buy&hold={s['buy_hold_return_pct']:+.2f}%")
        print(f"  Risk                    maxDD={s['max_drawdown_pct']:.2f}% "
              f"(buy&hold {s['buy_hold_max_drawdown_pct']:.2f}%)  "
              f"fees={s['fees_paid_pct']:.2f}%  changes={s['n_position_changes']}")
    for b in report.blockers:
        print(f"  BLOCKER: {b}")
    print(f"\n{report.switch_to_live_note}")

    return 0 if (report.any_symbol_produced_signals and not report.blockers) else 1


if __name__ == "__main__":
    raise SystemExit(main())
