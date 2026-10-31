import matplotlib.pyplot as plt


def plot_loss_distribution(portfolio_losses, p95, p99):
    plt.figure(figsize=(10, 6))

    plt.hist(
        portfolio_losses,
        bins=50,
        edgecolor="black"
    )

    plt.axvline(
        p95,
        linestyle="--",
        label=f"95th percentile: ${p95:,.0f}"
    )

    plt.axvline(
        p99,
        linestyle="--",
        label=f"99th percentile: ${p99:,.0f}"
    )

    plt.title("Distribution of Annual Insurance Losses")
    plt.xlabel("Total Annual Loss ($)")
    plt.ylabel("Number of Simulated Years")

    plt.legend()
    plt.tight_layout()
    plt.show()