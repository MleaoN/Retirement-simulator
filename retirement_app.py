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
start_year = 2025
start_age = get_int("Current Age (this is the minimum candidate start age)", 30)
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

# Typical tax on investment income (approx.)
tax_rate_on_investment = 0.25 if country.lower() == "canada" else 0.15

# ----- Tax Calculation -----
def calc_tax(income):
    tax = 0.0
    lower = 0.0
    for upper, rate in TAX_BRACKETS:
        if income > upper:
            tax += (upper - lower) * rate
            lower = upper
        else:
            tax += (income - lower) * rate
            break
    return tax

def gross_withdrawal_for_net(net_amount):
    """Return gross withdrawal and tax amount required so net after tax == net_amount."""
    guess = max(net_amount / 0.75, net_amount)
    for _ in range(200):
        tax = calc_tax(guess)
        net = guess - tax
        diff = net_amount - net
        if abs(diff) < 0.01:
            break
        guess += diff * 0.9
    tax = calc_tax(guess)
    return guess, tax

# ----- Backward Simulation -----
def backward_simulation_required_start_balance(target_age, candidate_start_age, annual_budget, interest_rate, inflation_rate):
    """
    For a given candidate_start_age, build the annual budgets:
      budget_at_start_age = annual_budget
      next_year = budget_at_start_age * (1+inflation)
      ...
      up to target_age
    Then backward compute required starting balance so final balance at target_age is zero.
    """
    if candidate_start_age > target_age:
        raise ValueError("candidate_start_age must be <= target_age")

    n_years = target_age - candidate_start_age + 1
    budgets = [annual_budget * ((1 + inflation_rate) ** i) for i in range(n_years)]

    balance_next = 0.0
    balances = [0.0] * n_years

    for i in reversed(range(n_years)):
        net_need = budgets[i]
        gross, tax_paid = gross_withdrawal_for_net(net_need)
        effective_interest = interest_rate * (1 - tax_rate_on_investment)
        balance_current = (balance_next + gross) / ((1 + effective_interest) / (1 + inflation_rate))
        balances[i] = round(balance_current, 2)
        balance_next = balance_current

    required_start_balance = balances[0]
    return required_start_balance, budgets, balances

# ----- Find earliest feasible start age -----
earliest_feasible_age = None
earliest_required_balance = None
earliest_budgets = None
earliest_balances = None

annual_budget = monthly_budget * 12

for candidate_age in range(start_age, max_age + 1):
    req_balance, budgets, balances = backward_simulation_required_start_balance(
        max_age, candidate_age, annual_budget, interest, inflation
    )
    if req_balance <= initial_balance:
        earliest_feasible_age = candidate_age
        earliest_required_balance = req_balance
        earliest_budgets = budgets
        earliest_balances = balances
        break

# ----- Monthly Investment Calculation -----
def monthly_investment_to_target(target_amount, invest_from_age, target_age, annual_interest, initial_investment=0):
    n_years = target_age - invest_from_age
    n_months = max(0, n_years * 12)
    if n_months == 0:
        return max(0.0, target_amount - initial_investment)
    monthly_rate = annual_interest / 12
    fv_initial = initial_investment * (1 + monthly_rate) ** n_months
    numerator = (target_amount - fv_initial) * monthly_rate
    denominator = (1 + monthly_rate) ** n_months - 1
    if denominator == 0:
        return float('inf')
    P = numerator / denominator
    return max(0.0, P)

# ----- Output -----
print("\n===== Simulation Summary =====")
print(f"Country:              {country}")
print(f"Initial Balance:      ${initial_balance:,.2f}")
print(f"Monthly Budget:       ${monthly_budget:,.2f}")
print(f"Annual Inflation:     {inflation*100:.2f}%")
print(f"Annual Interest:      {interest*100:.2f}%")
print(f"Investment Tax Rate:  {tax_rate_on_investment*100:.1f}%")
print(f"Maximum Age:          {max_age} years")
print(f"Start Year (fixed):   {start_year}")
print(f"Candidate start age range: {start_age} to {max_age}")
print("="*40)

if earliest_feasible_age is not None:
    print(f"\n✅ Earliest feasible start age where your initial balance lasts to age {max_age}: {earliest_feasible_age}")
    print(f"   Required starting balance at age {earliest_feasible_age}: ${earliest_required_balance:,.2f}")
    print("\n   Year-by-year (age, budget_after_tax, required_balance_at_year_start):")
    for i, age in enumerate(range(earliest_feasible_age, max_age+1)):
        print(f"    Age {age:3d}: Budget ${earliest_budgets[i]:,.2f}, Required balance ${earliest_balances[i]:,.2f}")
    monthly_needed = monthly_investment_to_target(earliest_required_balance, start_age, earliest_feasible_age, interest, initial_investment)
    print(f"\n💰 Monthly contribution needed from age {start_age} to reach ${earliest_required_balance:,.2f} by age {earliest_feasible_age} (initial invest ${initial_investment:,.2f}): ${monthly_needed:,.2f}")
else:
    reqs = []
    for candidate_age in range(start_age, max_age + 1):
        req_balance, _, _ = backward_simulation_required_start_balance(max_age, candidate_age, annual_budget, interest, inflation)
        reqs.append((candidate_age, req_balance))
    min_req = min(reqs, key=lambda x: x[1])
    print("\n⚠️ Not feasible: your initial balance is not sufficient for any candidate start age in the tested range.")
    print(f"   The minimum required starting balance across ages {start_age}-{max_age} is at age {min_req[0]} requiring ${min_req[1]:,.2f}")
    print("   (You can lower budget, increase interest, or increase initial balance to make it feasible.)")
