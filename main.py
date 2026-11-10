import simulation
import model
import parameters


standard_portfolio = parameters.ModelParameters(
    claim_rate=0.3,
    average_claim_cost=1000,
    risk_loading=0.2
)

high_frequency_portfolio = parameters.ModelParameters(
    claim_rate=0.5,
    average_claim_cost=1000,
    risk_loading=0.2
)

high_severity_portfolio = parameters.ModelParameters(
    claim_rate=0.3,
    average_claim_cost=1500,
    risk_loading=0.2
)


if __name__ == '__main__':
    # Initialize model parameters
    model_parameters = parameters.ModelParameters()

    # Run Monte Carlo simulation
    (
        portfolio_losses,
        p95,
        p99,
        total_claims_per_year,
        policies_with_claims_per_year,
        average_claim_severities,
        largest_claims
    ) = simulation.monte_carlo_simulation(model_parameters)

    model.plot_loss_distribution(portfolio_losses, p95, p99)

    simulation.analyze_frequency_and_severity(total_claims_per_year,
                                              policies_with_claims_per_year,
                                              average_claim_severities,
                                              largest_claims,
                                              model_parameters)

    gross_premium = simulation.calculate_gross_premium(model_parameters)
    expected_losses = simulation.calculate_expected_portfolio_losses(model_parameters)
    sensitivity_results = simulation.run_sensitivity_analysis()
    model.plot_sensitivity_analysis(sensitivity_results)