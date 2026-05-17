import os
from pathlib import Path
import mysql.connector


def load_environment():
    env_path = Path(__file__).with_name('.env')
    if not env_path.exists():
        return

    with env_path.open() as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            if key and value and key not in os.environ:
                os.environ[key] = value


def connect_database():
    try:
        return mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
    except mysql.connector.Error as err:
        print(f"Failed to connect to the database: {err}")
        print("Please verify your credentials and database availability.")
        raise


def prompt_int(prompt_text, min_value=None, max_value=None):
    while True:
        user_input = input(prompt_text).strip()
        if not user_input:
            print("Input cannot be empty. Please enter a number.")
            continue
        if not user_input.isdigit():
            print("Please enter a valid numeric value.")
            continue
        value = int(user_input)
        if min_value is not None and value < min_value:
            print(f"Value must be at least {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Value must be at most {max_value}.")
            continue
        return value


def prompt_choice(prompt_text, valid_choices):
    choices = [choice.lower() for choice in valid_choices]
    while True:
        choice = input(prompt_text).strip().lower()
        if choice in choices:
            return choice
        print(f"Please choose one of: {', '.join(valid_choices)}.")


def print_table(headers, rows):
    if not rows:
        print("No records found.")
        return

    columns = [list(map(str, column)) for column in zip(*([headers] + [list(map(str, row)) for row in rows]))]
    widths = [max(len(item) for item in column) for column in columns]
    header_line = ' | '.join(header.ljust(width) for header, width in zip(headers, widths))
    separator = '-+-'.join('-' * width for width in widths)
    print(header_line)
    print(separator)
    for row in rows:
        print(' | '.join(str(value).ljust(width) for value, width in zip(row, widths)))


def record_transaction(transaction_type, amount, account_number):
    cursor.execute("SELECT IFNULL(MAX(transaction_number), 0) + 1 FROM transaction_details")
    next_transaction_no = cursor.fetchone()[0]
    cursor.execute(
        "INSERT INTO transaction_details(transaction_number, account_number, transaction_type, amount) VALUES (%s, %s, %s, %s)",
        (next_transaction_no, account_number, transaction_type, amount)
    )
    conn.commit()


def create_account():
    print("\nCreate a new account")
    account_name = input("Enter account name: ").strip()
    if not account_name:
        print("Account name cannot be blank.")
        return

    account_number = prompt_int("Enter account number: ", min_value=1, max_value=2147483647)
    account_type = prompt_choice("Enter account type (savings/current): ", ["savings", "current"])
    initial_deposit = prompt_int("Enter initial deposit amount: ", min_value=0)
    account_pin = prompt_int("Set a 4-digit PIN: ", min_value=1000, max_value=9999)

    try:
        cursor.execute(
            "INSERT INTO user_bank_info(name, account_number, account_type, account_balance, account_pin) VALUES (%s, %s, %s, %s, %s)",
            (account_name, account_number, account_type, initial_deposit, account_pin)
        )
        conn.commit()
        print("\nAccount created successfully.\n")
    except mysql.connector.Error as err:
        print(f"Could not create account: {err}")


def user_login():
    print("\nUser login")
    account_number = prompt_int("Enter account number: ", min_value=1, max_value=2147483647)
    account_pin = prompt_int("Enter 4-digit PIN: ", min_value=1000, max_value=9999)

    cursor.execute(
        "SELECT name FROM user_bank_info WHERE account_number = %s AND account_pin = %s",
        (account_number, account_pin)
    )
    result = cursor.fetchone()
    if result:
        print(f"\nWelcome, {result[0]}\n")
        user_menu(account_number)
    else:
        print("\nInvalid account number or PIN.\n")


def user_menu(account_number):
    while True:
        print("\nUser menu")
        option = prompt_int(
            "1. View Balance\n2. Deposit\n3. Withdraw\n4. View Transactions\n5. Logout\nEnter your choice: ",
            min_value=1,
            max_value=5
        )

        if option == 1:
            cursor.execute(
                "SELECT account_balance FROM user_bank_info WHERE account_number = %s",
                (account_number, )
            )
            result = cursor.fetchone()
            if result is None:
                print("\nAccount not found.\n")
            else:
                print(f"\nCurrent balance: {result[0]}\n")

        elif option == 2:
            deposit_amount = prompt_int("Enter amount to deposit: ", min_value=1)
            try:
                cursor.execute(
                    "UPDATE user_bank_info SET account_balance = account_balance + %s WHERE account_number = %s",
                    (deposit_amount, account_number)
                )
                conn.commit()
                record_transaction("deposit", deposit_amount, account_number)
                print(f"\n{deposit_amount} deposited successfully.\n")
            except mysql.connector.Error as err:
                print(f"Could not complete deposit: {err}")

        elif option == 3:
            withdraw_amount = prompt_int("Enter amount to withdraw: ", min_value=1)
            cursor.execute(
                "SELECT account_balance FROM user_bank_info WHERE account_number = %s",
                (account_number, )
            )
            result = cursor.fetchone()
            if result is None:
                print("\nAccount not found.\n")
                continue
            current_balance = result[0]
            if current_balance < withdraw_amount:
                print("\nInsufficient balance.\n")
                continue
            try:
                cursor.execute(
                    "UPDATE user_bank_info SET account_balance = account_balance - %s WHERE account_number = %s",
                    (withdraw_amount, account_number)
                )
                conn.commit()
                record_transaction("withdraw", withdraw_amount, account_number)
                print("\nWithdraw successful.\n")
            except mysql.connector.Error as err:
                print(f"Could not complete withdrawal: {err}")

        elif option == 4:
            cursor.execute(
                "SELECT transaction_number, transaction_type, amount, date_of_transaction FROM transaction_details WHERE account_number = %s ORDER BY transaction_number",
                (account_number, )
            )
            transaction_rows = cursor.fetchall()
            print()
            print_table(
                ["Transaction Number", "Type", "Amount", "Date"],
                transaction_rows
            )
            print()

        elif option == 5:
            print("Logging out...\n")
            break


def admin_page():
    print("\nAdmin login")
    admin_name = input("Enter admin name: ").strip()
    if not admin_name:
        print("Admin name cannot be blank.")
        return
    admin_password = prompt_int("Enter admin password: ", min_value=0)

    cursor.execute(
        "SELECT 1 FROM admin_info WHERE name = %s AND pin = %s",
        (admin_name, admin_password)
    )
    auth_result = cursor.fetchone()
    if not auth_result:
        print("\nInvalid admin name or password.\n")
        return

    print("\nAdmin login successful.\n")
    cursor.execute(
        "SELECT name, account_number, account_type, account_balance, account_pin, date_of_create FROM user_bank_info ORDER BY account_number"
    )
    customer_rows = cursor.fetchall()
    print_table(
        ["Name", "Account Number", "Type", "Balance", "PIN", "Created Date"],
        customer_rows
    )
    print()


def main():
    load_environment()
    global conn, cursor
    conn = connect_database()
    cursor = conn.cursor()

    while True:
        print("\n------> Bank Management System <------")
        option = prompt_int(
            "1. Create Account\n2. User Login\n3. Admin Login\n4. Exit\nEnter your choice: ",
            min_value=1,
            max_value=4
        )

        if option == 1:
            create_account()
        elif option == 2:
            user_login()
        elif option == 3:
            admin_page()
        elif option == 4:
            print("\nExiting... Thank you.\n")
            break


if __name__ == "__main__":
    main()
