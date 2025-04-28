import streamlit as st
import pandas as pd
import hashlib
import datetime

# Define a Block
class Block:
    def __init__(self, index, date, description, tx_type, amount, previous_hash):
        self.index = index
        self.date = date
        self.description = description
        self.tx_type = tx_type
        self.amount = amount
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.date}{self.description}{self.tx_type}{self.amount}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

# Initialize blockchain
if 'blockchain' not in st.session_state:
    # Create Genesis Block
    genesis_block = Block(0, str(datetime.datetime.now()), "Genesis Block", "Income", 0.0, "0")
    st.session_state.blockchain = [genesis_block]

st.title("🏥 Hospital Ledger with Blockchain 🔗")

st.subheader("➕ Add a New Transaction")
with st.form("transaction_form"):
    date = st.date_input("Date", value=datetime.date.today())
    description = st.text_input("Description")
    tx_type = st.selectbox("Type", ["Income", "Expense"])
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        previous_block = st.session_state.blockchain[-1]
        index = previous_block.index + 1
        previous_hash = previous_block.hash
        new_block = Block(index, str(date), description, tx_type, amount, previous_hash)
        st.session_state.blockchain.append(new_block)
        st.success("Transaction added successfully!")

st.subheader("📋 Blockchain Ledger")

# Display the blockchain
ledger_data = []
for block in st.session_state.blockchain:
    ledger_data.append({
        "Index": block.index,
        "Date": block.date,
        "Description": block.description,
        "Type": block.tx_type,
        "Amount": block.amount,
        "Previous Hash": block.previous_hash,
        "Hash": block.hash
    })

ledger_df = pd.DataFrame(ledger_data)
st.dataframe(ledger_df, use_container_width=True)

st.subheader("🔎 Blockchain Integrity Check")

# Check validity
def is_chain_valid(chain):
    for i in range(1, len(chain)):
        current_block = chain[i]
        previous_block = chain[i-1]
        
        if current_block.hash != current_block.calculate_hash():
            return False
        if current_block.previous_hash != previous_block.hash:
            return False
    return True

if is_chain_valid(st.session_state.blockchain):
    st.success("✅ Blockchain is valid!")
else:
    st.error("❌ Blockchain integrity compromised!")

# Download Blockchain Ledger
st.subheader("⬇️ Download Blockchain Ledger")
csv = ledger_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Ledger as CSV",
    data=csv,
    file_name='hospital_blockchain_ledger.csv',
    mime='text/csv',
)
