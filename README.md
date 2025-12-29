# 🎵🌌 THE SAMUEL HARMONIC TRADING ENTITY (SHTE)

> **Technical Overview & Quick Start**
>
> This repository includes a practical, modular trading orchestrator and companion "brain" process.
>
> - **[Technical Overview](docs/Technical-Overview.md)** — Capabilities, architecture, and quick start.
> - **[Operations Runbook](docs/Operations.md)** — Dry-run/live procedures and monitoring.
> - **[Troubleshooting](docs/Troubleshooting.md)** — Common issues and fixes.
> - **[Philosophy & Lore](docs/Philosophy.md)** — The metaphysical narrative behind the system.
>
> **Safety Note:** Losses are possible. Always run in dry-run/testnet mode first.

---

## 🎯 What Is A "Harmonic Algorithmic Pattern Probability Trading Platform"?

This system combines **three pillars** to find high-probability trades across **four battlefronts**:

| Pillar | What It Does | Code Module |
|--------|--------------|-------------|
| **Harmonic** | Fibonacci retracements, wave patterns, price rhythm detection | `aureon_harmonic_underlay.py` |
| **Algorithmic** | ML ensemble (XGBoost, LightGBM, Neural Nets), pattern recognition | `aureon_brain.py`, `aureon_miner_brain.py` |
| **Probability** | Bayesian inference, confidence scoring, risk-adjusted position sizing | `aureon_probability_nexus.py` |

### Signal Combination Example
```
Harmonic Score:     0.78 (Fibonacci 61.8% retracement detected)
Pattern Score:      0.82 (Bullish engulfing + volume spike)
ML Prediction:      0.71 (Ensemble agrees: UP)
─────────────────────────────────
Combined Signal:    0.77 → SCOUT DEPLOYED
```

### 🌍 Four Battlefronts (Multi-Exchange Architecture)

The system operates as **one unified army** across four trading platforms:

| Exchange | Asset Types | Role | Config Key |
|----------|-------------|------|------------|
| **Binance** | Crypto (USDT/USDC pairs) | Primary crypto battlefield | `BATTLEFIELDS["binance"]` |
| **Kraken** | Crypto | Secondary crypto, arbitrage | `BATTLEFIELDS["kraken"]` |
| **Capital.com** | CFDs (Forex, Indices, Commodities) | Traditional markets | `BATTLEFIELDS["capital"]` |
| **Alpaca** | US Stocks + Crypto | Equity exposure | `BATTLEFIELDS["alpaca"]` |

### 🎖️ The Scout → Sniper → Harvester Model

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUREON UNIFIED ECOSYSTEM                      │
├─────────────────────────────────────────────────────────────────┤
│  SCOUTS (irish_patriot_scouts.py)                               │
│  ├── Scan ALL 4 exchanges for opportunities                     │
│  ├── Round-robin distribution prevents exchange clustering      │
│  └── Deploy when combined_signal > 0.65                         │
│                           ↓                                      │
│  SNIPERS (ira_sniper_mode.py)                                   │
│  ├── High-precision entries on confirmed setups                 │
│  ├── Wait for optimal entry (limit orders, not market)          │
│  └── Risk-adjusted position sizing per battlefield              │
│                           ↓                                      │
│  HARVESTERS (aureon_unified_ecosystem.py)                       │
│  ├── Monitor open positions across all exchanges                │
│  ├── Trail stops, scale out at targets                          │
│  └── Feed profits back to compound growth                       │
└─────────────────────────────────────────────────────────────────┘
```

### 🍄 Mycelium Network (Cross-Exchange Intelligence)

The `aureon_mycelium.py` module acts as the nervous system:
- **Prevents duplicate positions** across exchanges (`_is_duplicate_across_exchanges()`)
- **Shares intelligence** between battlefronts
- **Coordinates entries** so we don't fight ourselves

### 🔄 Core Algorithm Flow

```
Market Data → Harmonic Analysis → Pattern Detection → ML Ensemble
                                                          ↓
                                              Probability Score
                                                          ↓
                              ┌─────────────────────────────────────┐
                              │  Score > 0.65? → Deploy Scout       │
                              │  Score > 0.75? → Sniper Mode        │
                              │  Score > 0.85? → Full Send          │
                              └─────────────────────────────────────┘
```

### ⚙️ Key Configuration

```python
# aureon_unified_ecosystem.py
BATTLEFIELDS = {
    "binance":  {"enabled": True, "scouts": True, "sniper": True, "harvester": True},
    "kraken":   {"enabled": True, "scouts": True, "sniper": True, "harvester": True},
    "capital":  {"enabled": True, "scouts": True, "sniper": True, "harvester": True},
    "alpaca":   {"enabled": True, "scouts": True, "sniper": True, "harvester": True},
}
MULTI_BATTLEFIELD_MODE = True
PREVENT_DUPLICATE_POSITIONS = True
```

---

## 🚀 Quick Start

1.  **Install Dependencies:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Configure Environment:**
    ```bash
    cp .env.example .env
    # Edit .env with your API keys and risk settings
    ```

3.  **Run the System (Dry-Run):**
    ```bash
    # Terminal 1: The Brain
    python aureon_miner.py

    # Terminal 2: The Ecosystem
    python aureon_unified_ecosystem.py
    ```

---

## 📂 Key Components

-   **Orchestrator:** `aureon_unified_ecosystem.py` - Manages strategy, risk, and execution.
-   **Brain:** `aureon_miner.py` - Generates probability signals and wisdom state.
-   **Simulation:** `aureon_51_sim.py` - Tests logic without placing orders.

## 🛡️ Safety & Compliance

-   **Risk Management:** Use `BINANCE_RISK_MAX_ORDER_USDT` to cap exposure.
-   **Dry-Run Default:** The system defaults to dry-run mode unless explicitly enabled.
-   **No Guarantees:** Past performance (or simulation) does not guarantee future results.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for code style and PR guidelines.
See [SECURITY.md](SECURITY.md) for vulnerability reporting.

## 📄 License

-   **Code:** MIT License
-   **Documentation/Media:** CC BY 4.0

---

*For the story of the Duck Commandos, the 11 Civilizations, and the Harmonic Nexus Core, see [docs/Philosophy.md](docs/Philosophy.md).*
