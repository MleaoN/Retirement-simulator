🧮 Retirement Simulator

A Python-based retirement simulation tool that estimates how long your savings will last — or how much you’ll need to retire — based on inflation, investment returns, and country-specific tax brackets (🇨🇦 Canada or 🇧🇷 Brazil).

It handles progressive taxation, inflation-adjusted expenses, and compound returns, giving realistic long-term financial projections.
__________________________________________________________________________________________________________________________________________________________________
📊 Core Calculations

The program computes:

✅ Depletion simulation – projects your savings year by year until depletion.
✅ Post-tax net balance – accounts for actual tax burden before reinvestment or withdrawal.
✅ Inflation-adjusted budgets – expenses grow with inflation.
✅ Country-specific progressive taxation – income distributed across all applicable tax brackets.
✅ Optional investment simulation – monthly contributions before retirement.
_____________________________________________________________________________________________________________________________________________________________________
🚀 Features

🇨🇦 Canadian and 🇧🇷 Brazilian progressive tax systems

After-tax correction: income taxed across all relevant brackets

Inflation-adjusted spending to maintain real purchasing power

Backward/forward simulations for flexible analysis

Year-by-year detailed breakdown:

Interest earned

Taxes paid

Withdrawals

Ending balance
_____________________________________________________________________________________________________________________________________________________________________
🧠 How It Works

Each year, the simulator:

Applies investment growth (interest rate)

Deducts taxes based on the progressive tax system of your chosen country

Subtracts living expenses, adjusted for inflation

Records the net balance and repeats until depletion or maximum age

🇧🇷 Brazilian Tax System Example

In Brazil, every portion of income falls into its corresponding tax bracket — meaning higher income parts are taxed more heavily.

Example:
===== Retirement Simulation Results =====
Initial balance:       $7,000,000.00
Monthly budget:        $20,000.00 → annual $240,000.00
Interest rate (annual):12.00%
Inflation rate (annual):6.00%
Country tax system used: Brasil
Years until depletion:  36
Optimal retirement age: 65 (max_age 100)
Final end balance:      $-643,849.11
============================================================

First 2 years (starting from optimal age):
 Age     Budget  Withdrawal_Tax  After_Tax_Balance  End_Balance
  65 240,000.00       76,645.08       7,619,432.32 7,302,787.23
  66 254,400.00       82,107.15       7,948,562.04 7,612,054.89

✅ Reflects Brazil’s “income falls within all brackets” model.
________________________________________________________________________________________________________________________________________
🇨🇦 Canadian Tax System Example

In Canada, federal and provincial brackets combine to determine total income tax.
The simulator simplifies this by merging them into a representative progressive system for clear financial projection.

Example:
===== Retirement Simulation Results =====
Initial balance:       $3,000,000.00
Monthly budget:        $5,000.00 → annual $60,000.00
Interest rate (annual):5.00%
Inflation rate (annual):3.00%
Country tax system used: Canada
Years until depletion:  41
Optimal retirement age: 60 (max_age 100)
Final end balance:      $-97,273.01
============================================================

First 2 years (starting from optimal age):
 Age    Budget  Withdrawal_Tax  After_Tax_Balance  End_Balance
  60 60,000.00       13,971.98       3,106,780.63 3,032,808.65
  61 61,800.00       14,730.61       3,140,492.01 3,063,961.39
  
✅ Shows realistic after-tax investment depletion aligned with Canadian brackets.
_________________________________________________________________________________________________________________________________________

🖥️ Run the Program
# Clone the repository
git clone https://github.com/YOUR-USERNAME/retirement-simulator.git

# Navigate to folder
cd retirement-simulator

# Run the simulation
python retirement_simulator.py
_____________________________________________________________________________________________________________________________________________

🔮 Roadmap
Upcoming Features

✅ Depletion baseline chart

Graph + table showing when balance crosses 75%, 50%, 25%, and 0% thresholds

Text summary: “Portfolio estimated to fall below 50% in YEAR / at AGE”

✅ Mode selection

--mode age → find required starting balance for target age

--mode money → find feasible retirement age for given fund

✅ Real contribution logging

Track actual monthly deposits & withdrawals from CSV

Automatically adjust projections

✅ Visualization & export

Matplotlib/Plotly charts

Export to CSV and PDF

✅ Scenario comparison

Save and contrast different inflation, tax, and investment assumptions

✅ Enhanced tax realism

Add monthly vs annual options

Include deductions and dependents
_________________________________________________________________________________________________________________________________________

🧾 License

This project is released under the MIT License.

