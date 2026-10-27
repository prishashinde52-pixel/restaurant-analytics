# Restaurant Analytics Lab

An interactive restaurant analytics dashboard built with Python and Streamlit to explore sales performance, understand menu trends, and generate short-term revenue forecasts.

**[Live Demo](https://restaurant-analytics-prishinde.streamlit.app/) · [Source Code](https://github.com/prishashinde52-pixel/restaurant-analytics)**

## Overview

Restaurant Analytics Lab is a prototype designed to demonstrate how sales data can be transformed into meaningful visual insights. It brings together key performance indicators, interactive charts, menu analysis, and a baseline revenue forecasting method in one dashboard.

The current version uses **synthetic data generated for five fictional restaurants**. It serves as a public demonstration of the dashboard's analytical capabilities while the project is being developed further.

## Features

- **Sales Performance:** Explore total revenue, total orders, and average revenue per order.
- **Revenue Trends:** Visualize daily revenue and compare average weekday and weekend performance.
- **Restaurant Comparison:** Compare generated revenue across the five sample restaurants.
- **Menu Analytics:** Identify popular menu items and examine quantities sold and item-level revenue.
- **Seven-Day Revenue Forecast:** Estimate upcoming daily revenue using average revenue by weekday over the latest 28 days of historical sample data.
- **Data Explorer:** Inspect and download daily sales and item-level sales data as CSV files.
- **Interactive Dashboard:** Filter results by restaurant and explore visualizations through a Streamlit interface.

## Live Demo

Explore the dashboard here:

**[Open Restaurant Analytics Lab](https://restaurant-analytics-prishinde.streamlit.app/)**

The public demo uses generated sample data only. It does not display the actual sales records of the restaurants whose data I have obtained separately.

## Tech Stack

- **Python** — application logic and data processing
- **Streamlit** — interactive dashboard and user interface
- **Pandas** — data manipulation and aggregation
- **NumPy** — sample data generation and numerical calculations
- **Plotly Express** — interactive charts and visualizations

## Getting Started

### Prerequisites

- Python 3.10 or a compatible version
- pip

### Installation

Clone the repository:

```bash
git clone https://github.com/prishashinde52-pixel/restaurant-analytics.git
cd restaurant-analytics
```

Create and activate a virtual environment.

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Launch the dashboard:

```bash
streamlit run app.py
```

Streamlit will provide a local URL in the terminal where you can access the application.

## Forecasting Methodology

The current prototype implements a simple weekday-average baseline rather than a trained machine-learning model.

The process:
1. Aggregate daily revenue from the generated sales records.
2. Select the latest 28 days of historical data.
3. Calculate average revenue for each weekday.
4. Use the corresponding weekday average to estimate revenue for each of the next seven days.

This provides a straightforward baseline for exploring forecasting concepts. Forecast accuracy has not yet been evaluated against actual future sales.

## Data and Privacy

All records displayed in the public demo are synthetically generated for demonstration purposes.

Actual restaurant datasets are kept separate from this public repository. They are not included in the demo's source code or intentionally published through the public dashboard.

Future versions are intended to explore the use of restaurant-specific sales data, with appropriate permissions and access controls.

## Project Roadmap

- [x] Build an interactive Streamlit dashboard.
- [x] Generate sample data for multiple fictional restaurants.
- [x] Implement sales KPIs and revenue visualizations.
- [x] Add menu-level analysis and a seven-day baseline forecast.
- [x] Deploy a public demonstration.
- [ ] Add support for restaurant-specific CSV data.
- [ ] Validate data formats and handle missing or inconsistent records.
- [ ] Adapt the dashboard for two restaurants using their own sales data.
- [ ] Implement appropriate authentication and data isolation before any real-data deployment.
- [ ] Evaluate forecast performance against historical holdout data.

## Current Limitations

- The current dashboard uses synthetic data rather than actual restaurant sales records.
- The forecasting method is a simple baseline and is not a trained predictive model.
- Forecast accuracy and business impact have not been established.
- Secure multi-restaurant access and production data workflows are not yet implemented.

## Author

**Prisha Shinde**

Built as an ongoing project exploring Python-based analytics, interactive data visualization, and practical applications of data-driven decision-making.
