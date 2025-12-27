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
