🧮 Retirement Simulator
________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
A Python-based retirement simulation tool that estimates how long your savings can last based on inflation, investment returns, and country-specific tax brackets (Canada or Brazil).

The program calculates:

✅ The earliest feasible retirement age given your savings

📊 The required starting balance to sustain your lifestyle until a target age

💰 The monthly investment needed to reach financial independence
________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
🚀 Features

Country-specific progressive tax systems (Canada 🇨🇦 / Brazil 🇧🇷)

Backward analysis to determine when your savings can sustain expenses

Inflation-adjusted yearly budgets

Optional monthly investment calculator

Clear, year-by-year breakdown of balance, spending, and returns
________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
🧠 How It Works

The program runs a backward simulation from your maximum age to your current age, determining the required starting balance to end with exactly zero at the final year. It accounts for taxes, compound interest, and inflation, adjusting your real purchasing power each year.
_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
🧩 Inputs

When you run the program, you’ll be prompted for:

Country (Canada or Brasil)

Initial balance

Monthly budget

Annual inflation (%)

Annual interest rate (%)

Maximum age

Current age

(Optional) Initial investment amount
____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
🖥️ Run the Program
# Clone the repository
git clone https://github.com/YOUR-USERNAME/retirement-simulator.git

# Navigate to folder
cd retirement-simulator

# Run the simulation
python retirement_simulator.py

____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
🔮 Future Features (planned / roadmap)

These are the exact features we’ll add next (clear, actionable items):

Baseline for depletion

Compute and display a depletion baseline chart and table showing the year and age when balance crosses thresholds (e.g., 75%, 50%, 25%, 0% of starting balance).

Add textual summary: “Portfolio estimated to fall below 50% in YEAR / at AGE.”

Input mode: retirement age or retirement fund (money)

Two modes:

Age mode: user supplies desired retirement age → simulator finds required starting balance (current design).

Money mode: user supplies a target leftover (or target starting fund) → simulator returns feasible retirement age(s).

UI/CLI flag so users can switch mode (--mode age / --mode money).

Contribution & budget log (dynamic rebalancing)

Add a CSV/JSON log that users can append with real monthly contributions and actual monthly budgets.

On each run the model:

Reads log entries,

Adjusts the current balance and average contributions,

Recomputes projections dynamically so the forecast reflects actual behavior.

Example: contributions.csv with columns date, amount, type (contribution/budget).

Interactive reforecast

Allow the model to re-run after feeding historical contributions/budgets and provide updated required monthly contributions going forward.

Visualization & export

Matplotlib/Plotly charts for:

Required start balance vs start age,

Year-by-year balance, withdrawals, and taxes,

Depletion baseline heatmap.

Export results to CSV and PDF.

Scenario comparison

Save and compare multiple scenarios (e.g., different inflation, interest, tax regimes) side-by-side.

Improved tax realism

Option to toggle between monthly vs annualized tax treatment and add common deductions (e.g., standard deduction, dependents).

________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
🧾 License

This project is released under the MIT License.
