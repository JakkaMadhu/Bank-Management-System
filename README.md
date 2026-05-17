# Bank Management System

A command-line banking application built with Python and MySQL. The system supports user account creation, PIN-based authentication, deposits, withdrawals, and transaction history reporting.

## Features

- Create new customer accounts
- Authenticate users with account number and 4-digit PIN
- Deposit and withdraw funds
- Display current account balance
- Record transaction history automatically
- Show transaction history in a table format
- Admin access to view all customer accounts in a table layout
- Environment-based database configuration with `.env`

## Technology Stack

- Python 3
- MySQL
- `mysql-connector-python`

## Setup Instructions

1. Install Python 3.
2. Install MySQL and start the database server.
3. Install Python dependencies:

```bash
pip install mysql-connector-python
```

4. Create a `.env` file in the project root with the database connection details:

```env
DB_HOST=your_host_address
DB_USER=your_user_name
DB_PASSWORD=your_password_here
DB_NAME=dbbankmanagement
```

5. Create the database schema by running the SQL file. In a terminal, use:

```bash
mysql -u root -p < BankDatabase.sql
```

6. Confirm that the database and tables were created successfully.

## Running the Application

Start the application with:

```bash
python BankManagementSystem.py
```

Then follow the menu prompts to:

- Create an account
- Log in as a user
- Deposit or withdraw funds
- View transactions
- Log in as admin

## Usage Notes

- Account numbers are stored as integers and support up to 10 digits.
- PINs must be 4 digits.
- Deposit and withdrawal amounts must be positive integers.
- Transaction history and admin account listings are displayed with column headers for readability.
- Do not include quotes around values in the `.env` file unless necessary; if you do, the application will strip them.

## Database Schema

The application uses these tables:

- `admin_info` — stores admin credentials
- `user_bank_info` — stores customer account records
- `transaction_details` — stores deposit and withdrawal history

## Best Practices

- Keep your `.env` file private and do not commit it to version control.
- Use strong credentials for MySQL and admin access.
- Use the same `DB_NAME` value as configured in the `.env` file.

## License

This project is provided as a learning example for basic banking operations, MySQL integration, and Python command-line applications.
