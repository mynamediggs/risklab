import numpy as np



np.random.seed(42)

def simulate_portfolio(claim_rate, num_policies, average_claim_cost):
  claims = np.random.poisson(claim_rate, num_policies)

  severity_sigma = 1.0
  severity_mu = np.log(average_claim_cost) - severity_sigma ** 2 / 2

  claim_costs = np.random.lognormal(
    mean=severity_mu,
    sigma=severity_sigma,
    size=int(claims.sum())
  )

  policy_losses = np.zeros(num_policies)
  claim_index = 0

  for i in range(num_policies):
    num_claims = claims[i]

    policy_losses[i] = claim_costs[
      claim_index:claim_index + num_claims
    ].sum()

    claim_index += num_claims

  return {
    "total_claims": int(claims.sum()),
    "total_losses": float(policy_losses.sum()),
    "average_loss": float(policy_losses.mean()),
    "largest_policy_loss": float(policy_losses.max()),
    "policies_with_claims": int(np.count_nonzero(claims)),
    "average_claim_severity": (
      float(claim_costs.mean()) if claim_costs.size > 0 else 0.0
    ),
    "largest_claim": (
      float(claim_costs.max()) if claim_costs.size > 0 else 0.0
    )
  }

def monte_carlo_simulation():
  num_simulations = 10000

  total_claims_per_year = np.zeros(num_simulations)
  policies_with_claims_per_year = np.zeros(num_simulations)
  average_claim_severities = np.zeros(num_simulations)
  largest_claims = np.zeros(num_simulations)
  portfolio_losses = np.zeros(num_simulations)

  for i in range(num_simulations):
    results = simulate_portfolio()

    portfolio_losses[i] = results["total_losses"]
    total_claims_per_year[i] = results["total_claims"]
    policies_with_claims_per_year[i] = results["policies_with_claims"]
    average_claim_severities[i] = results["average_claim_severity"]
    largest_claims[i] = results["largest_claim"]

  p95 = np.percentile(portfolio_losses, 95)
  p99 = np.percentile(portfolio_losses, 99)

  print(f"Number of simulated years:", num_simulations)
  print(f"Average annual loss: ${portfolio_losses.mean():,.2f}")
  print("Median annual loss:", np.median(portfolio_losses))
  print("Minimum annual loss:", portfolio_losses.min())
  print("Maximum annual loss:", portfolio_losses.max())
  print("95th percentile loss:", p95)
  print("99th percentile loss:", p99)

  return (
      portfolio_losses,
      p95,
      p99,
      total_claims_per_year,
      policies_with_claims_per_year,
      average_claim_severities,
      largest_claims
    )


def compare_to_theoretical(portfolio_losses, num_policies, claim_rate, average_claim_cost):
  theoretical_mean = num_policies * claim_rate * average_claim_cost
  theoretical_variance = (
      num_policies
      * claim_rate
      * average_claim_cost**2
      * np.exp(1**2)
  )
  theoretical_std = np.sqrt(theoretical_variance)

  print("\n--- Theoretical vs. Simulated ---")
  print(f"Theoretical mean annual loss: ${theoretical_mean:,.2f}")
  print(f"Simulated mean annual loss:   ${portfolio_losses.mean():,.2f}")
  print(f"Theoretical standard deviation: ${theoretical_std:,.2f}")
  print(f"Simulated standard deviation:   ${portfolio_losses.std():,.2f}")



def analyze_frequency_and_severity(
      total_claims_per_year,
      policies_with_claims_per_year,
      average_claim_severities,
      largest_claims,
      num_policies,
      claim_rate,
      average_claim_cost,
  ):

    total_claims = total_claims_per_year.sum()

    # Estimate the average frequency of claims per policy-year
    estimated_claim_rate = (
        total_claims / (num_policies * len(total_claims_per_year))
    )

    # Weight each year's average severity by its number of claims
    estimated_average_severity = (
      np.sum(total_claims_per_year * average_claim_severities)
      / total_claims
      if total_claims > 0 else 0.0
    )

    print("\n--- Claim Frequency Analysis ---")
    print(f"Theoretical claim rate: {claim_rate:.3f}")
    print(f"Simulated claim rate:   {estimated_claim_rate:.3f}")
    print(f"Average claims per year: {total_claims_per_year.mean():.2f}")
    print(
      "Average policies with claims per year: "
      f"{policies_with_claims_per_year.mean():.2f}"
    )

    print("\n--- Claim Severity Analysis ---")
    print(f"Theoretical average claim severity: ${average_claim_cost:,.2f}")
    print(f"Simulated average claim severity:   ${estimated_average_severity:,.2f}")
    print(f"Average largest claim per year:     ${largest_claims.mean():,.2f}")
    print(f"Largest claim observed:             ${largest_claims.max():,.2f}")


def calculate_expected_portfolio_losses(num_policies, claim_rate, average_claim_cost):
  pure_premium = claim_rate * average_claim_cost
  portfolio_losses = num_policies * pure_premium

  print("\n--- Insurance Pricing ---")
  print(f"Pure premium per policy: ${pure_premium:,.2f}")
  print(f"Expected annual portfolio losses: ${portfolio_losses:,.2f}")


def calculate_gross_premium(risk_loading, num_policies, claim_rate, average_claim_cost):
  pure_premium = claim_rate * average_claim_cost
  gross_premium = pure_premium * (1 + risk_loading)

  print("\n--- Insurance Pricing ---")
  print(f"Pure premium per policy: ${pure_premium:,.2f}")
  print(f"Risk loading: {risk_loading:.0%}")
  print(f"Risk loading amount: ${gross_premium - pure_premium:,.2f}")
  print(f"Gross premium per policy: ${gross_premium:,.2f}")
  print(
    f"Expected portfolio premium revenue: "
    f"${gross_premium * num_policies:,.2f}")

  return gross_premium



