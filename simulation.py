import numpy as np

np.random.seed(42)
NUM_POLICIES = 1000
CLAIM_RATE = 0.3

def generate_claims():
  claims = np.random.poisson(CLAIM_RATE, NUM_POLICIES)

  print("Claims generated\n")

  print("First 10 policies: [", end="")
  for i in range(10):
    print(f"{claims[i]}, ", end="")
  print("...]")
  print("Total claims:", claims.sum())
  print("Expected claims:", NUM_POLICIES * CLAIM_RATE)
  print()
  return claims


def generate_severity(claims):
  average_claim_cost = 1000
  severity_sigma = 1.0

  severity_mu = np.log(average_claim_cost) - (severity_sigma ** 2 / 2)

  # lognormal takes mean and standard deviation of the underlying normal distribution
  severity = np.random.lognormal(
      severity_mu,
      severity_sigma,
      int(claims.sum()))

  print("Severity generated\n")

  print("First 10 claim costs: [", end="")
  for i in range(10):
    print(f"{round(severity[i], 3)}, ", end="")
  print("...]")
  print("Total claim costs:", round(severity.sum(), 3))
  print("Average claim cost:", round(severity.mean(), 3))
  print()
  return severity


def calculate_losses(claims, severity):
  policy_losses = np.zeros(NUM_POLICIES)

  index = 0

  for i, count in enumerate(claims):
    if count > 0:
      policy_losses[i] = severity[index:index + count].sum()
      index += count

  print("Losses generated\n")
  print("Total portfolio losses:", round(policy_losses.sum(), 3))
  print("Average loss per policy:", round(policy_losses.mean(), 3))
  print("Largest individual policy loss:", round(policy_losses.max(), 3))
  print()
  return policy_losses