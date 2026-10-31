import simulation
import model


if __name__ == '__main__':
    losses, p95, p99 = simulation.monte_carlo_simulation()
    model.plot_loss_distribution(losses, p95, p99)


