import pandas as pd

# ----- User Inputs -----
def get_float(prompt, default):
    val = input(f"{prompt} [{default}]: ").strip()
    return float(val) if val else default

def get_int(prompt, default):
    val = input(f"{prompt} [{default}]: ").strip()
    return int(val) if val else default

print("=== Retirement Simulation Parameters ===")
country = input("Select country for tax calculation (Canada/Brasil) [Canada]: ").strip().capitalize() or "Canada"
initial_balance = get_float("Initial Balance ($)", 3_000_000)
monthly_budget = get_float("Monthly Budget ($)", 5000)
inflation = get_float("Annual Inflation (e.g., 0.03 for 3%)", 0.03)
interest = get_float("Annual Interest (e.g., 0.05 for 5%)", 0.05)
max_age = get_int("Maximum Age", 100)
current_age = get_int("Current Age (for monthly investment calc)", 30)
initial_investment = get_float("Initial Investment ($)", 0)
print()

# ----- Tax Brackets -----
TAX_BRACKETS_Canada = [
    (15000, 0.00), (49231, 0.2005), (53359, 0.2415), (86696, 0.2965),
    (98463, 0.3148), (102139, 0.3389), (106717, 0.3791), (150000, 0.4341),
    (165430, 0.4497), (220000, 0.4829), (235675, 0.4985), (float("inf"), 0.5353)
]

TAX_BRACKETS_Brasil = [
    (22847.76, 0.0), (33919.80, 0.075), (45012.60, 0.15), (55976.16, 0.225),
    (float("inf"), 0.275)
]

TAX_BRACKETS = TAX_BRACKETS_Canada if country.lower() == "canada" else TAX_BRACKETS_Brasil

# ----- Tax helpers -----
def calc_tax(amount, brackets=TAX_BRACKETS):
    """Progressive tax: returns total tax amount for `amount`."""
    if amount <= 0:
        return 0.0
    tax = 0.0
    lower = 0.0
    for upper, rate in brackets:
        taxable = min(amount, upper) - lower
        if taxable > 0:
            tax += taxable * rate
        lower = upper
        if amount <= upper:
            break
    return tax

def gross_withdrawal_for_net(net_amount, brackets=TAX_BRACKETS):
    """Find gross withdrawal G such that net = G - tax(G) == net_amount."""
    if net_amount <= 0:
        return 0.0, 0.0
    guess = max(net_amount / 0.75, net_amount)
    for _ in range(400):
        tax = calc_tax(guess, brackets)
        net = guess - tax
        diff = net_amount - net
        if abs(diff) < 0.01:
            break
        guess += diff * 0.9
        if guess < 0:
            guess = net_amount
    tax = calc_tax(guess, brackets)
    return guess, tax

# ----- Forward depletion simulation -----
balance = initial_balance
annual_budget = monthly_budget * 12
records = []
year_count = 0
max_years = 200  # safety cap

# First, estimate how many years until depletion
while balance > 0 and year_count < max_years:
    year_count += 1
    # Interest and tax
    gain = balance * interest
    tax_on_gain = calc_tax(gain)
    after_gain_balance = balance + (gain - tax_on_gain)
    
    # Budget (inflated)
    budget_this_year = annual_budget * ((1 + inflation) ** (year_count - 1))
    
    # Gross withdrawal to match net budget
    gross_withdrawal, tax_on_withdrawal = gross_withdrawal_for_net(budget_this_year)
    
    # End balance
    end_balance = after_gain_balance - gross_withdrawal
    
    # Record
    records.append({
        "Budget": round(budget_this_year, 2),
        "Withdrawal_Tax": round(tax_on_withdrawal, 2),
        "After_Tax_Balance": round(after_gain_balance, 2),
        "End_Balance": round(end_balance, 2)
    })
    
    balance = end_balance

years_to_deplete = len(records)
optimal_retirement_age = max_age - years_to_deplete + 1

# ----- Convert records to DataFrame -----
df = pd.DataFrame(records)
df["Age"] = [optimal_retirement_age + i for i in range(years_to_deplete)]
df = df[["Age", "Budget", "Withdrawal_Tax", "After_Tax_Balance", "End_Balance"]]

# ----- Print Results -----
print("\n===== Retirement Simulation Results =====")
print(f"Initial balance:       ${initial_balance:,.2f}")
print(f"Monthly budget:        ${monthly_budget:,.2f} → annual ${annual_budget:,.2f}")
print(f"Interest rate (annual):{interest*100:.2f}%")
print(f"Inflation rate (annual):{inflation*100:.2f}%")
print(f"Country tax system used: {country}")
print(f"Years until depletion:  {years_to_deplete}")
print(f"Optimal retirement age: {optimal_retirement_age} (max_age {max_age})")
print(f"Final end balance:      ${balance:,.2f}")
print("="*60)

pd.options.display.float_format = '{:,.2f}'.format
print("\nFirst 8 years (starting from optimal age):")
print(df.head(8).to_string(index=False))
print("\nLast 6 years (ending at max_age):")
print(df.tail(6).to_string(index=False))

# ----- Monthly investment calculation -----
def monthly_investment_to_target(target_amount, from_age, target_age, annual_interest, initial_investment=0.0):
    n_years = target_age - from_age
    n_months = max(0, n_years * 12)
    if n_months == 0:
        return max(0.0, target_amount - initial_investment)
    monthly_rate = (1 + annual_interest) ** (1/12) - 1
    fv_initial = initial_investment * (1 + monthly_rate) ** n_months
    numerator = (target_amount - fv_initial) * monthly_rate
    denominator = (1 + monthly_rate) ** n_months - 1
    if denominator == 0:
        return float('inf')
    return numerator / denominator

if optimal_retirement_age > current_age:
    monthly_needed = monthly_investment_to_target(
        initial_balance, current_age, optimal_retirement_age, interest, initial_investment
    )
    print(f"\nTo reach ${initial_balance:,.0f} by age {optimal_retirement_age},")
    print(f"you need to invest ≈ ${monthly_needed:,.2f}/month starting at age {current_age},")
    print(f"assuming {interest*100:.1f}% annual growth and current investment ${initial_investment:.2f}.")
else:
    print("\nNo accumulation period (optimal retirement age <= current age).")

