
import streamlit as st

# Credit limit calculation function
def calculate_credit_limit(
    credit_score, income, dti, payment_history_score,
    weight_credit_score=0.3,
    weight_income=0.3,
    weight_dti=0.2,
    weight_payment_history=0.2
):
    norm_credit_score = credit_score / 850
    norm_income = min(income / 100000, 1)
    norm_dti = max(1 - dti, 0)
    score = (
        norm_credit_score * weight_credit_score +
        norm_income * weight_income +
        norm_dti * weight_dti +
        payment_history_score * weight_payment_history
    )
    min_limit = 500
    max_limit = 20000
    recommended_limit = min_limit + score * (max_limit - min_limit)
    return round(recommended_limit, 2)

st.title("Credit Limit Estimator")

st.sidebar.header("Input Parameters")
credit_score = st.sidebar.slider("Credit Score", 300, 850, 720)
income = st.sidebar.number_input("Annual Income ($)", min_value=10000, max_value=200000, value=75000, step=1000)
dti = st.sidebar.slider("Debt-to-Income Ratio", 0.0, 1.0, 0.25)
payment_history_score = st.sidebar.slider("Payment History Score", 0.0, 1.0, 0.95)

st.sidebar.header("Adjust Weights (Sum should be 1.0)")
weight_credit_score = st.sidebar.slider("Weight: Credit Score", 0.0, 1.0, 0.3)
weight_income = st.sidebar.slider("Weight: Income", 0.0, 1.0, 0.3)
weight_dti = st.sidebar.slider("Weight: DTI", 0.0, 1.0, 0.2)
weight_payment_history = st.sidebar.slider("Weight: Payment History", 0.0, 1.0, 0.2)

total_weight = weight_credit_score + weight_income + weight_dti + weight_payment_history
if abs(total_weight - 1.0) > 0.01:
    st.sidebar.warning(f"Total weight is {total_weight:.2f}. It should be 1.0.")

limit = calculate_credit_limit(
    credit_score, income, dti, payment_history_score,
    weight_credit_score, weight_income, weight_dti, weight_payment_history
)

st.subheader("Recommended Credit Limit")
st.metric(label="Credit Limit", value=f"${limit}")
