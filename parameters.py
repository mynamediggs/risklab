class ModelParameters:

  def __init__(
      self,
      num_policies=1000,
      claim_rate=0.3,
      average_claim_cost=1000,
      severity_sigma=1.0,
      risk_loading=0.2
  ):
    if num_policies <= 0:
      raise ValueError("Number of policies must be positive.")

    if claim_rate < 0:
      raise ValueError("Claim rate cannot be negative.")

    if average_claim_cost <= 0:
      raise ValueError("Average claim cost must be positive.")

    if severity_sigma <= 0:
      raise ValueError("Severity sigma must be positive.")

    if risk_loading < 0:
      raise ValueError("Risk loading cannot be negative.")

    self.num_policies = num_policies
    self.claim_rate = claim_rate
    self.average_claim_cost = average_claim_cost
    self.severity_sigma = severity_sigma
    self.risk_loading = risk_loading

  def with_updates(self, **updates):
    values = {
      "num_policies": self.num_policies,
      "claim_rate": self.claim_rate,
      "average_claim_cost": self.average_claim_cost,
      "severity_sigma": self.severity_sigma,
      "risk_loading": self.risk_loading
    }

    values.update(updates)

    return ModelParameters(**values)