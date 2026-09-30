import streamlit as st
import sqlite3

conn = sqlite3.connect("expenserecord.db", check_same_thread=False)
cur = conn.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS records(category TEXT, ItemName TEXT, Amount INTEGER, WalletBalance INTEGER)"""
)
conn.commit()

st.title("🎯 EXPENSE TRACKER 🎯")

# Clean labels without stray trailing spaces
choice = st.sidebar.radio(
    "Choose an option", ["ADD AMOUNT IN WALLET", "ADD SPENDING", "CHECK RECORDS"]
)

# Fetch latest balance
cur.execute("SELECT WalletBalance FROM records ORDER BY ROWID DESC LIMIT 1")
last_record = cur.fetchone()
current_balance = last_record[0] if last_record and last_record[0] is not None else 0

st.metric(label="Current Wallet Balance", value=f"₹{current_balance}")

# 1. TOP-UP
if choice == "ADD AMOUNT IN WALLET":
    with st.form("wallet_topup_form"):
        new_wallet_amount = st.number_input(
            "Enter New Wallet Balance:", min_value=0, step=1, value=current_balance
        )
        submitted = st.form_submit_button("Update Balance")

        if submitted:
            cur.execute(
                "INSERT INTO records (category, ItemName, Amount, WalletBalance) VALUES (?, ?, ?, ?)",
                ("BALANCE UPDATE", "Wallet", 0, new_wallet_amount),
            )
            conn.commit()
            st.success("Balance updated successfully!")
            st.rerun()

# 2. SPENDING
elif choice == "ADD SPENDING":
    st.subheader("Add Spending Details")
    with st.form("spending_form"):
        cg = st.selectbox("Category", ["SHOPPING", "FOOD", "ENTERTAINMENT", "SOCIAL"])
        item_name = st.text_input("Name of Item:")
        item_price = st.number_input("Amount:", min_value=1, step=1)
        submitted = st.form_submit_button("Add Expense")

        if submitted:
            if not item_name.strip():
                st.error("Item name cannot be empty.")
            elif item_price > current_balance:
                st.error("Insufficient balance. Payment failed.")
            else:
                new_balance = current_balance - item_price
                cur.execute(
                    "INSERT INTO records (category, ItemName, Amount, WalletBalance) VALUES (?, ?, ?, ?)",
                    (cg, item_name, item_price, new_balance),
                )
                conn.commit()
                st.success(
                    f"Spent ₹{item_price} on {item_name}. Remaining: ₹{new_balance}"
                )
                st.rerun()

# 3. RECORDS
elif choice == "CHECK RECORDS":
    st.subheader("Your Expense Records")
    cur.execute("SELECT category, ItemName, Amount, WalletBalance FROM records")
    rows = cur.fetchall()

    if rows:
        st.dataframe(
            rows,
            column_config={
                "0": "Category",
                "1": "Item Name",
                "2": "Amount",
                "3": "Balance",
            },
        )
    else:
        st.info("No records found.")
