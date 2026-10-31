import numpy as np

NUM_POLICIES = 1000
CLAIM_RATE = 0.3
AVERAGE_CLAIM_COST = 1000


np.random.seed(42)

def simulate_portfolio():
  claims = np.random.poisson(CLAIM_RATE, NUM_POLICIES)

  severity_sigma = 1.0
  severity_mu = np.log(AVERAGE_CLAIM_COST) - severity_sigma ** 2 / 2

  claim_costs = np.random.lognormal(
    mean=severity_mu,
    sigma=severity_sigma,
    size=int(claims.sum())
  )

  policy_losses = np.zeros(NUM_POLICIES)
  claim_index = 0

  for i in range(NUM_POLICIES):
    num_claims = claims[i]

    policy_losses[i] = claim_costs[
      claim_index:claim_index + num_claims
    ].sum()

    claim_index += num_claims

  return {
    "total_claims": int(claims.sum()),
    "total_losses": float(policy_losses.sum()),
    "average_loss": float(policy_losses.mean()),
    "largest_policy_loss": float(policy_losses.max())
  }


def monte_carlo_simulation():
  num_simulations = 10000

  portfolio_losses = np.zeros(num_simulations)
  for i in range(num_simulations):
    portfolio_losses[i] = simulate_portfolio()["total_losses"]

  p95 = np.percentile(portfolio_losses, 95)
  p99 = np.percentile(portfolio_losses, 99)

  print(f"Number of simulated years:", num_simulations)
  print(f"Average annual loss: ${portfolio_losses.mean():,.2f}")
  print("Median annual loss:", np.median(portfolio_losses))
  print("Minimum annual loss:", portfolio_losses.min())
  print("Maximum annual loss:", portfolio_losses.max())
  print("95th percentile loss:", p95)
  print("99th percentile loss:", p99)

  return portfolio_losses, p95, p99


def compare_to_theoretical(portfolio_losses):
  theoretical_mean = NUM_POLICIES * CLAIM_RATE * AVERAGE_CLAIM_COST
  theoretical_variance = (
      NUM_POLICIES
      * CLAIM_RATE
      * AVERAGE_CLAIM_COST**2
      * np.exp(1**2)
  )
  theoretical_std = np.sqrt(theoretical_variance)

  print("\n--- Theoretical vs. Simulated ---")
  print(f"Theoretical mean annual loss: ${theoretical_mean:,.2f}")
  print(f"Simulated mean annual loss:   ${portfolio_losses.mean():,.2f}")
  print(f"Theoretical standard deviation: ${theoretical_std:,.2f}")
  print(f"Simulated standard deviation:   ${portfolio_losses.std():,.2f}")