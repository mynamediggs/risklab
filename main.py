import simulation
import model

from parameters import (
  CLAIM_RATE,
  NUM_POLICIES,
  AVERAGE_CLAIM_COST,
  RISK_LOADING,
)


if __name__ == '__main__':
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
    simulation.calculate_expected_portfolio_losses()

    pure_premium = CLAIM_RATE * AVERAGE_CLAIM_COST
    gross_premium = simulation.calculate_gross_premium()


