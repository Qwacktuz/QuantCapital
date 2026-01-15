# QuantCapital price analysis framework

---

## 🛠️ Installation & Setup

This project uses [Pixi](https://prefix.dev/) for package management.

1. **Clone the repository:**

   ```bash
   git clone <repo_url>
   cd QuantCapital
   ```

2. **Install Dependencies:**
   Pixi will automatically create a virtual environment and install Python, Pandas, Matplotlib, etc.

   ```bash
   pixi install
   ```

3. **Run the Main Pipeline:**
   Execute the primary entry point to load data, calculate indicators, and plot results.

   ```bash
   pixi run python main.py
   ```

4. **Run Jupyter Notebooks:**
   To explore the research notebooks:

   ```bash
   pixi run jupyter notebook
   ```

---

## 📂 Project Structure

```text
QuantCapital/
├── core/                   # The core framework
│   ├── interfaces.py       # Abstract Base Classes (The rules/framework for new code)
│   └── data.py             # Misc. Data Loaders (CSV, APIs)
├── indicators/             # Technical Analysis Logic
│   ├── rsi.py              # Relative Strength Index
│   ├── volatility.py       # MA Bands, EMA Bands
│   └── trends.py           # Adaptive Trend / Sliding Window logic
├── evaluation/             # Logic for testing and labeling
│   └── labelers.py         # ZigZag algorithm for ground truth detection
├── notebooks/              # Research and Prototyping (Jupyter)
├── ohlcv/                  # Data storage/cache
├── main.py                 # Main entrypoint
└── pixi.toml               # Dependency configuration
```

---

## TODO/FIXME

- Unify data storge solution
  - Maybe add ohlcv/ to gitignore since these files are technically just fetched from the API as cache
  - Agree on some way to store/fetch data long(er) term
  - Fix/implement/unify BitCoinLab/ data directory properly together with other sources
- Fix relative path issue with jupyter notebooks/

