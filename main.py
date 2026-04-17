import sqlite3

def initialize_database():
    connection = sqlite3.connect("banking.db") #open database file named banking.db
    cursor = connection.cursor() # create a cursor so that Python can send SQL commands to database

    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS accounts (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   balance REAL NOT NULL CHECK (balance >= 0)
                   )
            """) #runs a SQL commmand to create accounts table; only if it doesn't already exist
    connection.commit() #save table creation to database file
    connection.close() #close database connection when finished
    print("Database and accounts table are ready!") #basic message to test the code's functionality

def create_account(name, initial_deposit): #more functional account instead of basic creation before
    if initial_deposit < 0:
        print("Initial deposit cannot be negative.")
        return None
    connection = sqlite3.connect("banking.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO accounts (name, balance) VALUES (?, ?)", 
        (name, initial_deposit)
    )
    connection.commit()
    account_id = cursor.lastrowid
    connection.close()

    print(f"Account created for {name}. Account ID: {account_id}")
    return account_id

def deposit_money(account_id, amount):
    if amount <= 0:
        print("Deposit amount must be greater than 0.")
        return False
    connection = sqlite3.connect("banking.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT balance FROM accounts WHERE id = ?",
        (account_id,)
    )
    row = cursor.fetchone()

    if row is None:
        connection.close()
        print("Account not found.")
        return False
    
    current_balance = row[0]
    new_balance = current_balance + amount

    cursor.execute(
        "UPDATE accounts SET balance = ? WHERE id = ?",
        (new_balance, account_id)
    )

    connection.commit()
    connection.close()
    print(f"Deposit successful. New balance: {new_balance}")
    return True

def withdraw_money(account_id, amount):
    if amount <= 0:
        print("Withdrawal amount has to be more than 0.")
        return False
    connection = sqlite3.connect("banking.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT balance FROM accounts WHERE id = ?",
        (account_id,)
    )
    row = cursor.fetchone()

    if row is None:
        connection.close()
        print("Account not found.")
        return False
    
    current_balance = row[0]

    if amount > current_balance:
        connection.close()
        print("Insufficient funds.")
        return False
    
    new_balance = current_balance - amount

    cursor.execute(
        "UPDATE accounts SET balance = ? WHERE id = ?",
        (new_balance, account_id)
    )
    connection.commit()
    connection.close()

    print(f"Withdrawal successful. New balance: {new_balance}")
    return True


def show_welcome_menu():
    print("\n~~~ Welcome to the Banking System! ~~~")
    print("1. Create account")
    print("2. Deposit money")
    print("3. Withdraw money")
    print("4. Check balance")
    print("5. List accounts")
    print("6. Exit")


def main(): 
    initialize_database() #calls the function that creates the db and table
    account_id = create_account("John Doe", 100.0)
    if account_id is not None:
        deposit_money(account_id, 50.0)
        withdraw_money(account_id, 30.0)

    show_welcome_menu()

main() #creates db and table, adds test account, and shows menu