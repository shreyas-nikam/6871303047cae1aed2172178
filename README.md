Here's a comprehensive `README.md` file for your Streamlit application lab project.

---

# QuLab: Risk Apetite & Governance Simulator

![QuantUniversity Logo](https://www.quantuniversity.com/assets/img/logo5.jpg)

## Project Description

The **Risk Governance Lab 1** is a interactive Streamlit application designed to simulate risk management strategies within a firm's predefined risk appetite. It serves as an educational and experimental platform, allowing users to:

*   **Generate synthetic risk scenarios:** Create diverse risk events with varying initial likelihoods and impacts (financial, reputational, operational).
*   **Define risk appetite thresholds:** Set quantitative limits for acceptable financial loss, incident frequency, and reputational damage.
*   **Simulate risk management actions:** Apply different strategies (Accept, Mitigate, Transfer, Eliminate) to individual scenarios and observe their residual impacts.
*   **Visualize the impact of actions:** Analyze cumulative impacts over time and aggregate results by risk category and action taken, providing insights into overall risk exposure and policy effectiveness.

This lab aims to illustrate the dynamic interplay between risk events, management interventions, and a firm's risk appetite, emphasizing key principles of effective risk governance and compliance.

## Features

The application is structured into three main pages, each offering distinct functionalities:

1.  ### Data Generation & Risk Appetite
    *   **Synthetic Data Generation**: Create a configurable number of synthetic risk scenarios across various categories (Strategic, Financial, Operational, Compliance, Reputational) with customizable initial impacts and likelihoods. A random seed option ensures reproducibility.
    *   **Risk Appetite Definition**: Set numerical thresholds for:
        *   Maximum Acceptable Financial Loss per Incident
        *   Maximum Acceptable Incidents per Period
        *   Maximum Acceptable Reputational Impact Score
    *   **Data Display**: View the generated synthetic risk scenarios and the currently defined risk appetite thresholds.

2.  ### Scenario Simulation
    *   **Individual Scenario Selection**: Choose a specific generated risk scenario for simulation.
    *   **Risk Management Actions**: Apply one of four common risk management strategies:
        *   **Accept**: Incur the full initial impact and likelihood.
        *   **Mitigate**: Reduce both impact and likelihood by configurable percentages.
        *   **Transfer**: Reduce financial impact through simulated insurance (deductible and coverage ratio).
        *   **Eliminate**: Reduce likelihood and impact to zero.
    *   **Real-time Outcome Display**: See the initial and residual impacts, along with compliance status against the defined risk appetite, for the chosen scenario and action.
    *   **Simulation Log**: Maintain a historical log of all simulated scenarios, chosen actions, and their outcomes, crucial for audit and governance.

3.  ### Impact Analysis
    *   **Cumulative Impact Visualization**: Plot cumulative financial impact and cumulative compliant operational incidents over the sequence of simulated scenarios, revealing trends and overall exposure.
    *   **Aggregated Results**: Group simulation outcomes by risk category and the chosen action, summarizing total residual financial impact for each combination.
    *   **Insights Identification**: Utilize bar charts to visually identify high-risk areas or the most effective risk management actions based on aggregated financial impacts.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

*   Python 3.8+
*   pip (Python package installer)
*   Git (for cloning the repository)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/risk-governance-lab.git
    cd risk-governance-lab
    ```

    *(Note: Replace `https://github.com/your-username/risk-governance-lab.git` with the actual repository URL.)*

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    The application relies on `streamlit`, `pandas`, `numpy`, and `plotly`. You can install them using pip:

    ```bash
    pip install streamlit pandas numpy plotly plotly-express
    ```

    *(Alternatively, create a `requirements.txt` file with these libraries listed and run `pip install -r requirements.txt`)*

## Usage

1.  **Run the Streamlit application:**

    Make sure your virtual environment is activated, then run:

    ```bash
    streamlit run app.py
    ```

    This command will open the application in your default web browser (usually at `http://localhost:8501`).

2.  **Navigate the Application:**

    *   **Sidebar Navigation:** Use the "Navigation" selectbox in the sidebar to switch between the three main pages: "Data Generation & Risk Appetite", "Scenario Simulation", and "Impact Analysis".

    *   **Page 1: Data Generation & Risk Appetite:**
        *   Use the slider to set the number of synthetic scenarios to generate.
        *   Optionally provide a random seed for reproducibility.
        *   Click "Generate Data" to populate the scenarios.
        *   Adjust the number inputs to define your firm's risk appetite thresholds. These values are automatically saved and used across the application.

    *   **Page 2: Scenario Simulation:**
        *   Ensure you have generated data on Page 1 first.
        *   Select a "Scenario ID" from the dropdown.
        *   Choose a "Risk Management Action" (Accept, Mitigate, Transfer, Eliminate).
        *   If "Mitigate" or "Transfer" is chosen, adjust the specific parameters (e.g., Impact Reduction, Insurance Deductible).
        *   Click "Run Simulation" to see the immediate outcome and compliance status.
        *   The simulation results will be automatically logged and become visible in the "Simulation Log" table below. If you re-simulate the same scenario, its entry in the log will be updated.

    *   **Page 3: Impact Analysis:**
        *   Ensure you have run simulations on Page 2 and logged outcomes.
        *   This page automatically displays interactive charts showing:
            *   Cumulative Financial Impact over time.
            *   Cumulative Compliant Operational Incidents over time.
        *   It also presents a table and a bar chart of aggregated residual financial impacts, grouped by risk category and the action taken, helping you identify areas of concern or effective strategies.

## Project Structure

```
.
├── app.py
├── application_pages/
│   ├── __init__.py
│   ├── page1.py
│   ├── page2.py
│   └── page3.py
└── README.md
```

*   `app.py`: The main entry point of the Streamlit application. It sets up the page configuration, displays the main title and description, and handles navigation between different functional pages.
*   `application_pages/`: A directory containing modular Python scripts for each major section/page of the application.
    *   `page1.py`: Contains logic for generating synthetic risk data and defining risk appetite thresholds.
    *   `page2.py`: Handles the simulation of risk management actions for individual scenarios and maintains a simulation log.
    *   `page3.py`: Focuses on calculating and visualizing cumulative impacts and aggregated results from the simulation log.
*   `README.md`: This file, providing an overview of the project.

## Technology Stack

*   **Frontend/Framework**: [Streamlit](https://streamlit.io/) (for creating interactive web applications with Python)
*   **Data Manipulation**: [Pandas](https://pandas.pydata.org/) (for data structures and analysis)
*   **Numerical Operations**: [NumPy](https://numpy.org/) (for numerical computing)
*   **Charting/Visualization**: [Plotly Express](https://plotly.com/python/plotly-express/) (for declarative, high-level plotting)
*   **Programming Language**: Python 3.x

## Contributing

Contributions are welcome! If you have suggestions for improvements, bug fixes, or new features, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/AmazingFeature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
5.  Push to the branch (`git push origin feature/AmazingFeature`).
6.  Open a Pull Request.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details (if applicable, otherwise state "No specific license defined for this lab project").

## Contact

For questions or inquiries, please contact:

*   **QuantUniversity** (info@quantuniversity.com)
*   Project Maintainer: [Your Name/GitHub Profile Link] (Optional)

---