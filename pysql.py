#!/bin/python3.8

#Python program for interacting with a MySQL database.

import sys, getopt, os.path, mysql.connector
from mysql.connector import errorcode

# Setting global variables.
###########################
# Program version.
version = "1.0"
# Hostname/IP Address of database server that we will connect to.
host = ""
# Username we will use when connecting to the server.
username = ""
# Password used along with the username.
password = ""
# Database name we want to connect to.
database = ""
# Table we want to modify/create.
table = ""
# Connection variable.
connection = ""
# Cursor variable.
cursor = ""
# Importing command line arguments into a list.
arguments = sys.argv[1:]
# Run mode of the program (dry run (0), production run (1)).
runmode = "1"
# Connect mode variable. Initially connect to a database (0), just connect to server (1).
connectmode = "1"
# SQL Query to run.
query = []
###########################

# Function for checking arguments that are passed to the program.
# This function will exit the program if invalid arguments are provided.
def ARGUMENT_CHECK(argument_list):
    # Setting variables
    # Global variable for queries whicha are provided as pure arguments on the command line.
    global query
    try:
        opts, args = getopt.getopt(argument_list, 'Dhu:s:q:d:')
    except getopt.GetoptError as error:
        print(error)
        sys.exit(2)
    query = args
    return opts

# This function parses arguments provided to it and sets variables to the
# values included with those arguments.
def ARGUMENT_PARSE(argument_list):
    # Setting variables.
    # Global username variable.
    global username
    # Global password variable.
    global password
    # Global host variable.
    global host
    # Global runmode variable.
    global runmode
    # Global query variable.
    global query
    # Global variable for database to connect to.
    global database
    if not argument_list:
        HELP()
        sys.exit(2)
    for o, a in argument_list:
        if o == "-D":
            runmode = "0"
        elif o == "-h":
            HELP()
        elif o == "-u":
            username = a
        elif o == "-p":
            password = a
        elif o == "-s":
            host = a
        elif o == "-d":
            database = a
        else:
            print("Unhandled option/argument.")
            sys.exit(2)

# This function will print a helpful 'help' page.
def HELP():
    print("Version:",version)
    print("")
    print("Description:")
    print("This program can interact with MySQL database servers. After specifying the command line arguments below simply state your MySQL")
    print("queries encased in quatation marks "". You can specify multiple queries and they will be ran in the order in which you give them.")
    print("")
    print("Options:")
    print("-D, Designates a dry run. The program will attempt to connect to your database server using the information provided but will make no changes.")
    print("-h, prints this page.")
    print("-u, designates the username used when connecting to the database server.")
    print("-p, designates the password that will be used with the provided username. For no password leave blank")
    print("-s, the host/server to connect to.")
    print("-d, this designates what database you want to initially connect to.")

# This function will check if a server is specified, if not it will exit. It also checks if a password is provided and if a dry run is needed.
def CHECKS(host, database, username, password, runmode, query):
    # Setting variables.
    # Global variable for setting the connect mode.
    global connectmode
    if host == "":
        print("No server specified. Exiting.")
        sys.exit(2)
    if username == "":
        print("No username specified. Exiting.")
        sys.exit(2)
    if password == "":
        print("No password provided. Using no password.")
    if database == "":
        print("No database specified. Only connecting to server.")
        connectmode = 1
    else:
        print("Connecting to server on database:",database)
        connectmode = 0
    if runmode == "0":
        print("Executing dry run.")
        DRYRUN()
    if query == []:
        print("No query specified. Exiting.")
        sys.exit(2)

# This function will execute a dry run. It will only attempt to connect to the server.
def DRYRUN():
    # Setting variables.
    # Global variable for username.
    global username
    # Global variable for password.
    global password
    # Global variable for host.
    global host
    # Global variable for database.
    global database
    SERVER_CONNECT(host, username, password, database)
    SERVER_DISCONNECT()
    sys.exit(1)

# Function for creating cursors.
def CURSOR_CREATE():
    # Setting variables.
    # Importing global connection variable.
    global connection
    # Importing global cursor variable.
    global cursor
    # Creating cursor and exporting to global variable.
    cursor = connection.cursor()

# Function for closing cursors.
def CURSOR_CLOSE():
    # Setting variables.
    # Importing global cursor variable.
    global cursor
    # Closing cursor.
    cursor.close

# Function that will both close the current open cursor and connection.
def CLOSE():
    CURSOR_CLOSE()
    SERVER_DISCONNECT()


# This function will connect to the target server using the provided username and password.
# If it fails to connect it will error out and close the program.
def SERVER_CONNECT(host, username, password, database):
    # Setting variables.
    # Variable for containing error information.
    error = ""
    # Global variable set for opening/interacting with the connection.
    global connection
    # Global variable for connection mode.
    global connectmode
    if connectmode == 1:
        # Attempting to connect to the server.
        print("Attempting to connect to MySQL server at:",host)
        try:
            connection = mysql.connector.connect(user=username, password=password, host=host)
        except mysql.connector.Error as error:
            print("Failed to connect to server. Error code:",error)
            exit
        finally:
            if (connection.is_connected()):
                print("Successfully connected to server.")
            else:
                print("Unknown error when connecting to server. Program exiting.")
                sys.exit(2)
    elif connectmode == 0:
        # Attempting to connect to the server.
        print("Attempting to connect to MySQL server at:",host,"On database:",database)
        try:
            connection = mysql.connector.connect(user=username, password=password, host=host, database=database)
        except mysql.connector.Error as error:
            print("Failed to connect to server. Error code:",error)
            exit
        finally:
            if (connection.is_connected()):
                print("Successfully connected to server.")
            else:
                print("Unknown error when connecting to server. Program exiting.")
                sys.exit(2)
    return connection

# This function will disconnect the current session if one is connected.
def SERVER_DISCONNECT():
    # Setting variables.
    # Global variable for interacting with the connection.
    global connection

    if (connection.is_connected()):
        print("Closing connection to server.")
        connection.close()
    else:
        print("Not connected to a server. Can't close connection.")

# Main function.
def main():
    # Setting variables.
    # Global variable for command line arguments.
    global arguments
    # Global variable for the query to be ran.
    global query
    # Global variables required for a connection.
    #############################################
    global host
    global database
    global username
    global password
    global runmode
    global query
    #############################################
    # Performing input validation on provided command line arguments.
    arguments = (ARGUMENT_CHECK(arguments))
    # Parsing said command line arguments for their provided values.
    ARGUMENT_PARSE(arguments)
    # Performing pre-flight checks.
    CHECKS(host, database, username, password, runmode, query)
    SERVER_CONNECT(host, username, password, database)
    CURSOR_CREATE()
    # Setting up counter for interating through query list.
    b = len(query)
    for i in range(b):
        try:
            cursor.execute(query[i])
            if cursor.rowcount == 0:
                continue
            else:
                results = cursor.fetchall()
                print(results)
        except mysql.connector.Error as error:
            print("Error when executing query:", error)


if __name__ =="__main__":
    main()
