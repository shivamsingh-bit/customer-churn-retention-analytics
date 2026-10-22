import joblib
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

BASE = Path(__file__).parent
st.set_page_config(page_title="Customer Churn Prediction", page_icon="📉")

@st.cache_resource
def load_model():
    return joblib.load(BASE / "models" / "churn_pipeline.pkl")  # only load files you trust

@st.cache_data
def load_data():
    return pd.read_csv(BASE / "data" / "customer_churn_clean.csv")

model, data = load_model(), load_data()

st.title("📉 Customer Churn Prediction")
st.write("Enter a customer's details to estimate whether they are likely to leave. Model: K-Nearest Neighbors.")

st.header("Customer details")
c1, c2 = st.columns(2)
with c1:
    gender = st.selectbox("Gender", ["Female", "Male"])
    senior = st.selectbox("Senior citizen", ["No", "Yes"])
    tenure = st.number_input("Tenure (months)", 0, 120, 12)
    monthly = st.number_input("Monthly charges ($)", 0.0, 200.0, 70.0, step=0.5)
    total = st.number_input("Total charges ($)", 0.0, 15000.0, 840.0, step=10.0)
with c2:
    contract = st.selectbox("Contract type", ["Month-to-month", "One year", "Two year"])
    internet = st.selectbox("Internet service", ["DSL", "Fiber optic", "No"])
    tech = st.selectbox("Technical support", ["No", "Yes", "No internet service"])

st.header("Prediction")
if st.button("Predict churn", type="primary"):
    row = pd.DataFrame([{"tenure": tenure, "monthly_charges": monthly, "total_charges": total,
                         "gender": gender, "senior_citizen": senior, "contract_type": contract,
                         "internet_service": internet, "tech_support": tech}])
    prob = model.predict_proba(row)[0, 1]
    if model.predict(row)[0] == 1:
        st.error(f"Likely to CHURN (estimated probability {prob:.0%})")
        st.write("Suggestion: offer a longer-contract discount or a tech-support bundle.")
    else:
        st.success(f"Likely to STAY (estimated probability of churn {prob:.0%})")
    st.caption("This is an estimate from a simple model, not a certainty.")

st.header("Business insights")
st.metric("Total customers", f"{len(data):,}")
st.metric("Churn rate", f"{(data['churn'] == 'Yes').mean():.1%}")
for col in ["contract_type", "tech_support"]:
    t = data.groupby(col)["churn"].apply(lambda s: (s == "Yes").mean() * 100).reset_index(name="churn_rate_%")
    fig = px.bar(t, x=col, y="churn_rate_%", title=f"Churn rate (%) by {col}", color_discrete_sequence=["#E45756"])
    st.plotly_chart(fig, width="stretch")
