import numpy as np
import pytest
import simulation

def test_single_year_results_are_valid():
  results = simulation.simulate_portfolio()

  # Check that all expected results are present
  assert "total_claims" in results
  assert "total_losses" in results
  assert "average_loss" in results
  assert "largest_policy_loss" in results
  assert "policies_with_claims" in results

  # Counts must be nonnegative
  assert results["total_claims"] >= 0
  assert results["policies_with_claims"] >= 0
  assert results["policies_with_claims"] <= simulation.NUM_POLICIES

  # There cannot be more policies with claims than total claims
  assert results["total_claims"] >= results["policies_with_claims"]

  # Losses cannot be negative
  assert results["total_losses"] >= 0
  assert results["average_loss"] >= 0
  assert results["largest_policy_loss"] >= 0

  # Average loss should equal total losses divided by policies
  assert results["average_loss"] == pytest.approx(
    results["total_losses"] / simulation.NUM_POLICIES
  )

  # The largest policy loss cannot exceed total portfolio losses
  assert results["largest_policy_loss"] <= results["total_losses"]

def test_simulated_mean_matches_theory():
    np.random.seed(12345)

    num_simulations = 3000
    annual_losses = np.array([
      simulation.simulate_portfolio()["total_losses"]
      for _ in range(num_simulations)
    ])

    theoretical_mean = (
        simulation.NUM_POLICIES *
        simulation.CLAIM_RATE *
        simulation.AVERAGE_CLAIM_COST
    )

    # Allow a 2% relative tolerance for Monte Carlo sampling variation
    assert annual_losses.mean() == pytest.approx(
      theoretical_mean,
      rel=0.02
    )


def test_simulated_standard_deviation_matches_theory():
  np.random.seed(12345)

  num_simulations = 3000
  annual_losses = np.array([
    simulation.simulate_portfolio()["total_losses"]
    for _ in range(num_simulations)
  ])

  severity_sigma = 1.0

  theoretical_variance = (
      simulation.NUM_POLICIES
      * simulation.CLAIM_RATE
      * simulation.AVERAGE_CLAIM_COST ** 2
      * np.exp(severity_sigma ** 2)
  )

  theoretical_std = np.sqrt(theoretical_variance)

  # Allow a 10% relative tolerance for the estimated standard deviation
  assert annual_losses.std() == pytest.approx(
    theoretical_std,
    rel=0.10
  )