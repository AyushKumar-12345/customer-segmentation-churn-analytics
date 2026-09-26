# Customer Segmentation & Churn Risk Analytics Suite

## Executive Summary
An enterprise customer intelligence project analyzing multi-attribute transactional purchase histories to segment customer cohorts and calculate early-warning churn risk probabilities.

The repository features an automated feature engineering and unsupervised machine learning clustering pipeline (K-Means and PCA), an enterprise SQL warehouse analytical suite, an interactive Streamlit telemetry dashboard, and Power BI executive reports.

---

## Architecture and Pipeline
1. Dataset: Online Retail transactional logs and synthesized RFM profiles (`customer_segments.csv`). Large transactions hosted via GitHub Release `v1.0.0`.
2. Machine Learning ETL Pipeline (`process_segmentation_data.py`):
   - Outlier management and log transformations for skewed spend distributions.
   - Standard scaling and optimal cluster evaluation.
   - Unsupervised K-Means clustering with 2D Principal Component Analysis (PCA).
   - Early-warning rule-based Churn Probability Risk Index calculation.
3. Relational Warehouse Analytics (`segmentation_queries.sql`):
   - Pareto 80/20 customer monetary concentration.
   - Geographic churn rates and GMV-at-risk analysis.
   - 5x5 RFM grid cohort mapping.
4. Interactive Dashboards:
   - Live Streamlit Web App (`app.py`) with Plotly visualizations.
   - Interactive Power BI reports (`.pbix`) with Star Schema semantic modeling.

---

## Tech Stack & Tools
- Python: Pandas, NumPy, Scikit-Learn, Plotly, Streamlit
- SQL: CTEs, Window Functions (ROW_NUMBER, SUM OVER), Conditional Aggregations
- Power BI: Relational modeling, DAX measures

---

## Key Performance Indicators

| Metric | Business Definition |
|---|---|
| Recency (R) | Number of elapsed days since the customer's last recorded transaction |
| Frequency (F) | Total count of distinct orders placed across customer lifetime |
| Monetary (M) | Cumulative gross revenue generated per customer account |
| Churn Risk Score | Weighted composite probability index (0–100%) identifying attrition risk |

---

## How to Run Locally

1. Install dependencies:
   pip install -r requirements.txt

2. Run ML clustering & feature pipeline:
   python process_segmentation_data.py

3. Run interactive web dashboard:
   streamlit run app.py

---

## Author
Ayush Kumar
