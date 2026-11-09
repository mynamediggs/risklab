import simulation
import model
import parameters


if __name__ == '__main__':
    parameters = parameters.ModelParameters()
    # (
    #     portfolio_losses,
    #     p95,
    #     p99,
    #     total_claims_per_year,
    #     policies_with_claims_per_year,
    #     average_claim_severities,
    #     largest_claims
    # ) = simulation.monte_carlo_simulation()



    # simulation.analyze_frequency_and_severity(
    #     total_claims_per_year,
    #     policies_with_claims_per_year,
    #     average_claim_severities,
    #     largest_claims
    # )

    # model.plot_loss_distribution(portfolio_losses, p95, p99)
    simulation.calculate_expected_portfolio_losses(parameters)
    gross_premium = simulation.calculate_gross_premium(parameters)


