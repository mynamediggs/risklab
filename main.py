import simulation
import model
import parameters


if __name__ == '__main__':
    # Initialize model parameters
    parameters = parameters.ModelParameters()

    # Run Monte Carlo simulation
    (
        portfolio_losses,
        p95,
        p99,
        total_claims_per_year,
        policies_with_claims_per_year,
        average_claim_severities,
        largest_claims
    ) = simulation.monte_carlo_simulation(parameters)

    model.plot_loss_distribution(portfolio_losses, p95, p99)

    simulation.analyze_frequency_and_severity(total_claims_per_year,
                                              policies_with_claims_per_year,
                                              average_claim_severities,
                                              largest_claims,
                                              parameters)

    gross_premium = simulation.calculate_gross_premium(parameters)
    expected_losses = simulation.calculate_expected_portfolio_losses(parameters)
    sensitivity_results = simulation.run_sensitivity_analysis()
    model.plot_sensitivity_analysis(sensitivity_results)