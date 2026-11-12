
import numpy as np
import pytest

import simulation
from parameters import ModelParameters


# -------------------------------
# Model Parameter Tests
# -------------------------------

def test_default_parameters():
    params = ModelParameters()

    assert params.num_policies == 1000
    assert params.claim_rate == 0.3
    assert params.average_claim_cost == 1000
    assert params.severity_sigma == 1.0
    assert params.risk_loading == 0.2


@pytest.mark.parametrize(
    "parameter",
    [
        {"num_policies": 0},
        {"claim_rate": -0.1},
        {"average_claim_cost": 0},
        {"severity_sigma": 0},
        {"risk_loading": -0.1}
    ]
)
def test_invalid_parameters(parameter):
    with pytest.raises(ValueError):
        ModelParameters(**parameter)


def test_with_updates():
    params = ModelParameters()

    updated_params = params.with_updates(claim_rate=0.5)

    assert updated_params.claim_rate == 0.5

    # Original parameters should remain unchanged
    assert params.claim_rate == 0.3


# -------------------------------
# Simulation Tests
# -------------------------------

def test_simulate_portfolio():
    params = ModelParameters(
        num_policies=2,
        claim_rate=0.2,
        average_claim_cost=100,
        severity_sigma=0.5
    )

    # Control the random results so this test is predictable
    monkeypatch = pytest.MonkeyPatch()

    monkeypatch.setattr(
        simulation.np.random,
        "poisson",
        lambda rate, size: np.array([1, 0])
    )

    monkeypatch.setattr(
        simulation.np.random,
        "lognormal",
        lambda mean, sigma, size: np.array([100.0])
    )

    try:
        results = simulation.simulate_portfolio(params)
    finally:
        monkeypatch.undo()

    assert results["total_claims"] == 1
    assert results["total_losses"] == 100.0
    assert results["average_loss"] == 50.0
    assert results["largest_policy_loss"] == 100.0
    assert results["average_claim_severity"] == 100.0
    assert results["largest_claim"] == 100.0


def test_zero_claim_rate():
    params = ModelParameters(claim_rate=0)

    results = simulation.simulate_portfolio(params)

    assert results["total_claims"] == 0
    assert results["total_losses"] == 0
    assert results["average_claim_severity"] == 0


# -------------------------------
# Pricing Tests
# -------------------------------

def test_expected_portfolio_losses():
    params = ModelParameters(
        num_policies=1000,
        claim_rate=0.3,
        average_claim_cost=1000
    )

    expected_losses = simulation.calculate_expected_portfolio_losses(
        params
    )

    assert expected_losses == 300000


def test_gross_premium():
    params = ModelParameters(
        claim_rate=0.3,
        average_claim_cost=1000,
        risk_loading=0.2
    )

    gross_premium = simulation.calculate_gross_premium(params)

    assert gross_premium == 360


# -------------------------------
# Portfolio Comparison Tests
# -------------------------------

def test_compare_portfolios():
    portfolios = {
        "Standard": ModelParameters(),
        "High Frequency": ModelParameters(claim_rate=0.5),
        "High Severity": ModelParameters(average_claim_cost=1500)
    }

    results = simulation.compare_portfolios(
        portfolios,
        num_simulations=100
    )

    assert len(results) == 3

    assert results["Standard"]["expected_loss"] == 300000
    assert results["High Frequency"]["expected_loss"] == 500000
    assert results["High Severity"]["expected_loss"] == 450000

    for portfolio_results in results.values():
        assert portfolio_results["p99"] >= portfolio_results["p95"]
        assert portfolio_results["simulated_std"] >= 0


def test_monte_carlo_simulation():
    params = ModelParameters(
        num_policies=100,
        claim_rate=0.3,
        average_claim_cost=1000
    )

    results = simulation.monte_carlo_simulation(
        params,
        num_simulations=100
    )

    (
        portfolio_losses,
        p95,
        p99,
        total_claims_per_year,
        policies_with_claims_per_year,
        average_claim_severities,
        largest_claims
    ) = results

    assert len(portfolio_losses) == 100
    assert len(total_claims_per_year) == 100
    assert len(policies_with_claims_per_year) == 100
    assert len(average_claim_severities) == 100
    assert len(largest_claims) == 100

    assert np.all(portfolio_losses >= 0)
    assert np.all(total_claims_per_year >= 0)
    assert p99 >= p95
