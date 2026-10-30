import simulation
from simulation import monte_carlo_simulation, compare_to_theoretical

if __name__ == '__main__':
    losses = monte_carlo_simulation()
    compare_to_theoretical(losses)

