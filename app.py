import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

import simulation
from parameters import ModelParameters

# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
  page_title="RiskLab",
  page_icon="📊",
  layout="wide"
)

st.title("RiskLab")
st.subheader("Insurance Loss Modeling & Pricing Simulator")

st.write(
  "Explore insurance portfolio risk using Monte Carlo simulation. "
  "Adjust the model assumptions, run simulations, and compare "
  "different portfolio configurations."
)

# -------------------------------
# Sidebar: Model Parameters
# -------------------------------

st.sidebar.header("Model Parameters")

num_policies = st.sidebar.number_input(
  "Number of Policies",
  min_value=1,
  max_value=2000,
  value=1000,
  step=100
)

claim_rate = st.sidebar.slider(
  "Claim Frequency",
  min_value=0.0,
  max_value=1.0,
  value=0.3,
  step=0.05
)

average_claim_cost = st.sidebar.number_input(
  "Average Claim Severity ($)",
  min_value=1,
  max_value=10000,
  value=1000,
  step=100
)

severity_sigma = st.sidebar.slider(
  "Severity Volatility",
  min_value=0.1,
  max_value=2.0,
  value=1.0,
  step=0.1
)

risk_loading = st.sidebar.slider(
  "Risk Loading",
  min_value=0.0,
  max_value=1.0,
  value=0.2,
  step=0.05
)

num_simulations = st.sidebar.slider(
  "Number of Simulated Years",
  min_value=500,
  max_value=5000,
  value=3000,
  step=500
)

# -------------------------------
# Run Simulation
# -------------------------------

if st.button("Run Simulation", type="primary"):
  model_params = ModelParameters(
    num_policies=int(num_policies),
    claim_rate=claim_rate,
    average_claim_cost=average_claim_cost,
    severity_sigma=severity_sigma,
    risk_loading=risk_loading
  )

  with st.spinner("Running Monte Carlo simulations..."):
    results = simulation.monte_carlo_simulation(
      model_params,
      num_simulations=num_simulations
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

    # Calculate theoretical expected annual loss
    expected_loss = (
        num_policies
        * claim_rate
        * average_claim_cost
    )

    # Calculate theoretical standard deviation
    theoretical_variance = (
        num_policies
        * claim_rate
        * average_claim_cost ** 2
        * np.exp(severity_sigma ** 2)
    )

    theoretical_std = np.sqrt(theoretical_variance)

    # Calculate frequency and severity statistics
    total_claims = total_claims_per_year.sum()

    estimated_claim_rate = (
        total_claims
        / (num_policies * num_simulations)
    )

    estimated_average_severity = (
      np.sum(
        total_claims_per_year
        * average_claim_severities
      ) / total_claims
      if total_claims > 0 else 0
    )

    # Calculate premiums
    pure_premium = (
        claim_rate * average_claim_cost
    )

    gross_premium = simulation.calculate_gross_premium(
      model_params
    )

    # Save results so they remain visible after Streamlit reruns
    st.session_state["dashboard_results"] = {
      "portfolio_losses": portfolio_losses,
      "p95": p95,
      "p99": p99,
      "total_claims_per_year": total_claims_per_year,
      "policies_with_claims_per_year": policies_with_claims_per_year,
      "average_claim_severities": average_claim_severities,
      "largest_claims": largest_claims,
      "expected_loss": expected_loss,
      "theoretical_std": theoretical_std,
      "estimated_claim_rate": estimated_claim_rate,
      "estimated_average_severity": estimated_average_severity,
      "pure_premium": pure_premium,
      "gross_premium": gross_premium,
      "model_params": model_params,
      "num_simulations": num_simulations
    }

    # Run portfolio comparison
    portfolios = {
      "Standard": model_params,
      "High Frequency": model_params.with_updates(
        claim_rate=min(claim_rate + 0.2, 1.0)
      ),
      "High Severity": model_params.with_updates(
        average_claim_cost=average_claim_cost * 1.5
      )
    }

    comparison_results = simulation.compare_portfolios(
      portfolios,
      num_simulations=num_simulations
    )

    st.session_state["comparison_results"] = comparison_results

# -------------------------------
# Display Results
# -------------------------------

if "dashboard_results" in st.session_state:

  results = st.session_state["dashboard_results"]

  portfolio_losses = results["portfolio_losses"]

  st.divider()

  st.header("Simulation Results")

  st.caption(
    f"Based on {results['num_simulations']:,} simulated years"
  )

  # Key metrics
  col1, col2, col3, col4 = st.columns(4)

  col1.metric(
    "Expected Annual Loss",
    f"${results['expected_loss']:,.0f}"
  )

  col2.metric(
    "Simulated Average Loss",
    f"${portfolio_losses.mean():,.0f}"
  )

  col3.metric(
    "95th Percentile Loss",
    f"${results['p95']:,.0f}"
  )

  col4.metric(
    "99th Percentile Loss",
    f"${results['p99']:,.0f}"
  )

  # Loss Distribution
  st.subheader("Annual Loss Distribution")

  fig, ax = plt.subplots(figsize=(10, 5))

  ax.hist(
    portfolio_losses,
    bins=50,
    edgecolor="black"
  )

  ax.axvline(
    results["expected_loss"],
    linestyle="--",
    label="Expected Loss"
  )

  ax.axvline(
    results["p95"],
    linestyle="--",
    label="95th Percentile"
  )

  ax.axvline(
    results["p99"],
    linestyle="--",
    label="99th Percentile"
  )

  ax.set_xlabel("Annual Portfolio Loss ($)")
  ax.set_ylabel("Number of Simulated Years")
  ax.set_title("Distribution of Annual Insurance Losses")
  ax.legend()

  fig.tight_layout()

  st.pyplot(fig)
  plt.close(fig)

  # Frequency and Severity
  st.subheader("Frequency and Severity Analysis")

  col1, col2, col3 = st.columns(3)

  col1.metric(
    "Estimated Claim Rate",
    f"{results['estimated_claim_rate']:.3f}"
  )

  col2.metric(
    "Average Claim Severity",
    f"${results['estimated_average_severity']:,.2f}"
  )

  col3.metric(
    "Average Claims Per Year",
    f"{results['total_claims_per_year'].mean():,.1f}"
  )

  # Theoretical vs Simulated
  st.subheader("Model Validation")

  col1, col2 = st.columns(2)

  col1.metric(
    "Theoretical Standard Deviation",
    f"${results['theoretical_std']:,.2f}"
  )

  col2.metric(
    "Simulated Standard Deviation",
    f"${portfolio_losses.std():,.2f}"
  )

  # Pricing
  st.subheader("Insurance Pricing")

  col1, col2 = st.columns(2)

  col1.metric(
    "Pure Premium Per Policy",
    f"${results['pure_premium']:,.2f}"
  )

  col2.metric(
    "Gross Premium Per Policy",
    f"${results['gross_premium']:,.2f}"
  )

  st.caption(
    "Gross premium includes the selected risk loading."
  )

  # Portfolio Comparison
  st.divider()

  st.header("Portfolio Comparison")

  comparison_results = st.session_state["comparison_results"]

  for name, comparison in comparison_results.items():
    st.write(f"**{name} Portfolio**")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
      "Expected Loss",
      f"${comparison['expected_loss']:,.0f}"
    )

    col2.metric(
      "Simulated Mean",
      f"${comparison['simulated_mean']:,.0f}"
    )

    col3.metric(
      "P95 Loss",
      f"${comparison['p95']:,.0f}"
    )

    col4.metric(
      "P99 Loss",
      f"${comparison['p99']:,.0f}"
    )

  # Comparison Chart
  st.subheader("Comparing Portfolio Risk")

  portfolio_names = list(comparison_results.keys())

  p95_values = [
    result["p95"]
    for result in comparison_results.values()
  ]

  p99_values = [
    result["p99"]
    for result in comparison_results.values()
  ]

  x = np.arange(len(portfolio_names))
  width = 0.35

  fig, ax = plt.subplots(figsize=(10, 5))

  ax.bar(
    x - width / 2,
    p95_values,
    width,
    label="95th Percentile"
  )

  ax.bar(
    x + width / 2,
    p99_values,
    width,
    label="99th Percentile"
  )

  ax.set_xticks(x)
  ax.set_xticklabels(portfolio_names)
  ax.set_ylabel("Annual Portfolio Loss ($)")
  ax.set_title("Portfolio Tail Risk Comparison")
  ax.legend()

  fig.tight_layout()

  st.pyplot(fig)
  plt.close(fig)

else:

  st.info(
    "Adjust the model parameters in the sidebar and "
    "click Run Simulation to get started."
  )
