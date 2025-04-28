import streamlit as st
import pandas as pd

# Initialize session state to store transactions
if 'ledger' not in st.session_state:
    st.session_state.ledger = pd.DataFrame(columns=["Date", "Description", "Type", "Amount"])

st.title("🏥 Hospital Ledger")

st.subheader("➕ Add a Transaction")
with st.form("transaction_form"):
    date = st.date_input("Date")
    description = st.text_input("Description")
    transaction_type = st.selectbox("Type", ["Income", "Expense"])
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    
    submitted = st.form_submit_button("Add Transaction")
    if submitted:
        new_transaction = {
            "Date": date,
            "Description": description,
            "Type": transaction_type,
            "Amount": amount if transaction_type == "Income" else -amount
        }
        st.session_state.ledger = pd.concat(
            [st.session_state.ledger, pd.DataFrame([new_transaction])],
            ignore_index=True
        )
        st.success("Transaction added successfully!")

st.subheader("📋 Ledger Records")
st.dataframe(st.session_state.ledger, use_container_width=True)

# Calculate Balance
st.subheader("💰 Ledger Summary")
total_income = st.session_state.ledger[st.session_state.ledger["Type"] == "Income"]["Amount"].sum()
total_expense = -st.session_state.ledger[st.session_state.ledger["Type"] == "Expense"]["Amount"].sum()
balance = total_income - total_expense

col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"₹ {total_income:,.2f}")
col2.metric("Total Expense", f"₹ {total_expense:,.2f}")
col3.metric("Current Balance", f"₹ {balance:,.2f}")

# Optional: Download Ledger
st.subheader("⬇️ Download Ledger")
csv = st.session_state.ledger.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Ledger as CSV",
    data=csv,
    file_name='hospital_ledger.csv',
    mime='text/csv',
)
