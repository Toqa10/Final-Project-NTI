# Health Data Analytics & Risk Prediction — Dashboard

An interactive Streamlit + Plotly deployment of `python_project_NTI.ipynb`: a full health-data
analytics and machine-learning project turned into a professional, filterable web dashboard with a
consistent **blue + gray** theme and a light/dark mode toggle.

## What's Included

- **🏠 Overview** — executive summary with headline KPIs and best-model callout.
- **📊 Analytics Dashboard** — interactive filters, population demographics, health-indicator
  distributions, correlation heatmap, BP-risk breakdowns, and a data explorer with CSV download.
- **💡 Business Insights** — the 6 core business/health questions from the notebook, each with its
  chart, data-driven answer, insight, implication, and recommendation, plus the full KPI dashboard.
- **🤖 Machine Learning** — target/feature definitions, Model 1 (Logistic Regression) vs Model 2
  (Random Forest) cards, a full metrics comparison table + chart, the best-model callout, and
  feature-importance charts for both models.
- **ℹ️ About** — project narrative, dataset summary, methodology, technologies, and highlights.

## Data Source of Truth

Every number in this app is either:

1. **Loaded live** from `cleaned_health_data.csv` if that file is present next to `app.py`, or
   uploaded via the sidebar file-uploader while the app is running — this unlocks live filtering,
   the data explorer table, and the CSV download button, or
2. **Read from `notebook_results.py`** — real values captured directly from the executed cells of
   `python_project_NTI.ipynb` (KPIs, business-question answers, correlation matrix, model metrics,
   feature importance). Nothing in this file is invented or estimated from nothing; it is the
   dashboard's fallback so it always shows a correct, notebook-grounded picture even without the CSV.

To run in full **live mode**, place your cleaned dataset next to `app.py` as either
`cleaned_health_data.csv` or `health_data_cleaned.csv`, or just upload it from the sidebar once the
app is running.

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually `http://localhost:8501`).

## How to Deploy

**Streamlit Community Cloud** (simplest):
1. Push this folder to a GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io), connect the repo, and set the main file to
   `app.py`.
3. (Optional) add `cleaned_health_data.csv` to the repo for live mode by default.

Any other platform that can run a Python web process (Render, Railway, an internal server, etc.) works
the same way: install `requirements.txt`, then run `streamlit run app.py --server.port $PORT
--server.address 0.0.0.0`.

## Required Files

```
healthcare-analytics-dashboard/
├── app.py                    # main Streamlit application
├── notebook_results.py       # real values extracted from the notebook (fallback data source)
├── requirements.txt
├── README.md
└── cleaned_health_data.csv   # optional — add for full live/interactive mode
```

## Notes

- No local/Windows-specific paths are used; the app looks for the CSV relative to its own folder.
- The light/dark toggle re-themes the sidebar, cards, and every chart together (no chart-by-chart
  color drift) using one shared blue + gray palette.
- If you don't have `cleaned_health_data.csv` handy yet, you can add an export step to the notebook
  (`df.to_csv('cleaned_health_data.csv', index=False)` after the feature-engineering section) and
  re-run it in Colab to produce one.
