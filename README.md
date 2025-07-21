# QuLab: Risk Governance Lab 1

![QuLab Logo](https://www.quantuniversity.com/assets/img/logo5.jpg)

## Project Title and Description

**QuLab: Risk Governance Lab 1** is an interactive Streamlit application designed to simulate risk management strategies and visualize their impact within a firm's defined risk appetite. This application serves as a practical lab environment for exploring key concepts in risk governance, allowing users to define risk thresholds, simulate various risk events, apply different risk management actions (Accept, Mitigate, Transfer, Eliminate), and analyze the resulting financial, reputational, and operational impacts.

The primary goal of QuLab is to provide a hands-on experience in understanding how risk appetite frameworks guide decision-making and ensure organizational resilience. It aids in visualizing the effectiveness of chosen risk responses and identifies areas where adjustments to policies or controls might be necessary.

## Features

QuLab provides a structured, step-by-step approach to risk simulation and analysis:

*   **1. Synthetic Risk Data Generation**:
    *   Generate a customizable number of synthetic risk scenarios across various categories (Strategic, Financial, Operational, Compliance, Reputational).
    *   Control reproducibility with an optional random seed.
    *   Simulates initial likelihood, financial impact ($), reputational impact (score), and operational impact (units).

*   **2. Dynamic Risk Appetite Definition**:
    *   Define key risk appetite thresholds interactively:
        *   **Max Acceptable Financial Loss per Incident ($)**: The maximum financial loss the firm is willing to tolerate from a single event.
        *   **Max Acceptable Incidents per Period**: A cap on the number of operational events per period.
        *   **Max Acceptable Reputational Impact Score**: The limit for damage to the firm's public standing (on a scale of 0-10).

*   **3. Interactive Scenario Outcome Simulation**:
    *   Select individual synthetic scenarios and apply one of four risk management actions:
        *   **Accept**: Incurs the full initial impact.
        *   **Mitigate**: Reduces both likelihood and impact by configurable percentages.
            *   *Formulae:* Residual Likelihood = Initial Likelihood × (1 - Likelihood Reduction %); Residual Impact = Initial Impact × (1 - Impact Reduction %)
        *   **Transfer**: Transfers financial risk, typically via insurance, with configurable deductible and coverage ratio.
            *   *Formulae:* Covered Amount = Initial Financial Impact × Insurance Coverage Ratio (%); Residual Financial Impact = max(0, Initial Financial Impact - Covered Amount) - Insurance Deductible
        *   **Eliminate**: Reduces all impacts and likelihood to zero.
    *   Real-time compliance checks for financial, operational, and reputational impacts against defined risk appetite.

*   **4. Comprehensive Simulation Logging**:
    *   Automatically logs the details of each simulated scenario, including initial impacts, chosen action, residual impacts, and compliance status.
    *   Provides an audit trail for analysis and governance review.

*   **5. Cumulative Impact Over Time Analysis**:
    *   Visualizes cumulative financial loss over successive simulated scenarios.
    *   Tracks the cumulative number of operational incidents that remain compliant with the defined appetite.
    *   **Initial vs. Residual Impact Plot**: A scatter plot comparing initial vs. residual financial impacts, clearly showing how actions reduce risk and where compliance thresholds are met/exceeded.

*   **6. Aggregated Risk Insights**:
    *   Aggregates simulation results by `Risk Category` and `Chosen Action`.
    *   Calculates the total residual financial impact for each group, enabling identification of high-risk areas or less effective actions.
    *   Presents aggregated data in both tabular and bar chart formats for quick insights.

## Getting Started

Follow these steps to set up and run the QuLab application on your local machine.

### Prerequisites

*   Python 3.8 or higher
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/QuLab-Risk-Governance.git
    cd QuLab-Risk-Governance
    ```
    *(Replace `yourusername` with the actual GitHub username/organization if this project is hosted on GitHub)*

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Create a `requirements.txt` file in your project root with the following content if you haven't already:)*
    ```
    streamlit==1.x.x # Use the version you developed with, or a recent stable one
    pandas==1.x.x
    numpy==1.x.x
    plotly==5.x.x
    ```

## Usage

Once you have installed the prerequisites, you can run the Streamlit application:

1.  **Navigate to the project root directory** (where `app.py` is located) in your terminal.

2.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

3.  Your web browser should automatically open a new tab displaying the QuLab application. If not, open your browser and go to `http://localhost:8501`.

### Basic Usage Flow

*   **Step 1: Generate Synthetic Data**: Use the sidebar controls under "Step 1" to define the number of scenarios and an optional random seed, then click "Generate Data".
*   **Step 2: Define Risk Appetite**: Adjust the financial loss, incident count, and reputational impact thresholds in the sidebar under "Step 2". These changes take effect immediately.
*   **Step 3: Simulate Scenarios**: Select a `Scenario ID` from the dropdown. Choose a `Risk Management Action` (Accept, Mitigate, Transfer, Eliminate) and configure any associated parameters (e.g., mitigation percentages, insurance deductible). Click "Run Simulation".
*   **Step 4-6: Review Results**: Observe the "Simulation Log", "Cumulative Impact Trends", and "Aggregated Risk Insights" sections in the main content area. These sections will update as you run more simulations.

## Project Structure

The project is organized into a modular structure:

```
QuLab-Risk-Governance/
├── app.py                      # Main Streamlit application entry point
├── application_pages/          # Directory for individual application pages/modules
│   └── risk_simulator.py       # Core logic for risk scenario generation, simulation, and analysis
├── requirements.txt            # Lists Python dependencies
└── README.md                   # Project documentation (this file)
```

## Technology Stack

*   **Streamlit**: For building the interactive web application user interface.
*   **Pandas**: For data manipulation and management (DataFrames).
*   **NumPy**: For numerical operations, especially in synthetic data generation.
*   **Plotly Express**: For creating interactive and insightful data visualizations.
*   **Python 3**: The core programming language.

## Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/AmazingFeature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
5.  Push to the branch (`git push origin feature/AmazingFeature`).
6.  Open a Pull Request.

Please ensure your code adheres to good practices and includes relevant documentation.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
*(You would typically add a `LICENSE` file in the root directory if you haven't already.)*

## Contact

For any questions or inquiries, please reach out:

*   **QuantUniversity**
*   **Website**: [www.quantuniversity.com](https://www.quantuniversity.com/)
*   **Email**: info@quantuniversity.com *(Replace with a more specific contact if applicable)*
