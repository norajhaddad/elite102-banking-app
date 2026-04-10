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

def show_welcome_menu():
    print("/n~~~ Welcome to the Banking System! ~~~")
    print("1. Create account")
    print("2. Deposit money")
    print("3. Withdraw money")
    print("4. Check balance")
    print("5. List accounts")
    print("6. Exit")

def add_test_account(): #opens the db
    connection = sqlite3.connect("banking.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSET INTO accounts (name, balance) VALUES ('Random Person', 100.0)" #inserts one test account into the table 
    )
    connection.commit() #saves changes
    connection.close() #closes db
    print("Test account added.")

def main(): #not necessary? but may be useful for future use/ultimately making code shorter
    initialize_database() #calls the function that creates the db and table
    add_test_account() #adds test account
    show_welcome_menu() #should show the menu in the terminal


main() #creates db and table, adds test account, and shows menu