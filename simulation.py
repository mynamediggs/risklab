import numpy as np
np.random.seed(42)



def simulate_portfolio(model_params):
  claims = np.random.poisson(model_params.claim_rate, model_params.num_policies)

  severity_sigma = 1.0
  severity_mu = np.log(model_params.average_claim_cost) - severity_sigma ** 2 / 2

  claim_costs = np.random.lognormal(
    mean=severity_mu,
    sigma=severity_sigma,
    size=int(claims.sum())
  )

  policy_losses = np.zeros(model_params.num_policies)
  claim_index = 0

  for i in range(model_params.num_policies):
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



def monte_carlo_simulation(model_params):
  num_simulations = 10000

  total_claims_per_year = np.zeros(num_simulations)
  policies_with_claims_per_year = np.zeros(num_simulations)
  average_claim_severities = np.zeros(num_simulations)
  largest_claims = np.zeros(num_simulations)
  portfolio_losses = np.zeros(num_simulations)

  for i in range(num_simulations):
    results = simulate_portfolio(model_params)

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



def compare_to_theoretical(portfolio_losses, model_params):
  theoretical_mean = model_params.num_policies * model_params.claim_rate * model_params.average_claim_cost
  theoretical_variance = (
      model_params.num_policies
      * model_params.claim_rate
      * model_params.average_claim_cost ** 2
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
      model_params
  ):

    total_claims = total_claims_per_year.sum()

    # Estimate the average frequency of claims per policy-year
    estimated_claim_rate = (
        total_claims / (model_params.num_policies * len(total_claims_per_year))
    )

    # Weight each year's average severity by its number of claims
    estimated_average_severity = (
      np.sum(total_claims_per_year * average_claim_severities)
      / total_claims
      if total_claims > 0 else 0.0
    )

    print("\n--- Claim Frequency Analysis ---")
    print(f"Theoretical claim rate: {model_params.claim_rate:.3f}")
    print(f"Simulated claim rate:   {estimated_claim_rate:.3f}")
    print(f"Average claims per year: {total_claims_per_year.mean():.2f}")
    print(
      "Average policies with claims per year: "
      f"{policies_with_claims_per_year.mean():.2f}"
    )

    print("\n--- Claim Severity Analysis ---")
    print(f"Theoretical average claim severity: ${model_params.average_claim_cost:,.2f}")
    print(f"Simulated average claim severity:   ${estimated_average_severity:,.2f}")
    print(f"Average largest claim per year:     ${largest_claims.mean():,.2f}")
    print(f"Largest claim observed:             ${largest_claims.max():,.2f}")



def calculate_expected_portfolio_losses(model_params):
  pure_premium = model_params.claim_rate * model_params.average_claim_cost
  portfolio_losses = model_params.num_policies * pure_premium

  print("\n--- Insurance Pricing ---")
  print(f"Pure premium per policy: ${pure_premium:,.2f}")
  print(f"Expected annual portfolio losses: ${portfolio_losses:,.2f}")



def calculate_gross_premium(model_params):
  pure_premium = model_params.claim_rate * model_params.average_claim_cost
  gross_premium = pure_premium * (1 + model_params.risk_loading)

  print("\n--- Insurance Pricing ---")
  print(f"Pure premium per policy: ${pure_premium:,.2f}")
  print(f"Risk loading: {model_params.risk_loading:.0%}")
  print(f"Risk loading amount: ${gross_premium - pure_premium:,.2f}")
  print(f"Gross premium per policy: ${gross_premium:,.2f}")
  print(
    f"Expected portfolio premium revenue: "
    f"${gross_premium * model_params.num_policies:,.2f}")

  return gross_premium

from parameters import ModelParameters


def run_sensitivity_analysis():
    base_parameters = ModelParameters()

    claim_rates = [0.2, 0.3, 0.4, 0.5, 0.6]
    claim_costs = [800, 900, 1000, 1100, 1200]
    risk_loadings = [0.0, 0.1, 0.2, 0.3, 0.4]

    frequency_premiums = []
    severity_premiums = []
    loading_premiums = []

    # Test different claim frequencies
    for rate in claim_rates:
        parameters = ModelParameters(
            num_policies=base_parameters.num_policies,
            claim_rate=rate,
            average_claim_cost=base_parameters.average_claim_cost,
            severity_sigma=base_parameters.severity_sigma,
            risk_loading=base_parameters.risk_loading
        )

        frequency_premiums.append(
            calculate_gross_premium(parameters)
        )

    # Test different claim severities
    for cost in claim_costs:
        parameters = ModelParameters(
            num_policies=base_parameters.num_policies,
            claim_rate=base_parameters.claim_rate,
            average_claim_cost=cost,
            severity_sigma=base_parameters.severity_sigma,
            risk_loading=base_parameters.risk_loading
        )

        severity_premiums.append(
            calculate_gross_premium(parameters)
        )

    # Test different risk loadings
    for loading in risk_loadings:
        parameters = ModelParameters(
            num_policies=base_parameters.num_policies,
            claim_rate=base_parameters.claim_rate,
            average_claim_cost=base_parameters.average_claim_cost,
            severity_sigma=base_parameters.severity_sigma,
            risk_loading=loading
        )

        loading_premiums.append(
            calculate_gross_premium(parameters)
        )

    return {
        "claim_rates": claim_rates,
        "frequency_premiums": frequency_premiums,
        "claim_costs": claim_costs,
        "severity_premiums": severity_premiums,
        "risk_loadings": risk_loadings,
        "loading_premiums": loading_premiums
    }
