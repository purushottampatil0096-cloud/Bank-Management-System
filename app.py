import streamlit as st
import mysql.connector
import random
import string
import os
from dotenv import load_dotenv

# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

# =========================
# MYSQL CONNECTION
# =========================

connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

cursor = connection.cursor(dictionary=True)

# =========================
# BANK CLASS
# =========================

class Bank:

    # -------------------------
    # GENERATE ACCOUNT NUMBER
    # -------------------------

    def generate_account_number(self):

        letters = random.choices(
            string.ascii_uppercase,
            k=3
        )

        numbers = random.choices(
            string.digits,
            k=5
        )

        return "".join(letters + numbers)

    # -------------------------
    # CREATE ACCOUNT
    # -------------------------

    def create_account(
        self,
        name,
        age,
        email,
        pin
    ):

        if age < 18:
            return False, "Age must be 18 or above."

        if len(pin) != 4 or not pin.isdigit():
            return False, "PIN must be exactly 4 digits."

        # CHECK EMAIL

        query = """
        SELECT * FROM accounts
        WHERE email = %s
        """

        cursor.execute(query, (email,))

        existing_user = cursor.fetchone()

        if existing_user:
            return False, "Email already exists."

        account_no = self.generate_account_number()

        query = """
        INSERT INTO accounts
        (
            name,
            age,
            email,
            pin,
            account_no,
            balance
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            name,
            age,
            email,
            pin,
            account_no,
            0
        )

        cursor.execute(query, values)

        connection.commit()

        return True, {
            "name": name,
            "account_no": account_no,
            "balance": 0
        }

    # -------------------------
    # LOGIN
    # -------------------------

    def login(self, acc_no, pin):

        query = """
        SELECT * FROM accounts
        WHERE account_no = %s
        AND pin = %s
        """

        cursor.execute(query, (acc_no, pin))

        return cursor.fetchone()

    # -------------------------
    # GET USER
    # -------------------------

    def get_user(self, acc_no):

        query = """
        SELECT * FROM accounts
        WHERE account_no = %s
        """

        cursor.execute(query, (acc_no,))

        return cursor.fetchone()

    # -------------------------
    # DEPOSIT
    # -------------------------

    def deposit_money(self, user, amount):

        if amount <= 0:
            return False, "Amount must be greater than 0."

        query = """
        UPDATE accounts
        SET balance = balance + %s
        WHERE account_no = %s
        """

        cursor.execute(
            query,
            (amount, user["account_no"])
        )

        connection.commit()

        return True, "Money deposited successfully."

    # -------------------------
    # WITHDRAW
    # -------------------------

    def withdraw_money(self, user, amount):

        if amount <= 0:
            return False, "Invalid amount."

        if amount > user["balance"]:
            return False, "Insufficient balance."

        query = """
        UPDATE accounts
        SET balance = balance - %s
        WHERE account_no = %s
        """

        cursor.execute(
            query,
            (amount, user["account_no"])
        )

        connection.commit()

        return True, "Money withdrawn successfully."

    # -------------------------
    # UPDATE DETAILS
    # -------------------------

    def update_details(
        self,
        user,
        name,
        email,
        pin
    ):

        if name.strip():

            query = """
            UPDATE accounts
            SET name = %s
            WHERE account_no = %s
            """

            cursor.execute(
                query,
                (name, user["account_no"])
            )

        if email.strip():

            query = """
            UPDATE accounts
            SET email = %s
            WHERE account_no = %s
            """

            cursor.execute(
                query,
                (email, user["account_no"])
            )

        if pin.strip():

            if len(pin) != 4 or not pin.isdigit():
                return False, "PIN must be exactly 4 digits."

            query = """
            UPDATE accounts
            SET pin = %s
            WHERE account_no = %s
            """

            cursor.execute(
                query,
                (pin, user["account_no"])
            )

        connection.commit()

        return True, "Details updated successfully."

    # -------------------------
    # DELETE ACCOUNT
    # -------------------------

    def delete_account(self, user):

        query = """
        DELETE FROM accounts
        WHERE account_no = %s
        """

        cursor.execute(
            query,
            (user["account_no"],)
        )

        connection.commit()

        return True


# =========================
# STREAMLIT UI
# =========================

st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦"
)

st.title("🏦 Bank Management System")

bank = Bank()

menu = st.sidebar.selectbox(
    "Choose Operation",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Show Details",
        "Update Details",
        "Delete Account"
    ]
)

# =========================
# CREATE ACCOUNT
# =========================

if menu == "Create Account":

    st.subheader("Create Account")

    name = st.text_input("Enter Name")

    age = st.number_input(
        "Enter Age",
        min_value=1,
        step=1
    )

    email = st.text_input("Enter Email")

    pin = st.text_input(
        "Enter 4 Digit PIN",
        type="password"
    )

    if st.button("Create Account"):

        success, result = bank.create_account(
            name,
            int(age),
            email,
            pin
        )

        if success:

            st.success(
                "Account Created Successfully."
            )

            st.write(
                f"### Account Number: {result['account_no']}"
            )

        else:
            st.error(result)

# =========================
# DEPOSIT MONEY
# =========================

elif menu == "Deposit Money":

    st.subheader("Deposit Money")

    acc_no = st.text_input(
        "Enter Account Number"
    )

    pin = st.text_input(
        "Enter PIN",
        type="password"
    )

    amount = int(
        st.number_input(
            "Enter Amount",
            min_value=1,
            step=1
        )
    )

    if st.button("Deposit"):

        user = bank.login(acc_no, pin)

        if user:

            success, message = bank.deposit_money(
                user,
                amount
            )

            if success:

                updated_user = bank.get_user(acc_no)

                st.success(message)

                st.info(
                    f"Updated Balance: ₹{updated_user['balance']}"
                )

            else:
                st.error(message)

        else:
            st.error("Invalid credentials.")

# =========================
# WITHDRAW MONEY
# =========================

elif menu == "Withdraw Money":

    st.subheader("Withdraw Money")

    acc_no = st.text_input(
        "Enter Account Number"
    )

    pin = st.text_input(
        "Enter PIN",
        type="password"
    )

    amount = int(
        st.number_input(
            "Enter Amount",
            min_value=1,
            step=1
        )
    )

    if st.button("Withdraw"):

        user = bank.login(acc_no, pin)

        if user:

            success, message = bank.withdraw_money(
                user,
                amount
            )

            if success:

                updated_user = bank.get_user(acc_no)

                st.success(message)

                st.info(
                    f"Remaining Balance: ₹{updated_user['balance']}"
                )

            else:
                st.error(message)

        else:
            st.error("Invalid credentials.")

# =========================
# SHOW DETAILS
# =========================

elif menu == "Show Details":

    st.subheader("Show Account Details")

    acc_no = st.text_input(
        "Enter Account Number"
    )

    pin = st.text_input(
        "Enter PIN",
        type="password"
    )

    if st.button("Show Details"):

        user = bank.login(acc_no, pin)

        if user:

            st.success("Login Successful")

            st.write(f"### Name: {user['name']}")
            st.write(f"### Age: {user['age']}")
            st.write(f"### Email: {user['email']}")
            st.write(
                f"### Account Number: {user['account_no']}"
            )
            st.write(
                f"### Balance: ₹{user['balance']}"
            )

        else:
            st.error("Invalid credentials.")

# =========================
# UPDATE DETAILS
# =========================

elif menu == "Update Details":

    st.subheader("Update Account")

    acc_no = st.text_input(
        "Enter Account Number"
    )

    old_pin = st.text_input(
        "Enter Current PIN",
        type="password"
    )

    user = bank.login(acc_no, old_pin)

    if user:

        st.success("Login Successful")

        new_name = st.text_input("Enter New Name")

        new_email = st.text_input("Enter New Email")

        new_pin = st.text_input(
            "Enter New PIN",
            type="password"
        )

        if st.button("Update"):

            success, message = bank.update_details(
                user,
                new_name,
                new_email,
                new_pin
            )

            if success:
                st.success(message)

            else:
                st.error(message)

    elif acc_no and old_pin:
        st.error("Invalid credentials.")

# =========================
# DELETE ACCOUNT
# =========================

elif menu == "Delete Account":

    st.subheader("Delete Account")

    acc_no = st.text_input(
        "Enter Account Number"
    )

    pin = st.text_input(
        "Enter PIN",
        type="password"
    )

    confirm = st.checkbox(
        "I confirm account deletion."
    )

    if st.button("Delete Account"):

        user = bank.login(acc_no, pin)

        if user:

            if confirm:

                bank.delete_account(user)

                st.success(
                    "Account deleted successfully."
                )

            else:
                st.warning(
                    "Please confirm deletion."
                )

        else:
            st.error("Invalid credentials.")