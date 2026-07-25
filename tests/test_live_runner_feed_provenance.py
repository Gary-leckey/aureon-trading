"""
The Queen live runner must not manufacture the market it calls live.

What it did before this bound, on every 2-second cycle, with no provider connected:

  * ``market.price`` — prices seeded at ``50000 + random()*10000`` and random-walked each
    tick, plus ``volume_24h = random()*1000000`` and ``change_1h = (random()-0.5)*5``;
  * ``market.momentum`` — a "top momentum" symbol chosen by ``max(key=lambda s: random())``
    with a random 1h change and a random volume-surge flag;
  * ``whale.orderbook`` — random bid/ask depth, an imbalance computed from those random
    numbers, and two invented "walls";
  * ``bot.detected`` / ``firm.activity`` / ``counter.strategy`` — trading-firm attribution
    picked by hashing ``<symbol>_<current minute>``, firing on ~60% of hashes, with a
    "confidence" of 0.65–0.98 read off the hash's low digits.

All of it went out on the same ThoughtBus topics real market data uses, under the banner
"REAL INTELLIGENCE MODE", to be read by the system hub dashboard as "live data". Naming a
real firm as the counterparty to activity nobody observed is the least defensible of these.

Every synthetic value now sits behind ``AUREON_ALLOW_SIMULATED_FEED``, default off. In the
default mode the runner emits real readings or an honest ``no_data`` with a named blocker;
in the opt-in mode every synthetic thought is stamped ``test_fixture``.
"""

from __future__ import annotations

import importlib
import json

import pytest


@pytest.fixture
def runner(tmp_path, monkeypatch):
    """The runner module with its thought stream pointed at a tmp file."""
    monkeypatch.setenv("AUREON_SUPPRESS_IMPORT_SIDE_EFFECTS", "1")
    monkeypatch.setenv("AUREON_AUDIT_MODE", "1")
    monkeypatch.setenv("AUREON_THOUGHTS_FILE", str(tmp_path / "thoughts.jsonl"))
    monkeypatch.delenv("AUREON_ALLOW_SIMULATED_FEED", raising=False)

    import aureon.trading.aureon_queen_live_runner as lr

    importlib.reload(lr)
    return lr


def _thoughts(lr) -> list[dict]:
    path = lr.THOUGHTS_FILE
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            out.append(json.loads(line))
    return out


def _by_topic(rows: list[dict], topic: str) -> list[dict]:
    return [r for r in rows if r.get("topic") == topic]


# ── the switch ──────────────────────────────────────────────────────────────────

def test_synthetic_feed_is_off_unless_explicitly_asked_for(runner):
    assert runner.simulated_feed_allowed() is False


def test_synthetic_feed_switch_accepts_the_usual_truthy_spellings(runner, monkeypatch):
    for value in ("1", "true", "YES", "on"):
        monkeypatch.setenv("AUREON_ALLOW_SIMULATED_FEED", value)
        assert runner.simulated_feed_allowed() is True
    for value in ("", "0", "false", "no", "maybe"):
        monkeypatch.setenv("AUREON_ALLOW_SIMULATED_FEED", value)
        assert runner.simulated_feed_allowed() is False


# ── prices ──────────────────────────────────────────────────────────────────────

def test_no_provider_means_no_price_not_an_invented_one(runner):
    """The original defect: a fresh process with nothing connected still published prices."""
    gen = runner.LiveMarketDataGenerator()
    assert gen.fetch_prices() == {}
    gen.emit_market_data()

    rows = _thoughts(runner)
    assert _by_topic(rows, "market.price") == []

    status = _by_topic(rows, "market.feed_status")
    assert status, "a missing feed must be reported, not passed over in silence"
    payload = status[-1]["payload"]
    assert payload["quoted"] == []
    assert sorted(payload["unquoted"]) == sorted(gen.symbols)
    assert payload["blocker"], "the blocker must be named"
    assert status[-1]["truth_status"] == "no_data"


def test_a_real_quote_is_published_and_marked_live(runner, monkeypatch):
    """The bound must not break the real case."""
    gen = runner.LiveMarketDataGenerator()
    monkeypatch.setattr(gen, "symbols", ["BTC/USD"])
    monkeypatch.setattr(gen, "fetch_prices",
                        lambda: (gen.real_symbols.add("BTC/USD"), {"BTC/USD": 61234.5})[1])

    gen.emit_market_data()
    prices = _by_topic(_thoughts(runner), "market.price")
    assert len(prices) == 1
    assert prices[0]["truth_status"] == "live"
    assert prices[0]["payload"]["price"] == pytest.approx(61234.5)


def test_volume_and_change_are_withheld_not_fabricated(runner, monkeypatch):
    """No provider supplies these, so they are named as withheld rather than invented."""
    gen = runner.LiveMarketDataGenerator()
    monkeypatch.setattr(gen, "symbols", ["BTC/USD"])
    monkeypatch.setattr(gen, "fetch_prices",
                        lambda: (gen.real_symbols.add("BTC/USD"), {"BTC/USD": 61234.5})[1])

    gen.emit_market_data()
    payload = _by_topic(_thoughts(runner), "market.price")[0]["payload"]
    assert payload["volume_24h"] is None
    assert payload["change_1h"] is None
    assert set(payload["withheld"]) == {"volume_24h", "change_1h"}


def test_a_symbol_that_stops_being_quoted_stops_being_published(runner, monkeypatch):
    """Serving the last known price forever would turn a dead feed into a flat market."""
    gen = runner.LiveMarketDataGenerator()
    monkeypatch.setattr(gen, "symbols", ["BTC/USD"])

    class _Service:
        value = 61234.5

        def get_ticker(self, _symbol):
            return self.value

    service = _Service()
    monkeypatch.setitem(
        __import__("sys").modules, "aureon_central_prefetch_service",
        type("_M", (), {"prefetch_service": service})(),
    )
    assert gen.fetch_prices() == {"BTC/USD": pytest.approx(61234.5)}

    service.value = None                       # the venue goes quiet
    assert gen.fetch_prices() == {}
    assert gen.real_symbols == set()


def test_the_synthetic_feed_still_works_but_is_stamped_a_fixture(runner, monkeypatch):
    """Opt-in demo mode is allowed to invent numbers; it is not allowed to look real."""
    monkeypatch.setenv("AUREON_ALLOW_SIMULATED_FEED", "1")
    gen = runner.LiveMarketDataGenerator()
    assert gen.simulated is True
    assert len(gen.fetch_prices()) == len(gen.symbols)

    gen.emit_market_data()
    prices = _by_topic(_thoughts(runner), "market.price")
    assert prices, "the demo stream must still stream"
    assert {r["truth_status"] for r in prices} == {"test_fixture"}


# ── orderbook depth ─────────────────────────────────────────────────────────────

def test_orderbook_depth_and_walls_are_reported_missing_not_invented(runner):
    tracker = runner.LiveWhaleTracker()
    tracker.emit_whale_data({"BTC/USD": 61234.5})

    books = _by_topic(_thoughts(runner), "whale.orderbook")
    assert len(books) == 1
    payload = books[0]["payload"]
    assert payload["bids_depth"] is None
    assert payload["asks_depth"] is None
    assert payload["imbalance"] is None
    assert payload["walls"] == []
    assert payload["blocker"] == "no_orderbook_feed_connected"
    assert books[0]["truth_status"] == "no_data"


# ── firm attribution ────────────────────────────────────────────────────────────

def test_no_firm_is_named_without_observed_order_flow(runner):
    """A hash of symbol+minute is not evidence about Citadel, Jump, or anyone else."""
    tracker = runner.LiveBotTracker()
    assert tracker.detect_bots({"BTC/USD": 61234.5, "ETH/USD": 3000.0}) == []
    for symbol in ("BTC/USD", "ETH/USD", "SOL/USD"):
        assert tracker._match_firm_pattern(symbol) is None

    tracker.emit_bot_data({"BTC/USD": 61234.5})
    rows = _thoughts(runner)
    assert _by_topic(rows, "bot.detected") == []
    assert _by_topic(rows, "firm.activity") == []
    assert _by_topic(rows, "counter.strategy") == []

    status = _by_topic(rows, "bot.feed_status")
    assert status, "zero detections must be explained, not left to read as a quiet market"
    assert status[-1]["truth_status"] == "no_data"
    assert status[-1]["payload"]["blocker"]


def test_firm_attribution_returns_under_the_opt_in_and_is_labelled(runner, monkeypatch):
    monkeypatch.setenv("AUREON_ALLOW_SIMULATED_FEED", "1")
    tracker = runner.LiveBotTracker()
    if not tracker.firm_signatures:
        pytest.skip("firm signature table unavailable in this environment")

    # The hash fires on ~60% of symbols, so sweep enough to be sure of at least one.
    symbols = {f"SYM{i}/USD": 1.0 for i in range(20)}
    bots = tracker.detect_bots(symbols)
    assert bots, "the demo stream must still produce detections"

    tracker.emit_bot_data(symbols)
    detected = _by_topic(_thoughts(runner), "bot.detected")
    assert {r["truth_status"] for r in detected} == {"test_fixture"}


# ── momentum ────────────────────────────────────────────────────────────────────

def test_momentum_ranking_is_withheld_without_a_price_history(runner):
    scanner = runner.LiveScannerEngine()
    scanner.emit_scanner_data({"BTC/USD": 61234.5, "ETH/USD": 3000.0})

    momentum = _by_topic(_thoughts(runner), "market.momentum")
    assert len(momentum) == 1
    assert momentum[0]["payload"]["top_momentum"] is None
    assert momentum[0]["payload"]["blocker"] == "no_price_history_source"
    assert momentum[0]["truth_status"] == "no_data"


# ── the envelope ────────────────────────────────────────────────────────────────

def test_every_thought_carries_a_contract_truth_status(runner):
    """A consumer must be able to tell provenance from the envelope alone, without
    knowing which producer wrote the row."""
    from aureon.observer.real_data_contract import TRUTH_STATUSES

    gen = runner.LiveMarketDataGenerator()
    gen.emit_market_data()
    runner.LiveWhaleTracker().emit_whale_data({"BTC/USD": 61234.5})
    runner.LiveBotTracker().emit_bot_data({"BTC/USD": 61234.5})
    runner.LiveScannerEngine().emit_scanner_data({"BTC/USD": 61234.5})

    rows = _thoughts(runner)
    assert rows
    for row in rows:
        assert row.get("truth_status") in TRUTH_STATUSES, row.get("topic")


def test_the_thought_stream_is_the_one_the_hub_dashboard_reads(runner, monkeypatch):
    """These were two different files — aureon/trading/thoughts.jsonl for the runner,
    aureon/command_centers/thoughts.jsonl for the dashboard that spawns it — so nothing
    the runner emitted ever arrived."""
    monkeypatch.delenv("AUREON_THOUGHTS_FILE", raising=False)
    importlib.reload(runner)
    runner_path = runner.THOUGHTS_FILE

    flask = pytest.importorskip("flask", reason="the hub dashboard requires flask")
    assert flask
    psutil = pytest.importorskip("psutil", reason="the hub dashboard requires psutil")
    assert psutil
    import aureon.command_centers.aureon_system_hub_dashboard as hub

    importlib.reload(hub)
    assert runner_path == hub.THOUGHTS_FILE


def test_the_hub_dashboard_points_at_a_runner_that_exists(runner):
    """The spawn path was Path(__file__).parent / "aureon_queen_live_runner.py" in
    command_centers/, where no such file has ever existed, so the auto-start silently
    never fired."""
    pytest.importorskip("flask", reason="the hub dashboard requires flask")
    pytest.importorskip("psutil", reason="the hub dashboard requires psutil")
    import aureon.command_centers.aureon_system_hub_dashboard as hub

    assert hub.LIVE_RUNNER_SCRIPT.exists()
    assert hub.LIVE_RUNNER_SCRIPT.name == "aureon_queen_live_runner.py"


def test_opening_a_dashboard_does_not_launch_a_background_producer(runner, monkeypatch):
    pytest.importorskip("flask", reason="the hub dashboard requires flask")
    pytest.importorskip("psutil", reason="the hub dashboard requires psutil")
    import aureon.command_centers.aureon_system_hub_dashboard as hub

    monkeypatch.delenv("AUREON_AUTOSTART_LIVE_RUNNER", raising=False)
    assert hub._autostart_live_runner_allowed() is False

    spawned = []
    monkeypatch.setattr(hub.subprocess, "Popen", lambda *a, **k: spawned.append(a))
    monkeypatch.setattr(hub, "_is_process_running", lambda _match: False)
    assert hub._ensure_live_runner() is False
    assert spawned == []

    monkeypatch.setenv("AUREON_AUTOSTART_LIVE_RUNNER", "1")
    assert hub._ensure_live_runner() is True
    assert len(spawned) == 1
