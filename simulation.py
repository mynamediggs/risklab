import numpy as np
np.random.seed(42)




def simulate_portfolio(model_params):
    claims = np.random.poisson(
        model_params.claim_rate,
        model_params.num_policies
    )

    severity_sigma = model_params.severity_sigma
    severity_mu = (
        np.log(model_params.average_claim_cost)
        - severity_sigma ** 2 / 2
    )

    claim_costs = np.random.lognormal(
        mean=severity_mu,
        sigma=severity_sigma,
        size=int(claims.sum())
    )

    # Associate each claim with its policy
    policy_indices = np.repeat(
        np.arange(model_params.num_policies),
        claims
    )

    # Calculate total losses for each policy
    policy_losses = np.bincount(
        policy_indices,
        weights=claim_costs,
        minlength=model_params.num_policies
    )

    return {
        "total_claims": int(claims.sum()),
        "total_losses": float(policy_losses.sum()),
        "average_loss": float(policy_losses.mean()),
        "largest_policy_loss": float(policy_losses.max()),
        "policies_with_claims": int(np.count_nonzero(claims)),
        "average_claim_severity": (
            float(claim_costs.mean())
            if claim_costs.size > 0 else 0.0
        ),
        "largest_claim": (
            float(claim_costs.max())
            if claim_costs.size > 0 else 0.0
        )
    }





def monte_carlo_simulation(model_params, num_simulations=10000):
    if num_simulations <= 0:
        raise ValueError("Number of simulations must be positive.")

    # Generate claim counts for every policy in every simulated year
    claims = np.random.poisson(
        model_params.claim_rate,
        size=(num_simulations, model_params.num_policies)
    )

    # Calculate total claims for each year
    total_claims_per_year = claims.sum(axis=1)

    # Generate all claim severities
    severity_sigma = model_params.severity_sigma
    severity_mu = (
        np.log(model_params.average_claim_cost)
        - severity_sigma ** 2 / 2
    )

    claim_costs = np.random.lognormal(
        mean=severity_mu,
        sigma=severity_sigma,
        size=int(total_claims_per_year.sum())
    )

    # Associate every claim with its simulated year
    year_indices = np.repeat(
        np.arange(num_simulations),
        total_claims_per_year
    )

    # Calculate total portfolio losses for each year
    portfolio_losses = np.bincount(
        year_indices,
        weights=claim_costs,
        minlength=num_simulations
    )

    # Calculate number of policies with claims per year
    policies_with_claims_per_year = np.count_nonzero(
        claims,
        axis=1
    )

    # Average claim severity for each year
    total_severity_per_year = portfolio_losses

    average_claim_severities = np.divide(
        total_severity_per_year,
        total_claims_per_year,
        out=np.zeros(num_simulations, dtype=float),
        where=total_claims_per_year > 0
    )

    # Calculate largest claim for each year
    largest_claims = np.zeros(num_simulations)

    np.maximum.at(
        largest_claims,
        year_indices,
        claim_costs
    )

    # Calculate risk percentiles
    p95 = float(np.percentile(portfolio_losses, 95))
    p99 = float(np.percentile(portfolio_losses, 99))

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

def compare_portfolios(portfolios, num_simulations=3000):
  comparison_results = {}

  for name, model_params in portfolios.items():
    annual_losses = np.zeros(num_simulations)

    # Simulate the portfolio over multiple years
    for i in range(num_simulations):
      results = simulate_portfolio(model_params)
      annual_losses[i] = results["total_losses"]

    # Calculate theoretical expected annual losses
    pure_premium = (
        model_params.claim_rate
        * model_params.average_claim_cost
    )

    expected_loss = model_params.num_policies * pure_premium

    # Store portfolio statistics
    comparison_results[name] = {
      "expected_loss": expected_loss,
      "simulated_mean": float(annual_losses.mean()),
      "simulated_std": float(annual_losses.std()),
      "p95": float(np.percentile(annual_losses, 95)),
      "p99": float(np.percentile(annual_losses, 99)),
      "pure_premium": pure_premium,
      "gross_premium": calculate_gross_premium(model_params)
    }

  return comparison_results


def print_portfolio_comparison(comparison_results):
  print("\n--- Portfolio Comparison ---")

  for name, results in comparison_results.items():
    print(f"\n{name} Portfolio")
    print("-" * 40)

    print(f"Expected Annual Loss: ${results['expected_loss']:,.2f}")
    print(f"Simulated Average Loss: ${results['simulated_mean']:,.2f}")
    print(f"Standard Deviation: ${results['simulated_std']:,.2f}")
    print(f"95th Percentile Loss: ${results['p95']:,.2f}")
    print(f"99th Percentile Loss: ${results['p99']:,.2f}")

    print(f"Pure Premium (per policy): ${results['pure_premium']:,.2f}")
    print(f"Gross Premium (per policy): ${results['gross_premium']:,.2f}")
