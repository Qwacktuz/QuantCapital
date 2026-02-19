# 📈 QuantCapital

## ⚡ Quick Start

This project utilizes **Pixi** for high-performance package management and reproducible environments.

### 1. Environment Setup

Ensure [**Pixi**](https://prefix.dev/) is installed on your system, then initialize the project:

```bash
# Clone the repository
git clone https://github.com/Qwacktuz/QuantCapital
cd QuantCapital

# Synchronize dependencies and lockfile
pixi install
```

### 2. Execution

* **Example usage** `pixi run python main.py`
* **Normalized indicator pool construction** `pixi run python pool.py`
* **Research Notebooks** `pixi run jupyter notebooks`

## 📂 Project Architecture

```text
QuantCapital/
├── indicators/                # Technical analysis implementations
│   ├── __init__.py            # Exposes indicator classes
│   ├── indicator.py           # Base Indicator interface
│   ├── rsi.py                 # Relative Strength Index
│   ├── trends.py              # Josep's sliding_window_analysis
│   └── volatility.py          # Josep's 'ExponentialDecayMovingAverage'
│
├── labelers/                  # Label generation for supervised learning
│   ├── __init__.py            # Exposes labeler classes
│   ├── BaseLabeler.py         # Base Labeler interface
│   └── ZigZagLabeler.py       # ZigZag-based trend identification
│
├── legacy_scripts/            # Deprecated experimental assets
│
├── loaders/                   # Data ingestion layer
│   ├── __init__.py            # Exposes loader classes
│   ├── BaseLoader.py          # Base data Loader interface
│   ├── CsvLoader.py           # Local CSV OHLCV ingestion
│   └── ResearchBitcoinLoader.py # Custom research dataset loader
│
├── main.py                    # Core execution entry point
│
├── notebooks/                 # Jupyter research & visualization
│
├── ohlcv/                     # Local data cache (OHLCV)
│
├── pixi.lock                  # Deterministic dependency lock
├── pixi.toml                  # Manifest & dependency definitions
│
├── pool.py                    # Normalized indicator pool construction
│
├── README.md                  # Project documentation
│
├── resources/                 # Reference papers & academic material
│
└── tests/                     # Unit & Integration testing suite
    └── test_researchbitcoin_loader.py
```

## 🛠 Active Development (TODO/FIXME)
* **Data Persistence:** Unify the storage solution for cached OHLCV data.
* **Git Hygiene:** Add `ohlcv/` to `.gitignore` to prevent caching local API fetches.
* **Directory Mapping:** Resolve BitcoinLab/ pathing inconsistencies across loaders.
* **Notebook Context:** Fix relative path resolution for assets within `notebooks/`.
