import numpy as np
np.random.seed(42)



def simulate_portfolio(model_params):
  claims = np.random.poisson(model_params.claim_rate, model_params.num_policies)

  severity_sigma = model_params.severity_sigma
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
  theoretical_mean = (
      model_params.num_policies
      * model_params.claim_rate
      * model_params.average_claim_cost
  )

  theoretical_variance = (
      model_params.num_policies
      * model_params.claim_rate
      * model_params.average_claim_cost ** 2
      * np.exp(model_params.severity_sigma ** 2)
  )

  theoretical_std = np.sqrt(theoretical_variance)

  return {
    "theoretical_mean": theoretical_mean,
    "simulated_mean": float(portfolio_losses.mean()),
    "theoretical_std": theoretical_std,
    "simulated_std": float(portfolio_losses.std())
  }



def analyze_frequency_and_severity(
    total_claims_per_year,
    policies_with_claims_per_year,
    average_claim_severities,
    largest_claims,
    model_params
  ):

  total_claims = total_claims_per_year.sum()

  estimated_claim_rate = (
      total_claims
      / (model_params.num_policies * len(total_claims_per_year))
  )

  estimated_average_severity = (
    np.sum(total_claims_per_year * average_claim_severities)
    / total_claims
    if total_claims > 0 else 0.0
  )

  return {
    "theoretical_claim_rate": model_params.claim_rate,
    "simulated_claim_rate": estimated_claim_rate,
    "average_claims_per_year": float(total_claims_per_year.mean()),
    "average_policies_with_claims": float(
      policies_with_claims_per_year.mean()
    ),
    "theoretical_average_severity": model_params.average_claim_cost,
    "simulated_average_severity": estimated_average_severity,
    "average_largest_claim": float(largest_claims.mean()),
    "largest_claim_observed": float(largest_claims.max())
  }



def calculate_expected_portfolio_losses(model_params):
  pure_premium = model_params.claim_rate * model_params.average_claim_cost
  portfolio_losses = model_params.num_policies * pure_premium

  # print("\n--- Insurance Pricing ---")
  # print(f"Pure premium per policy: ${pure_premium:,.2f}")
  # print(f"Expected annual portfolio losses: ${portfolio_losses:,.2f}")

  return portfolio_losses



def calculate_gross_premium(model_params):
  pure_premium = model_params.claim_rate * model_params.average_claim_cost
  gross_premium = pure_premium * (1 + model_params.risk_loading)
  #
  # print("\n--- Insurance Pricing ---")
  # print(f"Pure premium per policy: ${pure_premium:,.2f}")
  # print(f"Risk loading: {model_params.risk_loading:.0%}")
  # print(f"Risk loading amount: ${gross_premium - pure_premium:,.2f}")
  # print(f"Gross premium per policy: ${gross_premium:,.2f}")
  # print(
  #   f"Expected portfolio premium revenue: "
  #   f"${gross_premium * model_params.num_policies:,.2f}")

  return gross_premium

from parameters import ModelParameters



def run_sensitivity_analysis():
  base_parameters = ModelParameters()

  claim_rates = [0.2, 0.3, 0.4, 0.5, 0.6]
  claim_costs = [800, 900, 1000, 1100, 1200]
  risk_loadings = [0.0, 0.1, 0.2, 0.3, 0.4]

  frequency_premiums = [
    calculate_gross_premium(
      base_parameters.with_updates(claim_rate=rate)
    )
    for rate in claim_rates
  ]

  severity_premiums = [
    calculate_gross_premium(
      base_parameters.with_updates(average_claim_cost=cost)
    )
    for cost in claim_costs
  ]

  loading_premiums = [
    calculate_gross_premium(
      base_parameters.with_updates(risk_loading=loading)
    )
    for loading in risk_loadings
  ]

  return {
    "claim_rates": claim_rates,
    "frequency_premiums": frequency_premiums,
    "claim_costs": claim_costs,
    "severity_premiums": severity_premiums,
    "risk_loadings": risk_loadings,
    "loading_premiums": loading_premiums
  }


