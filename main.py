import simulation

if __name__ == '__main__':
    claims = simulation.generate_claims()
    severity = simulation.generate_severity(claims)
    policy_losses = simulation.calculate_losses(claims, severity)


