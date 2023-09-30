# Import modules
import os
import sqlite3
import sys
from prettytable import PrettyTable # For tabular output
from colorama import Fore, Back, Style # For colored prompts
# Define constants
VERSION = "24.00.00.128+ Velocity Developer Preview"
AUTHOR = "Gautham Nair"
PROMPT = "DonutDB $ "
CREATE_DB = "create database"
if sys.platform == "win32":
    # Clear the screen
    os.system("cls")
    # Print some information about DonutDB
    print(Fore.CYAN + f"Welcome to DonutDB {VERSION} by {AUTHOR}")
    print("A lightweight and fast relational database management system written in Python")
    print("Enter 'help' for more information" + Style.RESET_ALL)
    # Define a function to execute SQL commands on a database
    def execute_sql(conn, cursor):
        # Enter a loop to execute SQL commands
        while True:
            # Prompt the user to enter a command
            command = input((Fore.GREEN + PROMPT)).lower()
            # If the command is 'select', print the result of the query in a table format
            if "select" in command:
                try:
                    cursor.execute(command)
                    result = cursor.fetchall()
                    fields = [desc[0] for desc in cursor.description] # Get the column names
                    table = PrettyTable(fields) # Create a table with the column names
                    table.add_rows(result) # Add the rows from the result
                    print(table) # Print the table
                except sqlite3.Error as err:
                    print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
            # If the command is 'show databases', list the files in the current directory
            elif command == "show databases":
                files = os.listdir()
                print(files)
            # If the command is 'show tables', list the tables in the current database
            elif command == "show tables":
                try:
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = cursor.fetchall()
                    print(tables)
                except sqlite3.Error as err:
                    print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
            # If the command is 'exit', break out of the loop and close the connection
            elif command == "exit":
                break
            # Otherwise, try to execute the command and commit or rollback depending on success or failure
            else:
                try:
                    cursor.execute(command)
                    conn.commit() # Save the changes to the database
                    print(Fore.GREEN + "Command executed successfully" + Style.RESET_ALL)
                except sqlite3.Error as err:
                    conn.rollback() # Undo the changes to the database
                    print(Fore.RED + f"Command failed: {err}" + Style.RESET_ALL)
        # Close the connection when done
        conn.close()
    # Define a function to create a new database file and connect to it
    def create_db(db_name):
        try:
            conn = sqlite3.connect(db_name) # Create a new database file and connect to it
            cursor = conn.cursor() # Create a cursor object from the connection object
            print(Fore.GREEN + f"Database {db_name} created successfully" + Style.RESET_ALL)
            execute_sql(conn, cursor) # Call the execute_sql function with the connection and cursor objects
        except sqlite3.Error as err:
            print(Fore.RED + f"Database creation failed: {err}" + Style.RESET_ALL)
    # Enter a loop to create databases or exit
    while True:
        # Prompt the user to enter a command
        command = input((Fore.GREEN + PROMPT)).lower()
        # If the command starts with 'create database', extract the database name and call the create_db function with it
        if command.startswith(CREATE_DB):
            db_name = command[len(CREATE_DB):].strip() # Remove 'create database' and any whitespace from the command
            if db_name: # If there is a database name given, call create_db with it
                create_db(db_name)
            else: # Otherwise, print an error message
                print(Fore.RED + "Please enter a valid database name" + Style.RESET_ALL)
        # If the command is 'exit', break out of the loop and exit the program
        elif command == "exit":
            break
        # Otherwise, print an error message
        else:
            print(Fore.RED + "Invalid command" + Style.RESET_ALL)
