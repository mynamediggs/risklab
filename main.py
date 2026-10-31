import simulation
import model


if __name__ == '__main__':
    (
        portfolio_losses,
        p95,
        p99,
        total_claims_per_year,
        policies_with_claims_per_year,
        average_claim_severities,
        largest_claims
    ) = simulation.monte_carlo_simulation()

    # model.plot_loss_distribution(portfolio_losses, p95, p99)

    simulation.analyze_frequency_and_severity(
        total_claims_per_year,
        policies_with_claims_per_year,
        average_claim_severities,
        largest_claims
    )


