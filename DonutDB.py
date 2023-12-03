# Import modules
import os
import sqlite3
import sys
from prettytable import PrettyTable # For tabular output
from colorama import Fore, Back, Style # For colored prompts
from tabulate import tabulate # for databases listing in tabular form
import getpass
import hashlib
# Define constants
VERSION = "24.00.00.512p+ Velocity Developer Preview"
AUTHOR = "Gautham Nair"
PROMPT = "DonutDB $ "
CREATE_DB = "create database"
USE_DB = "use"
DATABASE_DIR = "databases"

if sys.platform == "win32":
    # Clear the screen
    os.system("cls")
    if os.path.getsize("ddbnupf") == 0:
        file_path = "ddbnupf"
        file = open(file_path, "w")
        create_password = getpass.getpass("Create Password: ")
        file.write(create_password)
        file.close()
        print()
        # Print some information about DonutDB
        print(Fore.CYAN + f"DonutDB {VERSION} \n - {AUTHOR}")
        print("A lightweight and fast relational database management system written in Python")
        print("Enter 'help' for more information" + Style.RESET_ALL)
        # Define a function to execute SQL commands on a database
        def execute_sql(conn, cursor):
            # Enter a loop to execute SQL commands
            command = ""
            while command != "exit":
                # Prompt the user to enter a command
                command = input((Fore.GREEN + PROMPT))
                # If the command is 'select', print the result of the query in a table format
                if "select" in command or "SELECT" in command:
                    try:
                        cursor.execute(command)
                        result = cursor.fetchall()
                        fields = [desc[0] for desc in cursor.description] # Get the column names
                        table = PrettyTable(fields) # Create a table with the column names
                        table.add_rows(result) # Add the rows from the result
                        print(table) # Print the table
                    except sqlite3.Error as err:
                        print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                elif "desc" in command or "DESC" in command:
                    try:
                        desc_candidate = command.split(" ")[1]
                        cursor.execute(f"PRAGMA table_info({desc_candidate})")
                        rows = cursor.fetchall()
                        desc_table = PrettyTable(["Column ID","Column Name","Data Type","Not Null?","Default Value","Primary Key"])
                        for row in rows:
                            desc_table.add_row(row)
                        print(desc_table)
                    except sqlite3.Error as err:
                        print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                elif "alter" in command or "ALTER" in command:
                    try:
                        cursor.execute(command)
                        print("Table Altered")
                    except sqlite3.Error as err:
                        print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                elif "delete" in command or "DELETE" in command:
                    try:
                        cursor.execute(command)
                        print("Deleted")
                    except sqlite3.Error as err:
                        print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                elif "update" in command or "UPDATE" in command:
                    try:
                        cursor.execute(command)
                        print("Table Updated")
                    except sqlite3.Error as err:
                        print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                elif command == "show databases" or command == "SHOW DATABASES":
                    databases_dir = os.path.join(os.path.dirname(__file__), 'databases')
                    files = os.listdir(databases_dir)
                    print(tabulate([files], headers=['Databases'], tablefmt='orgtbl'))
                # If the command is 'show tables', list the tables in the current database
                elif command == "show tables" or command == "SHOW TABLES":
                    try:
                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                        result = cursor.fetchall()
                        fields = [desc[0] for desc in cursor.description] # Get the column names
                        table = PrettyTable(fields) # Create a table with the column names
                        table.add_rows(result) # Add the rows from the result
                        print(table) # Print the table
                    except sqlite3.Error as err:
                        print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                # If the command is 'exit', break out of the loop and close the connection
                elif command == "exit":
                    print("Exitted the database conection..!")
                    break
                # Otherwise, try to execute the command and commit or rollback depending on success or failure
                elif command == "help":
                    print(Fore.YELLOW + "DonutDB Help")
                    print("-----------------------------------------------------------------------")
                    print("exit - exit the current database connection" + Style.RESET_ALL)
                    print(Fore.WHITE + "create table <t_name> ... - create the table")
                    print("desc - describe command")
                    print("select  - select command ")
                    print("alter  - alter command ")
                    print("update  - update command ")
                    print("show tables - show all the tables available in current database")
                    print(Fore.YELLOW + "-----------------------------------------------------------------------" + Style.RESET_ALL)
                else:
                    try:
                        cursor.execute(command)
                        conn.commit() # Save the changes to the database
                        print(Fore.GREEN + "Command executed successfully.. Changes Commited Successfully" + Style.RESET_ALL)
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

        def use_db(db_name):
            try:
                conn = sqlite3.connect(db_name) # Create a new database file and connect to it
                cursor = conn.cursor() # Create a cursor object from the connection object
                print(Fore.GREEN + f"Database {db_name} connected successfully" + Style.RESET_ALL)
                execute_sql(conn, cursor) # Call the execute_sql function with the connection and cursor objects
            except sqlite3.Error as err:
                print(Fore.RED + f"Database connection failed: {err}" + Style.RESET_ALL)
        # Enter a loop to create databases or exit

        while True:
            # Prompt the user to enter a command
            command = input((Fore.GREEN + PROMPT))
            # If the command starts with 'create database', extract the database name and call the create_db function with it
            if command.startswith(CREATE_DB):
                db_name = command.split(" ")[2]# Remove 'create database' and any whitespace from the command
                db_path = os.path.join(DATABASE_DIR, db_name)
                if db_name: # If there is a database name given, call create_db with it
                    create_db(db_path)
                else: # Otherwise, print an error message
                    print(Fore.RED + "Please enter a valid database name" + Style.RESET_ALL)
            # If the command is 'exit', break out of the loop and exit the program
            elif command.startswith(USE_DB):
                db_name = command.split(" ")[1] # Remove 'use' and any whitespace from the command
                db_path = os.path.join(DATABASE_DIR, db_name)
                if os.path.isfile(db_path):
                    if db_name: # If there is a database name given, call use_db with it
                        use_db(db_path)
                    else: # Otherwise, print an error message
                        print(Fore.RED + "Database Corrupted of Unreadable" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Database not found, use " + Style.RESET_ALL + Fore.GREEN + "create database",db_name + Style.RESET_ALL + Fore.RED + " instead to create one.!" + Style.RESET_ALL)
            # If the command is 'exit', break out of the loop and exit the program
            elif command == "show databases" or command == "SHOW DATABASES":
                databases_dir = os.path.join(os.path.dirname(__file__), 'databases')
                files = os.listdir(databases_dir)
                print(tabulate([files], headers=['Databases'], tablefmt='orgtbl'))
            elif command == "exit":
                break
            elif "drop database" in command:
                drop_name = command.split(" ")[2]
                path_drop = os.path.join(DATABASE_DIR, drop_name)
                os.remove(path_drop)
            elif command == "help":
                print(Fore.YELLOW + "DonutDB Help")
                print("----------------------------------------------------")
                print("exit - quit the application")
                print("create database <db_name> - create the database")
                print("use <db_name> - use a particular database")
                print("show databases - show all the databases available")
                print("----------------------------------------------------" + Style.RESET_ALL)
            else:
                print(Fore.RED + "Invalid command" + Style.RESET_ALL)
    else:
        with open("ddbnupf","r") as f:
            correct_password = f.read().strip()
        correct_password = hashlib.sha256(correct_password.encode()).hexdigest()
        user_password = getpass.getpass("Enter Password: ")
        user_password = hashlib.sha256(user_password.encode()).hexdigest()
        if user_password == correct_password:
            print("Access Granted..!")
            print()
            # Print some information about DonutDB
            print(Fore.CYAN + f"DonutDB {VERSION} \n - {AUTHOR}")
            print("A lightweight and fast relational database management system written in Python")
            print("Enter 'help' for more information" + Style.RESET_ALL)
            # Define a function to execute SQL commands on a database
            def execute_sql(conn, cursor):
                # Enter a loop to execute SQL commands
                command = ""
                while command != "exit":
                    # Prompt the user to enter a command
                    command = input((Fore.GREEN + PROMPT))
                    # If the command is 'select', print the result of the query in a table format
                    if "select" in command or "SELECT" in command:
                        try:
                            cursor.execute(command)
                            result = cursor.fetchall()
                            fields = [desc[0] for desc in cursor.description] # Get the column names
                            table = PrettyTable(fields) # Create a table with the column names
                            table.add_rows(result) # Add the rows from the result
                            print(table) # Print the table
                        except sqlite3.Error as err:
                            print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                    elif "desc" in command or "DESC" in command:
                        try:
                            desc_candidate = command.split(" ")[1]
                            cursor.execute(f"PRAGMA table_info({desc_candidate})")
                            rows = cursor.fetchall()
                            desc_table = PrettyTable(["Column ID","Column Name","Data Type","Not Null?","Default Value","Primary Key"])
                            for row in rows:
                                desc_table.add_row(row)
                            print(desc_table)
                        except sqlite3.Error as err:
                            print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                    elif "alter" in command or "ALTER" in command:
                        try:
                            cursor.execute(command)
                            print("Table Altered")
                        except sqlite3.Error as err:
                            print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                    elif "delete" in command or "DELETE" in command:
                        try:
                            cursor.execute(command)
                            print("Deleted")
                        except sqlite3.Error as err:
                            print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                    elif "update" in command or "UPDATE" in command:
                        try:
                            cursor.execute(command)
                            print("Table Updated")
                        except sqlite3.Error as err:
                            print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                    elif command == "show databases" or command == "SHOW DATABASES":
                        databases_dir = os.path.join(os.path.dirname(__file__), 'databases')
                        files = os.listdir(databases_dir)
                        print(tabulate([files], headers=['Databases'], tablefmt='orgtbl'))
                    # If the command is 'show tables', list the tables in the current database
                    elif command == "show tables" or command == "SHOW TABLES":
                        try:
                            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                            result = cursor.fetchall()
                            fields = [desc[0] for desc in cursor.description] # Get the column names
                            table = PrettyTable(fields) # Create a table with the column names
                            table.add_rows(result) # Add the rows from the result
                            print(table) # Print the table
                        except sqlite3.Error as err:
                            print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                    # If the command is 'exit', break out of the loop and close the connection
                    elif command == "exit":
                        print("Exitted the database conection..!")
                        break
                    # Otherwise, try to execute the command and commit or rollback depending on success or failure
                    elif command == "help":
                        print(Fore.YELLOW + "DonutDB Help")
                        print("-----------------------------------------------------------------------")
                        print("exit - exit the current database connection" + Style.RESET_ALL)
                        print(Fore.WHITE + "create table <t_name> ... - create the table")
                        print("desc - describe command")
                        print("select  - select command ")
                        print("alter  - alter command ")
                        print("update  - update command ")
                        print("show tables - show all the tables available in current database")
                        print(Fore.YELLOW + "-----------------------------------------------------------------------" + Style.RESET_ALL)
                    else:
                        try:
                            cursor.execute(command)
                            conn.commit() # Save the changes to the database
                            print(Fore.GREEN + "Command executed successfully.. Changes Commited Successfully" + Style.RESET_ALL)
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

            def use_db(db_name):
                try:
                    conn = sqlite3.connect(db_name) # Create a new database file and connect to it
                    cursor = conn.cursor() # Create a cursor object from the connection object
                    print(Fore.GREEN + f"Database {db_name} connected successfully" + Style.RESET_ALL)
                    execute_sql(conn, cursor) # Call the execute_sql function with the connection and cursor objects
                except sqlite3.Error as err:
                    print(Fore.RED + f"Database connection failed: {err}" + Style.RESET_ALL)
            # Enter a loop to create databases or exit

            while True:
                # Prompt the user to enter a command
                command = input((Fore.GREEN + PROMPT))
                # If the command starts with 'create database', extract the database name and call the create_db function with it
                if command.startswith(CREATE_DB):
                    db_name = command.split(" ")[2]# Remove 'create database' and any whitespace from the command
                    db_path = os.path.join(DATABASE_DIR, db_name)
                    if db_name: # If there is a database name given, call create_db with it
                        create_db(db_path)
                    else: # Otherwise, print an error message
                        print(Fore.RED + "Please enter a valid database name" + Style.RESET_ALL)
                # If the command is 'exit', break out of the loop and exit the program
                elif command.startswith(USE_DB):
                    db_name = command.split(" ")[1] # Remove 'use' and any whitespace from the command
                    db_path = os.path.join(DATABASE_DIR, db_name)
                    if os.path.isfile(db_path):
                        if db_name: # If there is a database name given, call use_db with it
                            use_db(db_path)
                        else: # Otherwise, print an error message
                            print(Fore.RED + "Database Corrupted of Unreadable" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + "Database not found, use " + Style.RESET_ALL + Fore.GREEN + "create database",db_name + Style.RESET_ALL + Fore.RED + " instead to create one.!" + Style.RESET_ALL)
                # If the command is 'exit', break out of the loop and exit the program
                elif command == "show databases" or command == "SHOW DATABASES":
                    databases_dir = os.path.join(os.path.dirname(__file__), 'databases')
                    files = os.listdir(databases_dir)
                    print(tabulate([files], headers=['Databases'], tablefmt='orgtbl'))
                elif command == "exit":
                    break
                elif "drop database" in command:
                    drop_name = command.split(" ")[2]
                    path_drop = os.path.join(DATABASE_DIR, drop_name)
                    os.remove(path_drop)
                elif command == "help":
                    print(Fore.YELLOW + "DonutDB Help")
                    print("----------------------------------------------------")
                    print("exit - quit the application")
                    print("create database <db_name> - create the database")
                    print("use <db_name> - use a particular database")
                    print("show databases - show all the databases available")
                    print("----------------------------------------------------" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Invalid command" + Style.RESET_ALL)
        else:
            print("Access Denied..!")
else:
    # Clear the screen
    os.system("clear")
    if os.path.getsize("ddbnupf") == 0:
        file_path = "ddbnupf"
        file = open(file_path, "w")
        create_password = getpass.getpass("Create Password: ")
        file.write(create_password)
        file.close()
        print()
        # Print some information about DonutDB
        print(Fore.CYAN + f"DonutDB {VERSION} \n - {AUTHOR}")
        print("A lightweight and fast relational database management system written in Python")
        print("Enter 'help' for more information" + Style.RESET_ALL)
        # Define a function to execute SQL commands on a database
        def execute_sql(conn, cursor):
            # Enter a loop to execute SQL commands
            command = ""
            while command != "exit":
                # Prompt the user to enter a command
                command = input((Fore.GREEN + PROMPT))
                # If the command is 'select', print the result of the query in a table format
                if "select" in command or "SELECT" in command:
                    try:
                        cursor.execute(command)
                        result = cursor.fetchall()
                        fields = [desc[0] for desc in cursor.description] # Get the column names
                        table = PrettyTable(fields) # Create a table with the column names
                        table.add_rows(result) # Add the rows from the result
                        print(table) # Print the table
                    except sqlite3.Error as err:
                        print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                elif "desc" in command or "DESC" in command:
                    try:
                        desc_candidate = command.split(" ")[1]
                        cursor.execute(f"PRAGMA table_info({desc_candidate})")
                        rows = cursor.fetchall()
                        desc_table = PrettyTable(["Column ID","Column Name","Data Type","Not Null?","Default Value","Primary Key"])
                        for row in rows:
                            desc_table.add_row(row)
                        print(desc_table)
                    except sqlite3.Error as err:
                        print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                elif "alter" in command or "ALTER" in command:
                    try:
                        cursor.execute(command)
                        print("Table Altered")
                    except sqlite3.Error as err:
                        print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                elif "delete" in command or "DELETE" in command:
                    try:
                        cursor.execute(command)
                        print("Deleted")
                    except sqlite3.Error as err:
                        print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                elif "update" in command or "UPDATE" in command:
                    try:
                        cursor.execute(command)
                        print("Table Updated")
                    except sqlite3.Error as err:
                        print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                elif command == "show databases" or command == "SHOW DATABASES":
                    databases_dir = os.path.join(os.path.dirname(__file__), 'databases')
                    files = os.listdir(databases_dir)
                    print(tabulate([files], headers=['Databases'], tablefmt='orgtbl'))
                # If the command is 'show tables', list the tables in the current database
                elif command == "show tables" or command == "SHOW TABLES":
                    try:
                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                        result = cursor.fetchall()
                        fields = [desc[0] for desc in cursor.description] # Get the column names
                        table = PrettyTable(fields) # Create a table with the column names
                        table.add_rows(result) # Add the rows from the result
                        print(table) # Print the table
                    except sqlite3.Error as err:
                        print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                # If the command is 'exit', break out of the loop and close the connection
                elif command == "exit":
                    print("Exitted the database conection..!")
                    break
                # Otherwise, try to execute the command and commit or rollback depending on success or failure
                elif command == "help":
                    print(Fore.YELLOW + "DonutDB Help")
                    print("-----------------------------------------------------------------------")
                    print("exit - exit the current database connection" + Style.RESET_ALL)
                    print(Fore.WHITE + "create table <t_name> ... - create the table")
                    print("desc - describe command")
                    print("select  - select command ")
                    print("alter  - alter command ")
                    print("update  - update command ")
                    print("show tables - show all the tables available in current database")
                    print(Fore.YELLOW + "-----------------------------------------------------------------------" + Style.RESET_ALL)
                else:
                    try:
                        cursor.execute(command)
                        conn.commit() # Save the changes to the database
                        print(Fore.GREEN + "Command executed successfully.. Changes Commited Successfully" + Style.RESET_ALL)
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

        def use_db(db_name):
            try:
                conn = sqlite3.connect(db_name) # Create a new database file and connect to it
                cursor = conn.cursor() # Create a cursor object from the connection object
                print(Fore.GREEN + f"Database {db_name} connected successfully" + Style.RESET_ALL)
                execute_sql(conn, cursor) # Call the execute_sql function with the connection and cursor objects
            except sqlite3.Error as err:
                print(Fore.RED + f"Database connection failed: {err}" + Style.RESET_ALL)
        # Enter a loop to create databases or exit

        while True:
            # Prompt the user to enter a command
            command = input((Fore.GREEN + PROMPT))
            # If the command starts with 'create database', extract the database name and call the create_db function with it
            if command.startswith(CREATE_DB):
                db_name = command.split(" ")[2]# Remove 'create database' and any whitespace from the command
                db_path = os.path.join(DATABASE_DIR, db_name)
                if db_name: # If there is a database name given, call create_db with it
                    create_db(db_path)
                else: # Otherwise, print an error message
                    print(Fore.RED + "Please enter a valid database name" + Style.RESET_ALL)
            # If the command is 'exit', break out of the loop and exit the program
            elif command.startswith(USE_DB):
                db_name = command.split(" ")[1] # Remove 'use' and any whitespace from the command
                db_path = os.path.join(DATABASE_DIR, db_name)
                if os.path.isfile(db_path):
                    if db_name: # If there is a database name given, call use_db with it
                        use_db(db_path)
                    else: # Otherwise, print an error message
                        print(Fore.RED + "Database Corrupted of Unreadable" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Database not found, use " + Style.RESET_ALL + Fore.GREEN + "create database",db_name + Style.RESET_ALL + Fore.RED + " instead to create one.!" + Style.RESET_ALL)
            # If the command is 'exit', break out of the loop and exit the program
            elif command == "show databases" or command == "SHOW DATABASES":
                databases_dir = os.path.join(os.path.dirname(__file__), 'databases')
                files = os.listdir(databases_dir)
                print(tabulate([files], headers=['Databases'], tablefmt='orgtbl'))
            elif command == "exit":
                break
            elif "drop database" in command:
                drop_name = command.split(" ")[2]
                path_drop = os.path.join(DATABASE_DIR, drop_name)
                os.remove(path_drop)
            elif command == "help":
                print(Fore.YELLOW + "DonutDB Help")
                print("----------------------------------------------------")
                print("exit - quit the application")
                print("create database <db_name> - create the database")
                print("use <db_name> - use a particular database")
                print("show databases - show all the databases available")
                print("----------------------------------------------------" + Style.RESET_ALL)
            else:
                print(Fore.RED + "Invalid command" + Style.RESET_ALL)
    else:
        with open("ddbnupf","r") as f:
            correct_password = f.read().strip()
        correct_password = hashlib.sha256(correct_password.encode()).hexdigest()
        user_password = getpass.getpass("Enter Password: ")
        user_password = hashlib.sha256(user_password.encode()).hexdigest()
        if user_password == correct_password:
            print("Access Granted..!")
            print()
            # Print some information about DonutDB
            print(Fore.CYAN + f"DonutDB {VERSION} \n - {AUTHOR}")
            print("A lightweight and fast relational database management system written in Python")
            print("Enter 'help' for more information" + Style.RESET_ALL)
            # Define a function to execute SQL commands on a database
            def execute_sql(conn, cursor):
                # Enter a loop to execute SQL commands
                command = ""
                while command != "exit":
                    # Prompt the user to enter a command
                    command = input((Fore.GREEN + PROMPT))
                    # If the command is 'select', print the result of the query in a table format
                    if "select" in command or "SELECT" in command:
                        try:
                            cursor.execute(command)
                            result = cursor.fetchall()
                            fields = [desc[0] for desc in cursor.description] # Get the column names
                            table = PrettyTable(fields) # Create a table with the column names
                            table.add_rows(result) # Add the rows from the result
                            print(table) # Print the table
                        except sqlite3.Error as err:
                            print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                    elif "desc" in command or "DESC" in command:
                        try:
                            desc_candidate = command.split(" ")[1]
                            cursor.execute(f"PRAGMA table_info({desc_candidate})")
                            rows = cursor.fetchall()
                            desc_table = PrettyTable(["Column ID","Column Name","Data Type","Not Null?","Default Value","Primary Key"])
                            for row in rows:
                                desc_table.add_row(row)
                            print(desc_table)
                        except sqlite3.Error as err:
                            print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                    elif "alter" in command or "ALTER" in command:
                        try:
                            cursor.execute(command)
                            print("Table Altered")
                        except sqlite3.Error as err:
                            print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                    elif "delete" in command or "DELETE" in command:
                        try:
                            cursor.execute(command)
                            print("Deleted")
                        except sqlite3.Error as err:
                            print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                    elif "update" in command or "UPDATE" in command:
                        try:
                            cursor.execute(command)
                            print("Table Updated")
                        except sqlite3.Error as err:
                            print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                    elif command == "show databases" or command == "SHOW DATABASES":
                        databases_dir = os.path.join(os.path.dirname(__file__), 'databases')
                        files = os.listdir(databases_dir)
                        print(tabulate([files], headers=['Databases'], tablefmt='orgtbl'))
                    # If the command is 'show tables', list the tables in the current database
                    elif command == "show tables" or command == "SHOW TABLES":
                        try:
                            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                            result = cursor.fetchall()
                            fields = [desc[0] for desc in cursor.description] # Get the column names
                            table = PrettyTable(fields) # Create a table with the column names
                            table.add_rows(result) # Add the rows from the result
                            print(table) # Print the table
                        except sqlite3.Error as err:
                            print(Fore.RED + f"Invalid query: {err}" + Style.RESET_ALL)
                    # If the command is 'exit', break out of the loop and close the connection
                    elif command == "exit":
                        print("Exitted the database conection..!")
                        break
                    # Otherwise, try to execute the command and commit or rollback depending on success or failure
                    elif command == "help":
                        print(Fore.YELLOW + "DonutDB Help")
                        print("-----------------------------------------------------------------------")
                        print("exit - exit the current database connection" + Style.RESET_ALL)
                        print(Fore.WHITE + "create table <t_name> ... - create the table")
                        print("desc - describe command")
                        print("select  - select command ")
                        print("alter  - alter command ")
                        print("update  - update command ")
                        print("show tables - show all the tables available in current database")
                        print(Fore.YELLOW + "-----------------------------------------------------------------------" + Style.RESET_ALL)
                    else:
                        try:
                            cursor.execute(command)
                            conn.commit() # Save the changes to the database
                            print(Fore.GREEN + "Command executed successfully.. Changes Commited Successfully" + Style.RESET_ALL)
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

            def use_db(db_name):
                try:
                    conn = sqlite3.connect(db_name) # Create a new database file and connect to it
                    cursor = conn.cursor() # Create a cursor object from the connection object
                    print(Fore.GREEN + f"Database {db_name} connected successfully" + Style.RESET_ALL)
                    execute_sql(conn, cursor) # Call the execute_sql function with the connection and cursor objects
                except sqlite3.Error as err:
                    print(Fore.RED + f"Database connection failed: {err}" + Style.RESET_ALL)
            # Enter a loop to create databases or exit

            while True:
                # Prompt the user to enter a command
                command = input((Fore.GREEN + PROMPT))
                # If the command starts with 'create database', extract the database name and call the create_db function with it
                if command.startswith(CREATE_DB):
                    db_name = command.split(" ")[2]# Remove 'create database' and any whitespace from the command
                    db_path = os.path.join(DATABASE_DIR, db_name)
                    if db_name: # If there is a database name given, call create_db with it
                        create_db(db_path)
                    else: # Otherwise, print an error message
                        print(Fore.RED + "Please enter a valid database name" + Style.RESET_ALL)
                # If the command is 'exit', break out of the loop and exit the program
                elif command.startswith(USE_DB):
                    db_name = command.split(" ")[1] # Remove 'use' and any whitespace from the command
                    db_path = os.path.join(DATABASE_DIR, db_name)
                    if os.path.isfile(db_path):
                        if db_name: # If there is a database name given, call use_db with it
                            use_db(db_path)
                        else: # Otherwise, print an error message
                            print(Fore.RED + "Database Corrupted of Unreadable" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + "Database not found, use " + Style.RESET_ALL + Fore.GREEN + "create database",db_name + Style.RESET_ALL + Fore.RED + " instead to create one.!" + Style.RESET_ALL)
                # If the command is 'exit', break out of the loop and exit the program
                elif command == "show databases" or command == "SHOW DATABASES":
                    databases_dir = os.path.join(os.path.dirname(__file__), 'databases')
                    files = os.listdir(databases_dir)
                    print(tabulate([files], headers=['Databases'], tablefmt='orgtbl'))
                elif command == "exit":
                    break
                elif "drop database" in command:
                    drop_name = command.split(" ")[2]
                    path_drop = os.path.join(DATABASE_DIR, drop_name)
                    os.remove(path_drop)
                elif command == "help":
                    print(Fore.YELLOW + "DonutDB Help")
                    print("----------------------------------------------------")
                    print("exit - quit the application")
                    print("create database <db_name> - create the database")
                    print("use <db_name> - use a particular database")
                    print("show databases - show all the databases available")
                    print("----------------------------------------------------" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Invalid command" + Style.RESET_ALL)
        else:
            print("Access Denied..!")