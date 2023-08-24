import sqlite3
import os
import sys

if sys.platform == "win32":
    os.system('cls')
    print("DonutDB 2023 Velocity")
    print("Version 23.8.20")
    print("Gautham Nair")
    print("-" * 80)
    command = ""
    while command != "quit" or command != "exit":
        command = input("DonutDB $ ")
        if command == "CREATE DATABASE" or command == "create database" or command == "Create database" or command == "Create Database" or command == "Create DataBase":
            database = input("DonutDB $ (Create Database) ")
            print("Please wait while we create and connect to Database ",database)
            print("Done!")
            connection = sqlite3.connect(database)
            cursor = connection.cursor()
            command = ""
            while command != "exit" or command != "quit":
                command = input("DonutDB $ ")
                connection = sqlite3.connect(database)
                cursor = connection.cursor()
                if "select" in command:
                    cursor.execute(command)
                    connection.commit()
                    print(cursor.fetchall())
                elif command == "show databases":
                    os.system('dir /w')
                elif command == "exit":
                    connection.close()
                    break
                elif command == "about":
                    print("DonutDB 2023 Velocity")
                    print("v23.8.20")
                    print("Gautham Nair")
                else:
                    cursor.execute(command)
                    connection.commit()
            break
        elif command == "enter database":
            database = input("Enter database name: ")
            while command != "exit" or command != "quit":
                command = input("DonutDB $ ")
                connection = sqlite3.connect(database)
                cursor = connection.cursor()
                if "select" in command:
                    cursor.execute(command)
                    connection.commit()
                    print(cursor.fetchall())
                elif command == "show databases":
                    os.system('dir /w')
                elif command == "exit":
                    connection.close()
                    break
                elif command == "about":
                    print("DonutDB 2023 Velocity")
                    print("v23.8.20")
                    print("Gautham Nair")
                else:
                    cursor.execute(command)
                    connection.commit()
            break
        else:
            print("Terminating DonutDB")
            break
                
else:
    os.system('clear')
    print("DonutDB 2023 Velocity")
    print("Version 23.8.20")
    print("-" * 80)
    command = ""
    while command != "quit" or command != "exit":
        command = input("DonutDB $ ")
        if command == "CREATE DATABASE" or command == "create database" or command == "Create database" or command == "Create Database" or command == "Create DataBase":
            database = input("DonutDB $ (Create Database) ")
            print("Please wait while we create and connect to Database ",database)
            print("Done!")
            connection = sqlite3.connect(database)
            cursor = connection.cursor()
            command = ""
            while command != "exit" or command != "quit":
                command = input("DonutDB $ ")
                connection = sqlite3.connect(database)
                cursor = connection.cursor()
                if "select" in command:
                    cursor.execute(command)
                    connection.commit()
                    print(cursor.fetchall())
                elif command == "show databases":
                    os.system('ls')
                elif command == "exit":
                    connection.close()
                    break
                elif command == "about":
                    print("DonutDB 2023 Velocity")
                    print("v23.8.20")
                    print("Gautham Nair")
                else:
                    cursor.execute(command)
                    connection.commit()
            break
        elif command == "enter database":
            database = input("Enter database name: ")
            while command != "exit" or command != "quit":
                command = input("DonutDB $ ")
                connection = sqlite3.connect(database)
                cursor = connection.cursor()
                if "select" in command:
                    cursor.execute(command)
                    connection.commit()
                    print(cursor.fetchall())
                elif command == "show databases":
                    os.system('ls')
                elif command == "exit":
                    connection.close()
                    break
                elif command == "about":
                    print("DonutDB 2023 Velocity")
                    print("v23.8.20")
                    print("Gautham Nair")
                else:
                    cursor.execute(command)
                    connection.commit()
            break
        else:
            print("Terminating DonutDB")
            break
