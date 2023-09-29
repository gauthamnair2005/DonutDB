# Import modules
import os
import sqlite3
import sys
from prettytable import PrettyTable # For tabular output
from colorama import Fore, Back, Style # For colored prompts

# Define constants
VERSION = "23.9.30"
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
                    result = cursor.fetchall()
                    table = PrettyTable(["Table Name"]) # Create a table with one column
                    table.add_rows(result) # Add the rows from the result
                    print(table) # Print the table
                except sqlite3.Error as err:
                    print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)

            # If the command is 'desc' or 'describe', show the structure of a table
            elif command.startswith("desc") or command.startswith("describe"):
                try:
                    # Split the command into words and get the table name
                    words = command.split()
                    table_name = words[1]

                    # Use PRAGMA table_info to get the details of a table
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    result = cursor.fetchall()
                    
                    # Create a table with column names from PRAGMA table_info output
                    fields = ["cid", "name", "type", "notnull", "dflt_value", "pk"]
                    table = PrettyTable(fields)
                    
                    # Add the rows from the result
                    table.add_rows(result)
                    
                    # Print the table
                    print(table)
                except sqlite3.Error as err:
                    print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)

            # If the command is 'modify' or 'alter', perform the modification or alteration on a table or a column
            elif command.startswith("modify") or command.startswith("alter"):
                try:
                    # Split the command into words and get the table name and column name (if any)
                    words = command.split()
                    table_name = words[1]
                    column_name = words[2] if len(words) > 2 else None

                    # If there is no column name, rename the table to a new name provided by the user
                    if not column_name:
                        new_name = input(f"Enter new name for table {table_name}: ")
                        cursor.execute(f"ALTER TABLE {table_name} RENAME TO {new_name}")
                        conn.commit()
                        print(f"Table {table_name} renamed to {new_name}")

                    # If there is a column name, perform one of the following actions based on user input:
                    # - Rename the column to a new name
                    # - Change the data type of the column
                    # - Add or remove a constraint on the column
                    else:
                        action = input(f"What do you want to do with column {column_name} of table {table_name}?\nOptions: rename, change type, add constraint, remove constraint\nEnter your choice: ")
                        if action == "rename":
                            new_name = input(f"Enter new name for column {column_name}: ")
                            cursor.execute(f"ALTER TABLE {table_name} RENAME COLUMN {column_name} TO {new_name}")
                            conn.commit()
                            print(f"Column {column_name} renamed to {new_name}")
                        elif action == "change type":
                            new_type = input(f"Enter new data type for column {column_name}: ")
                            cursor.execute(f"ALTER TABLE {table_name} ALTER COLUMN {column_name} TYPE {new_type}")
                            conn.commit()
                            print(f"Column {column_name} changed to type {new_type}")
                        elif action == "add constraint":
                            constraint = input(f"Enter constraint for column {column_name}: ")
                            cursor.execute(f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint} ON {column_name}")
                            conn.commit()
                            print(f"Constraint {constraint} added on column {column_name}")
                        elif action == "remove constraint":
                            constraint = input(f"Enter constraint to remove from column {column_name}: ")
                            cursor.execute(f"ALTER TABLE {table_name} DROP CONSTRAINT {constraint} ON {column_name}")
                            conn.commit()
                            print(f"Constraint {constraint} removed from column {column_name}")
                        else:
                            print(Fore.RED + f"Invalid action: {action}" + Style.RESET_ALL)
                except sqlite3.Error as err:
                    print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)

            # If the command is 'exit', close the connection and break out of the loop
            elif command == "exit":
                conn.close()
                break

            # If the command is 'about', print some information about DonutDB
            elif command == "about":
                print(Fore.CYAN + f"DonutDB {VERSION} by {AUTHOR}")
                print("A lightweight and fast relational database management system written in Python")
                print("Enter 'help' for more information" + Style.RESET_ALL)

            # Otherwise, execute the command and commit the changes to the database
            else:
                try:
                    cursor.execute(command)
                    conn.commit()
                except sqlite3.Error as err:
                    print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)

    # Enter a loop to prompt the user to enter a command
    while True:
        # Prompt the user to enter a command
        command = input((Fore.GREEN + PROMPT)).lower()

        # If the user enters 'create database' or any variation of it, ask for the database name and create a connection and a cursor object
        if CREATE_DB in command:
            db_name = input("Enter database name: ")
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            execute_sql(conn, cursor)

        # If the user enters 'enter database', ask for the database name and connect to it
        elif command == "enter database":
            db_name = input("Enter database name: ")
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            execute_sql(conn, cursor)

        # If the user enters 'help', print some help messages
        elif command == "help":
            print(Fore.GREEN + "DonutDB commands:")
            print(f"{CREATE_DB.upper()} - create a new database")
            print("ENTER DATABASE - enter an existing database")
            print("SHOW DATABASES - list all databases in the current directory")
            print("SHOW TABLES - list all tables in the current database")
            print("DESC TABLE - show the structure of a table")
            print("DESCRIBE TABLE - alias for DESC TABLE")
            print("MODIFY TABLE - modify a table or a column in the current database")
            print("ALTER TABLE - alias for MODIFY TABLE")
            print("ABOUT - show information about DonutDB")
            print("EXIT - exit from DonutDB or from a database" + Style.RESET_ALL)
            print()
            print(Fore.YELLOW + "SQL commands:")
            print("You can use any valid SQL commands on a database, such as:")
            print("CREATE TABLE - create a new table")
            print("INSERT INTO - insert data into a table")
            print("SELECT FROM - query data from a table")
            print("UPDATE - update data in a table")
            print("DELETE FROM - delete data from a table")
            print("DROP TABLE - delete a table" + Style.RESET_ALL)

        # If the user enters 'exit', exit from DonutDB
        elif command == "exit":
            sys.exit()

        # Otherwise, print an error message
        else:
            print(Fore.RED + "Invalid command. Enter 'help' for more information." + Style.RESET_ALL)

else :
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
                    result = cursor.fetchall()
                    table = PrettyTable(["Table Name"]) # Create a table with one column
                    table.add_rows(result) # Add the rows from the result
                    print(table) # Print the table
                except sqlite3.Error as err:
                    print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)

            # If the command is 'desc' or 'describe', show the structure of a table
            elif command.startswith("desc") or command.startswith("describe"):
                try:
                    # Split the command into words and get the table name
                    words = command.split()
                    table_name = words[1]

                    # Use PRAGMA table_info to get the details of a table
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    result = cursor.fetchall()
                    
                    # Create a table with column names from PRAGMA table_info output
                    fields = ["cid", "name", "type", "notnull", "dflt_value", "pk"]
                    table = PrettyTable(fields)
                    
                    # Add the rows from the result
                    table.add_rows(result)
                    
                    # Print the table
                    print(table)
                except sqlite3.Error as err:
                    print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)

            # If the command is 'modify' or 'alter', perform the modification or alteration on a table or a column
            elif command.startswith("modify") or command.startswith("alter"):
                try:
                    # Split the command into words and get the table name and column name (if any)
                    words = command.split()
                    table_name = words[1]
                    column_name = words[2] if len(words) > 2 else None

                    # If there is no column name, rename the table to a new name provided by the user
                    if not column_name:
                        new_name = input(f"Enter new name for table {table_name}: ")
                        cursor.execute(f"ALTER TABLE {table_name} RENAME TO {new_name}")
                        conn.commit()
                        print(f"Table {table_name} renamed to {new_name}")

                    # If there is a column name, perform one of the following actions based on user input:
                    # - Rename the column to a new name
                    # - Change the data type of the column
                    # - Add or remove a constraint on the column
                    else:
                        action = input(f"What do you want to do with column {column_name} of table {table_name}?\nOptions: rename, change type, add constraint, remove constraint\nEnter your choice: ")
                        if action == "rename":
                            new_name = input(f"Enter new name for column {column_name}: ")
                            cursor.execute(f"ALTER TABLE {table_name} RENAME COLUMN {column_name} TO {new_name}")
                            conn.commit()
                            print(f"Column {column_name} renamed to {new_name}")
                        elif action == "change type":
                            new_type = input(f"Enter new data type for column {column_name}: ")
                            cursor.execute(f"ALTER TABLE {table_name} ALTER COLUMN {column_name} TYPE {new_type}")
                            conn.commit()
                            print(f"Column {column_name} changed to type {new_type}")
                        elif action == "add constraint":
                            constraint = input(f"Enter constraint for column {column_name}: ")
                            cursor.execute(f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint} ON {column_name}")
                            conn.commit()
                            print(f"Constraint {constraint} added on column {column_name}")
                        elif action == "remove constraint":
                            constraint = input(f"Enter constraint to remove from column {column_name}: ")
                            cursor.execute(f"ALTER TABLE {table_name} DROP CONSTRAINT {constraint} ON {column_name}")
                            conn.commit()
                            print(f"Constraint {constraint} removed from column {column_name}")
                        else:
                            print(Fore.RED + f"Invalid action: {action}" + Style.RESET_ALL)
                except sqlite3.Error as err:
                    print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)

            # If the command is 'exit', close the connection and break out of the loop
            elif command == "exit":
                conn.close()
                break

            # If the command is 'about', print some information about DonutDB
            elif command == "about":
                print(Fore.CYAN + f"DonutDB {VERSION} by {AUTHOR}")
                print("A lightweight and fast relational database management system written in Python")
                print("Enter 'help' for more information" + Style.RESET_ALL)

            # Otherwise, execute the command and commit the changes to the database
            else:
                try:
                    cursor.execute(command)
                    conn.commit()
                except sqlite3.Error as err:
                    print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)

    # Enter a loop to prompt the user to enter a command
    while True:
        # Prompt the user to enter a command
        command = input((Fore.GREEN + PROMPT)).lower()

        # If the user enters 'create database' or any variation of it, ask for the database name and create a connection and a cursor object
        if CREATE_DB in command:
            db_name = input("Enter database name: ")
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            execute_sql(conn, cursor)

        # If the user enters 'enter database', ask for the database name and connect to it
        elif command == "enter database":
            db_name = input("Enter database name: ")
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            execute_sql(conn, cursor)

        # If the user enters 'help', print some help messages
        elif command == "help":
            print(Fore.GREEN + "DonutDB commands:")
            print(f"{CREATE_DB.upper()} - create a new database")
            print("ENTER DATABASE - enter an existing database")
            print("SHOW DATABASES - list all databases in the current directory")
            print("SHOW TABLES - list all tables in the current database")
            print("DESC TABLE - show the structure of a table")
            print("DESCRIBE TABLE - alias for DESC TABLE")
            print("MODIFY TABLE - modify a table or a column in the current database")
            print("ALTER TABLE - alias for MODIFY TABLE")
            print("ABOUT - show information about DonutDB")
            print("EXIT - exit from DonutDB or from a database" + Style.RESET_ALL)
            print()
            print(Fore.YELLOW + "SQL commands:")
            print("You can use any valid SQL commands on a database, such as:")
            print("CREATE TABLE - create a new table")
            print("INSERT INTO - insert data into a table")
            print("SELECT FROM - query data from a table")
            print("UPDATE - update data in a table")
            print("DELETE FROM - delete data from a table")
            print("DROP TABLE - delete a table" + Style.RESET_ALL)

        # If the user enters 'exit', exit from DonutDB
        elif command == "exit":
            sys.exit()

        # Otherwise, print an error message
        else:
            print(Fore.RED + "Invalid command. Enter 'help' for more information." + Style.RESET_ALL)