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

def plot_sensitivity_analysis(results):
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Claim frequency
    axes[0].plot(
        results["claim_rates"],
        results["frequency_premiums"],
        marker="o"
    )
    axes[0].set_title("Effect of Claim Frequency")
    axes[0].set_xlabel("Claim Rate")
    axes[0].set_ylabel("Gross Premium ($)")
    axes[0].grid(True)

    # Claim severity
    axes[1].plot(
        results["claim_costs"],
        results["severity_premiums"],
        marker="o"
    )
    axes[1].set_title("Effect of Claim Severity")
    axes[1].set_xlabel("Average Claim Severity ($)")
    axes[1].set_ylabel("Gross Premium ($)")
    axes[1].grid(True)

    # Risk loading
    axes[2].plot(
        results["risk_loadings"],
        results["loading_premiums"],
        marker="o"
    )
    axes[2].set_title("Effect of Risk Loading")
    axes[2].set_xlabel("Risk Loading")
    axes[2].set_ylabel("Gross Premium ($)")
    axes[2].grid(True)

    plt.tight_layout()
    plt.show()