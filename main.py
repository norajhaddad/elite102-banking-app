import sqlite3


def initialize_database():
    # Open the database file. SQLite creates it if it does not exist.
    connection = sqlite3.connect("banking.db")
    cursor = connection.cursor()

    # Create the accounts table if it does not already exist.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            balance REAL NOT NULL CHECK (balance >= 0)
        )
    """)

    # Create the transactions table if it does not already exist.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)

    # Save changes and close the database.
    connection.commit()
    connection.close()


def add_transaction(account_id, transaction_type, amount):
    # Open the database.
    connection = sqlite3.connect("banking.db")
    cursor = connection.cursor()

    # Add a transaction record.
    cursor.execute(
        "INSERT INTO transactions (account_id, transaction_type, amount) VALUES (?, ?, ?)",
        (account_id, transaction_type, amount)
    )

    # Save changes and close the database.
    connection.commit()
    connection.close()


def create_account(name, initial_deposit):
    # Do not allow a negative starting balance bc...you can't have a negative initial balance-.
    if initial_deposit < 0:
        print("Initial deposit cannot be negative.")
        return None

    # Open the database.
    connection = sqlite3.connect("banking.db")
    cursor = connection.cursor()

    # Insert the new account.
    cursor.execute(
        "INSERT INTO accounts (name, balance) VALUES (?, ?)",
        (name, initial_deposit)
    )

    # Save the account and get its ID.
    connection.commit()
    account_id = cursor.lastrowid
    connection.close()

    # Record the account creation in transactions.
    add_transaction(account_id, "create", initial_deposit)

    print(f"Account created for {name}. Account ID: {account_id}")
    return account_id


def deposit_money(account_id, amount):
    # Deposit amount must be greater than 0.
    if amount <= 0:
        print("Deposit amount must be greater than 0.")
        return False

    # Open the database.
    connection = sqlite3.connect("banking.db")
    cursor = connection.cursor()

    # Find the account balance.
    cursor.execute(
        "SELECT balance FROM accounts WHERE id = ?",
        (account_id,)
    )
    row = cursor.fetchone()

    # Stop if account does not exist.
    if row is None:
        connection.close()
        print("Account not found.")
        return False

    # Calculate the new balance.
    current_balance = row[0]
    new_balance = current_balance + amount

    # Update the account balance.
    cursor.execute(
        "UPDATE accounts SET balance = ? WHERE id = ?",
        (new_balance, account_id)
    )

    # Save changes and close the database.
    connection.commit()
    connection.close()

    # Record the deposit in transactions.
    add_transaction(account_id, "deposit", amount)

    print(f"Deposit successful. New balance: {new_balance}")
    return True


def withdraw_money(account_id, amount):
    # Withdrawal amount must be greater than 0.
    if amount <= 0:
        print("Withdrawal amount must be greater than 0.")
        return False

    # Open the database.
    connection = sqlite3.connect("banking.db")
    cursor = connection.cursor()

    # Find the account balance.
    cursor.execute(
        "SELECT balance FROM accounts WHERE id = ?",
        (account_id,)
    )
    row = cursor.fetchone()

    # Stop if account does not exist.
    if row is None:
        connection.close()
        print("Account not found.")
        return False

    current_balance = row[0]

    # Do not allow overdrawing.
    if amount > current_balance:
        connection.close()
        print("Insufficient funds.")
        return False

    # Calculate the new balance.
    new_balance = current_balance - amount

    # Update the account balance.
    cursor.execute(
        "UPDATE accounts SET balance = ? WHERE id = ?",
        (new_balance, account_id)
    )

    # Save changes and close the db.
    connection.commit()
    connection.close()

    # Record the withdrawal in transactions.
    add_transaction(account_id, "withdraw", amount)

    print(f"Withdrawal successful. New balance: {new_balance}")
    return True


def check_balance(account_id):
    # Open the database.
    connection = sqlite3.connect("banking.db")
    cursor = connection.cursor()

    # Look up the account.
    cursor.execute(
        "SELECT name, balance FROM accounts WHERE id = ?",
        (account_id,)
    )
    row = cursor.fetchone()

    # Close the database.
    connection.close()

    if row is None:
        print("Account not found.")
        return None

    name = row[0]
    balance = row[1]

    print(f"Account: {name}")
    print(f"Current balance: {balance}")
    return balance


def list_accounts():
    # Open the database.
    connection = sqlite3.connect("banking.db")
    cursor = connection.cursor()

    # Get all accounts.
    cursor.execute("SELECT id, name, balance FROM accounts")
    rows = cursor.fetchall()

    # Close the database.
    connection.close()

    if not rows:
        print("No accounts found.")
        return

    print("\nAccounts:")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Balance: {row[2]}")


def show_welcome_menu():
    print("\n~~~ Welcome to the Banking System! ~~~")
    print("1. Create account")
    print("2. Deposit money")
    print("3. Withdraw money")
    print("4. Check balance")
    print("5. List accounts")
    print("6. Exit")


def main():
    # Make sure the database and tables exist before the menu starts.
    initialize_database()

    # Keep showing the menu until the user chooses Exit.
    while True:
        show_welcome_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter account holder name: ")

            try:
                initial_deposit = float(input("Enter initial deposit: "))
            except ValueError:
                print("Please enter a valid number.")
                continue

            create_account(name, initial_deposit)

        elif choice == "2":
            try:
                account_id = int(input("Enter account ID: "))
                amount = float(input("Enter deposit amount: "))
            except ValueError:
                print("Please enter valid numbers.")
                continue

            deposit_money(account_id, amount)

        elif choice == "3":
            try:
                account_id = int(input("Enter account ID: "))
                amount = float(input("Enter withdrawal amount: "))
            except ValueError:
                print("Please enter valid numbers.")
                continue

            withdraw_money(account_id, amount)

        elif choice == "4":
            try:
                account_id = int(input("Enter account ID: "))
            except ValueError:
                print("Please enter a valid account ID.")
                continue

            check_balance(account_id)

        elif choice == "5":
            list_accounts()

        elif choice == "6":
            print("Thank you for using the Banking System.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


main()