import streamlit as st
from pathlib import Path
import json
import random
import string

# -----------------------------
# Backend logic (adapted from the original CLI bank class)
# -----------------------------

class Bank:
    database = "database.json"

    @classmethod
    def load(cls):
        if Path(cls.database).exists():
            try:
                with open(cls.database, "r") as fs:
                    return json.loads(fs.read())
            except Exception as err:
                st.error(f"An error occurred while loading data: {err}")
                return []
        return []

    @classmethod
    def save(cls, data):
        with open(cls.database, "w") as fs:
            fs.write(json.dumps(data, indent=4))

    @staticmethod
    def generate_account_no():
        digits = random.choices(string.digits, k=12)
        return "".join(digits)

    @classmethod
    def find_user(cls, data, account_no, pin):
        for user in data:
            if str(user["pin"]) == str(pin) and user["account number"] == account_no:
                return user
        return None


# -----------------------------
# Streamlit app setup
# -----------------------------

st.set_page_config(page_title="Simple Bank App", page_icon="🏦", layout="centered")

if "data" not in st.session_state:
    st.session_state.data = Bank.load()

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None  # holds the dict of the logged-in user

st.title("🏦 Glow Bank")

menu = [
    "Create Account",
    "Login",
    "Deposit",
    "Withdrawal",
    "Check Details",
    "Update Details",
    "Delete Account",
]

choice = st.sidebar.radio("Choose an action", menu)

# Show login status in sidebar
st.sidebar.markdown("---")
if st.session_state.logged_in_user:
    st.sidebar.success(f"Logged in as {st.session_state.logged_in_user['name']}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in_user = None
        st.rerun()
else:
    st.sidebar.info("Not logged in")


def require_login():
    """Show a login form inline and return the logged-in user, or None."""
    if st.session_state.logged_in_user:
        return st.session_state.logged_in_user

    st.subheader("🔐 Login required")
    with st.form("login_form"):
        account_no = st.text_input("Account number")
        pin = st.text_input("4-digit PIN", type="password", max_chars=4)
        submitted = st.form_submit_button("Login")

    if submitted:
        if not account_no or not pin:
            st.warning("Please fill in both fields.")
            return None
        user = Bank.find_user(st.session_state.data, account_no, pin)
        if user is None:
            st.error("No such user exists! Check your account number and PIN.")
            return None
        st.session_state.logged_in_user = user
        st.success(f"Login successful! Welcome {user['name']}!")
        st.rerun()

    return None


# -----------------------------
# Create Account
# -----------------------------
if choice == "Create Account":
    st.subheader("📝 Create a new account")

    with st.form("create_account_form"):
        name = st.text_input("Full name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        mail = st.text_input("Email address")
        contact_number = st.text_input("Contact number (10 digits)")
        pin = st.text_input("4-digit PIN", type="password", max_chars=4)
        submitted = st.form_submit_button("Create Account")

    if submitted:
        errors = []
        if not name.strip():
            errors.append("Name cannot be empty.")
        if age < 18:
            errors.append("You are a minor. You must be 18 or older to open an account.")
        if not mail.strip():
            errors.append("Email cannot be empty.")
        if not contact_number.isdigit() or len(contact_number) != 10:
            errors.append("Contact number must contain exactly 10 digits.")
        if not pin.isdigit() or len(pin) != 4:
            errors.append("PIN must contain exactly 4 digits.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            account_no = Bank.generate_account_no()
            info = {
                "name": name,
                "age": int(age),
                "mail": mail,
                "balance": 0,
                "contact number": contact_number,
                "pin": pin,
                "account number": account_no,
            }
            st.session_state.data.append(info)
            Bank.save(st.session_state.data)
            st.success("Your account was created successfully! 🎉")
            st.info(f"Your account number is **{account_no}** — save it, you'll need it to log in.")

# -----------------------------
# Login (standalone view)
# -----------------------------
elif choice == "Login":
    st.subheader("🔐 Login")
    if st.session_state.logged_in_user:
        st.success(f"You're already logged in as {st.session_state.logged_in_user['name']}.")
    else:
        require_login()

# -----------------------------
# Deposit
# -----------------------------
elif choice == "Deposit":
    st.subheader("💰 Deposit Money")
    user = require_login()
    if user:
        with st.form("deposit_form"):
            amount = st.number_input("Amount to deposit (Rs)", min_value=0, step=1)
            submitted = st.form_submit_button("Deposit")
        if submitted:
            if amount > 100000 or amount <= 0:
                st.error("You cannot deposit more than 100000 Rs or less than/equal to 0 Rs!")
            else:
                user["balance"] += amount
                Bank.save(st.session_state.data)
                st.success(f"You have successfully deposited {amount} Rs!")
                st.metric("New balance", f"₹{user['balance']}")

# -----------------------------
# Withdrawal
# -----------------------------
elif choice == "Withdrawal":
    st.subheader("💸 Withdraw Money")
    user = require_login()
    if user:
        with st.form("withdraw_form"):
            amount = st.number_input("Amount to withdraw (Rs)", min_value=0, step=1)
            submitted = st.form_submit_button("Withdraw")
        if submitted:
            if amount <= 0:
                st.error("Enter an amount greater than 0.")
            elif user["balance"] > amount:
                user["balance"] -= amount
                Bank.save(st.session_state.data)
                st.success(f"You have successfully withdrawn {amount} Rs!")
                st.info(f"Thank you for visiting, {user['name']}!")
                st.metric("New balance", f"₹{user['balance']}")
            else:
                st.error("Insufficient balance!")

# -----------------------------
# Check Details
# -----------------------------
elif choice == "Check Details":
    st.subheader("📋 Account Details")
    user = require_login()
    if user:
        st.write("Your details are:")
        st.json(user)

# -----------------------------
# Update Details
# -----------------------------
elif choice == "Update Details":
    st.subheader("✏️ Update Details")
    user = require_login()
    if user:
        field = st.selectbox(
            "What would you like to update?",
            ["Name", "Email", "Contact number", "PIN"],
        )

        with st.form("update_form"):
            if field == "Name":
                new_value = st.text_input("New name")
            elif field == "Email":
                new_value = st.text_input("New email")
            elif field == "Contact number":
                new_value = st.text_input("New contact number (10 digits)")
            else:
                new_value = st.text_input("New 4-digit PIN", type="password", max_chars=4)

            submitted = st.form_submit_button("Update")

        if submitted:
            if field == "Name":
                if not new_value.strip():
                    st.error("Name cannot be empty.")
                else:
                    user["name"] = new_value
                    Bank.save(st.session_state.data)
                    st.success(f"Name updated successfully! New name: {new_value}")
            elif field == "Email":
                if not new_value.strip():
                    st.error("Email cannot be empty.")
                else:
                    user["mail"] = new_value
                    Bank.save(st.session_state.data)
                    st.success(f"Email updated successfully! New email: {new_value}")
            elif field == "Contact number":
                if not new_value.isdigit() or len(new_value) != 10:
                    st.error("Contact number must contain exactly 10 digits.")
                else:
                    user["contact number"] = new_value
                    Bank.save(st.session_state.data)
                    st.success(f"Phone number updated successfully! New number: {new_value}")
            else:
                if not new_value.isdigit() or len(new_value) != 4:
                    st.error("PIN must contain exactly 4 digits.")
                else:
                    user["pin"] = new_value
                    Bank.save(st.session_state.data)
                    st.success("PIN updated successfully!")

# -----------------------------
# Delete Account
# -----------------------------
elif choice == "Delete Account":
    st.subheader("🗑️ Delete Account")
    user = require_login()
    if user:
        st.warning("This action is permanent and cannot be undone.")
        confirm_no = st.text_input("Re-enter your account number to confirm deletion")
        if st.button("Delete my account"):
            if confirm_no == user["account number"]:
                st.session_state.data.remove(user)
                Bank.save(st.session_state.data)
                st.session_state.logged_in_user = None
                st.success("Account deleted successfully!")
                st.rerun()
            else:
                st.error("Account number doesn't match. Deletion cancelled.")