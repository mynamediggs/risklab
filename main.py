import simulation
import model
from parameters import ModelParameters


standard_portfolio = ModelParameters(
    claim_rate=0.3,
    average_claim_cost=1000,
    risk_loading=0.2
)

high_frequency_portfolio = ModelParameters(
    claim_rate=0.5,
    average_claim_cost=1000,
    risk_loading=0.2
)

high_severity_portfolio = ModelParameters(
    claim_rate=0.3,
    average_claim_cost=1500,
    risk_loading=0.2
)

portfolios = {
    "Standard": standard_portfolio,
    "High Frequency": high_frequency_portfolio,
    "High Severity": high_severity_portfolio
}


if __name__ == '__main__':
    model_params = ModelParameters()

    # Run Monte Carlo simulation
    (
        portfolio_losses,
        p95,
        p99,
        total_claims_per_year,
        policies_with_claims_per_year,
        average_claim_severities,
        largest_claims
    ) = simulation.monte_carlo_simulation(model_params)

    model.plot_loss_distribution(portfolio_losses, p95, p99)

    simulation.analyze_frequency_and_severity(total_claims_per_year,
                                              policies_with_claims_per_year,
                                              average_claim_severities,
                                              largest_claims,
                                              model_params)

    gross_premium = simulation.calculate_gross_premium(model_params)
    expected_losses = simulation.calculate_expected_portfolio_losses(model_params)
    sensitivity_results = simulation.run_sensitivity_analysis()
    model.plot_sensitivity_analysis(sensitivity_results)

    portfolios = {
        "Standard": model_params,
        "High Frequency": model_params.with_updates(claim_rate=0.5),
        "High Severity": model_params.with_updates(average_claim_cost=1500)
    }

    comparison_results = simulation.compare_portfolios(portfolios)
    simulation.print_portfolio_comparison(comparison_results)
    model.plot_portfolio_comparison(comparison_results)


