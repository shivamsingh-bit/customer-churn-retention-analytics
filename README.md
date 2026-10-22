# Customer Churn Prediction

Python + SQL + KNN + Streamlit, using the Kaggle Telco Customer Churn dataset (7,043 customers, 26.5% churn).
The dataset has no `age` column, so `senior_citizen` is used instead.

## Structure
```
data/            customer_churn.csv (raw), customer_churn_clean.csv, churn.db (SQLite)
notebooks/       notebook.ipynb  (cleaning, SQL, basic EDA, KNN, metrics, save model)
models/          churn_pipeline.pkl  (scaler + encoder + KNN in one pipeline)
app.py           Streamlit app
sql_analysis.sql 3 KPI queries
```

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
To retrain: open `notebooks/notebook.ipynb` and run all cells. (The saved model was made with scikit-learn 1.8; retrain if you get version warnings.)

## Method
- Features: tenure, monthly_charges, total_charges (scaled) + gender, senior_citizen, contract_type, internet_service, tech_support (one-hot encoded).
- 80/20 stratified split. Preprocessing is inside the pipeline, so it is fitted on training data only.
- KNN tuned with 5-fold GridSearchCV on the training set (best: 51 neighbours, distance weighting).

## Test-set results (actual)
| Accuracy | Precision | Recall | F1 |
|---|---|---|---|
| 0.787 | 0.617 | 0.521 | 0.565 |

Accuracy looks fine, but recall shows KNN misses about half of the customers who really leave.

## Findings (associations, not proof of cause)
- Month-to-month contracts churn ~43% vs ~3% for two-year contracts.
- Fibre-optic customers and customers without tech support churn more.
- Short-tenure customers churn more; gender makes almost no difference.
