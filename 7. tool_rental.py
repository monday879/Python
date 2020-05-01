#!/usr/bin/python
# Name: Qichen Jia
# Course: CST8245 Advanced Scripting
# Student Number: 040914732
# Date: April 11, 2020
# Script Name: /home/u8245/pythonApps.d/tool_rental.py
# Purpose: This program can connect to postgersql database. Users can display, insert or delete records.
# Version: 1.0

# Import Modules
import psycopg2
import sys

# Variables
dbname = 'tool_store_143'
username = 'dbadmin'

################################
# Name: connect_db
# Purpose: Test if database can be connected
# Parameters: dbname, username
# Return value: none
################################
def connect_db(dbname,username):
    try:
        print "Cnnecting to the '"+ dbname +"' database..."
        # Establish connection
        connection = psycopg2.connect(database = dbname, user = username)
    except:
        # Print an Error message if cannot connect to the db
        print 'Error: connection can not established.'
        # Exit handled
        sys.exit(1)
    else:
        print "Database connected!"
        # Close the connection
        connection.close()

################################
# Name: display_main_menu
# Purpose: Display main menu
# Parameters: none
# Return value: none
#################################

def display_main_menu():
    print '''
Please select from one of the menu options:

1. Queries (sub-menu)
2. Insert tool rental
3. Delete tool rental
x. Exit

'''

################################
# Name: display_query_menu
# Purpose: Display query menu
# Parameters: none
# Return value: none
#################################
#
def display_query_menu():
    print'''
Please select from one of the query options:

1.  Display all customers
2.  Display all tools (optionally by job)
3.  Display all rentals (optionally by customer)
4.  Display all overdue rentals

'''

################################
# Name: display_query
# Purpose: Display query
# Parameters: none
# Return value: none
##################################
#
def display_query(sqlQuery):
    # Connect to the db
    connection = psycopg2.connect(database = dbname, user = username)
    # Derive cursor from the connection
    cursor = connection.cursor()
    # Execute the sql query
    cursor.execute(sqlQuery)
    # Fetchone will get next record untill none
    tuple = cursor.fetchone()
    while tuple is not None:
        print tuple
        print ""
        tuple = cursor.fetchone()
    # Close cursor
    cursor.close()
    # Close connection
    connection.close()

################################
# Name: get_menu_selection
# Purpose: Get query menu selection
# Parameters: none
# Return value: selection
##################################
#
def get_menu_selection():
    # Get user input for the query menu selection
    selection = raw_input("Enter your selection: ")
    # Test if the input is valid
    if selection != '1' and selection != '2' and selection != '3' and selection != '4':
        # If user does not type in a valid option, display an Error message
        print "Error: Please enter 1-4."
    else:
        # Return the user selection
        return selection

################################
# Name: get_query_selection
# Purpose: Get menu selection
# Parameters: none
# Return value: selection
##################################
#
def get_query_selection():
    # Get user input for the main menu selection
    selection = raw_input("Enter your selection: ")
    # Test if the input is valid
    if selection != '1' and selection != '2' and selection != '3' and selection != 'x':
        print "Error: Please enter 1-3 or x."
    else:
        return selection
    
################################
# Name: get_customer_name
# Purpose: Get customer name
# Parameters: none
# Return value: fname,lname
##################################
#
def get_customer_name():
    # Get user input for the customer first name
    fname = str(raw_input("Enter the customer first name: "))
    # Get customer last name
    lname = str(raw_input("Enter the customer last name: "))
    return fname,",",lname
 

################################
# Name: get_customer_id
# Purpose: Get customer id
# Parameters: fname,lname
# Return value: tuple[0]
##################################
#
def get_customer_id(fname,lname):
    # Connect to database
    connection = psycopg2.connect(database = dbname, user = username)
    # Define the sql query that going to execute, get customer_id by first name and last name
    sqlQuery = "SELECT customer_id FROM customers WHERE fname = '"+fname+"' and lname = '"+lname+"'"
    # Drive cursor from connection
    cursor = connection.cursor()
    # Execute the query
    cursor.execute(sqlQuery)
    # Get all the fetched records
    tuple = cursor.fetchone()
    # Test if the customer exists
    if tuple is None:
        print "Error: The customer can not be found."
    else:
        return tuple[0]
    cursor.close()
    connection.close()

################################
# Name: get_tool_name
# Purpose: Get tool name
# Parameters: none
# Return value: tool_name
##################################
#
def get_tool_name():
    tool_name = str(raw_input("Enter the tool name: "))
    return tool_name

################################
# Name: get_tool_id
# Purpose: Get tool id
# Parameters: tool_name
# Return value: tuple[0]
##################################
#
def get_tool_id(tool_name):
    # Define the sql query, get tool_id by tool name
    sqlQuery = "SELECT tool_id FROM tools WHERE tool_name = '"+tool_name+"'"
    connection = psycopg2.connect(database = dbname, user = username)
    cursor = connection.cursor()
    cursor.execute(sqlQuery)
    tuple = cursor.fetchone()
    # Test if the tool is available
    if tuple is None:
        print "Error: The tool can not be found."
    else:
        return tuple[0]
    cursor.close()
    connection.close()

################################
# Name: get_rental_days
# Purpose: Get tool rental days
# Parameters: tool_name
# Return value: tuple[0]
##################################
# 
def get_rental_days(tool_name):
    # Defind the sql query, get rental_days by tool name
    sqlQuery = "SELECT rental_days FROM tools WHERE tool_name = '"+tool_name+"'"
    connection = psycopg2.connect(database = dbname, user = username)
    cursor = connection.cursor()
    cursor.execute(sqlQuery)
    tuple = cursor.fetchone()
    return tuple[0]
    cursor.close()
    connection.close()

################################
# Name: query_customers
# Purpose: Query all customers
# Parameters: none
# Return value: none
##################################
#
def query_customers():
    # Define the sql query, display all customer information
    sqlQuery = "SELECT * FROM customers;"
    print "Customer information: "
    display_query(sqlQuery)

################################
# Name: query_tools
# Purpose: Query all tools
# Parameters: none
# Return value: none
##################################
#
def query_tools():
    # Dispaly available tools information order by job name 
    sqlQuery = "SELECT tools.tool_id,tool_name,job_name,rental_days FROM tools LEFT JOIN tool_jobs ON tools.tool_id = tool_jobs.tool_id LEFT JOIN jobs ON jobs.job_id = tool_jobs.job_id ORDER BY job_name;"
    print "Tools available: "
    display_query(sqlQuery)

################################
# Name: query_tools_by_job
# Purpose: Query all tools sorted by job
# Parameters: job_name
# Return value: none
##################################
#
def query_tools_by_job(job_name):
    # Get tools name by job name
    sqlQuery = "SELECT tool_name FROM tools JOIN tool_jobs ON tools.tool_id = tool_jobs.tool_id JOIN jobs ON jobs.job_id = tool_jobs.job_id WHERE job_name = '" + job_name + "'"
    print "Tool information selected: "
    display_query(sqlQuery)

################################
# Name: query_rentals
# Purpose: Query all rentals
# Parameters: none 
# Return value: none
##################################
#
def query_rentals():
    # Get all rental records
    sqlQuery = "SELECT fname,lname,tool_name,rental_date,return_date FROM customers JOIN rentals ON rentals.customer_id = customers.customer_id JOIN tools ON rentals.tool_id = tools.tool_id;"
    print "Rental records: "
    display_query(sqlQuery)

###################################
# Name: query_rentals_by_customer
# Purpose: Query all rentals sorted by customer
# Parameters: customer_id
# Return value: none
###################################
# 
def query_rentals_by_customer(customer_id):
    # Get a customer's rental records
    sqlQuery = "SELECT fname,lname,tool_name,rental_date,return_date FROM customers JOIN rentals ON rentals.customer_id = customers.customer_id JOIN tools ON rentals.tool_id = tools.tool_id WHERE rentals.customer_id = " + customer_id
    print "Customer rental record:"
    display_query(sqlQuery)

###################################
# Name: query_overdue_rentals
# Purpose: Query overdue rentals
# Parameters: none
# Return value: none
###################################
#
def query_overdue_rentals():
    # Get overdue rentals records
    sqlQuery = "SELECT phone,tool_name,rental_date,return_date,fname,lname FROM customers JOIN rentals ON rentals.customer_id = customers.customer_id JOIN tools ON rentals.tool_id = tools.tool_id WHERE return_date < current_date;"
    print "Overdue rental records: "
    print "(phone number, tool name, rental_date, return_date, first name, last name)"
    display_query(sqlQuery)

###################################
# Name: is_tool_rented_by_customer
# Purpose: If tool already rented by a customer
# Parameters: customer_id,tool_id
# Return value: Trun or False
###################################
#
def is_tool_rented_by_customer(customer_id,tool_id):
    # Get tools' records rented by a customer
    sqlQuery = "SELECT tool_name FROM customers JOIN rentals ON rentals.customer_id = customers.customer_id JOIN tools ON rentals.tool_id = tools.tool_id WHERE rentals.customer_id = " + customer_id + " and rentals.tool_id = " + tool_id
    connection = psycopg2.connect(database = dbname, user = username)
    cursor = connection.cursor()
    cursor.execute(sqlQuery)
    tuple = cursor.fetchone()
    # If returns with records, means the tool has rented to this customer
    if tuple is not None:
        # If rented to this costomer, return True
        return True
    else:
        # If not rented to this costomer, return False
        return False
    cursor.close()
    connection.close()

###################################
# Name: insert_rental
# Purpose: Insert rental record
# Parameters: none
# Return value: none
###################################
#
def insert_rental():
    # Get user input for customer first name
    fname = str(raw_input("Enter the customer first name: "))
    # Get user input for customer last name
    lname = str(raw_input("Enter the customer last name: "))
    # Call the get_customer_id function to get customer_id by the customer's name
    customer_id = str(get_customer_id(fname,lname))
    print ""
    # Manage exceptions when customer_id = none
    try:
        # Display this customer current rentals
        query_rentals_by_customer(customer_id)
        print ""
        # Display available tools
        query_tools()
        print ""
        # Get tool id by the tool name
        tool_id = str(get_tool_id(get_tool_name()))
        # Test if the tool has been rented to this customer
        test = is_tool_rented_by_customer(customer_id,tool_id)
        # If it has been rented to this customer, display an Error message
        if test is True:
            print "Error: The tool has rented to this customer."
        # If not, insert the record
        else:
            sqlQuery = "INSERT INTO rentals(tool_id, customer_id, rental_date, return_date) VALUES (" + tool_id + " , " + customer_id + ", current_date, (current_date + (SELECT rental_days FROM tools WHERE tool_id = " + tool_id + ")));"
            connection = psycopg2.connect(database = dbname, user = username)
            cursor = connection.cursor()
            cursor.execute(sqlQuery)
            connection.commit()
            print ""
            # Print the updated customer rentals
            query_rentals_by_customer(customer_id)
            print ""
            cursor.close()
            connection.close()
    except:
        # Mute the exception
        print ""

####################################
# Name: delete_rental 
# Purpose: Delete rental record
# Parameters: none
# Return value: none
####################################
# 
def delete_rental():
    # Get user input for customer first name
    fname = str(raw_input("Enter the customer first name: "))
    # Get user input for customer last name
    lname = str(raw_input("Enter the customer last name: "))
    # Get customer id by name
    try:
        customer_id = str(get_customer_id(fname,lname))
        print ""
        # Dispaly the customer's current rentals
        query_rentals_by_customer(customer_id)
        print ""
        # Get tool id by tool's name
        tool_id = str(get_tool_id(get_tool_name()))
        # Test if there is no such rental record
        test = is_tool_rented_by_customer(customer_id,tool_id)
        if test is False:
            # If no such record, then display an Error message
            print "Error: The tool did not rented to this customer."
        else:
            # If such record exists, then delete it
            sqlQuery = "DELETE FROM rentals WHERE tool_id = " + tool_id + " and customer_id = " + customer_id
            connection = psycopg2.connect(database = dbname, user = username)
            cursor = connection.cursor()
            cursor.execute(sqlQuery)
            connection.commit()
            print ""
            # Print the updated customer rental records
            print query_rentals_by_customer(customer_id)
            print ""
            cursor.close()
            connection.close()
    except:
        # Mute the exception
        print ""

####################################
# Name: main
# Purpose: The main function
# Parameters: none
# Return value: none
####################################
# The main function
def main():
    # Test databse connection
    connect_db(dbname,username)
    # Predefine a selection value
    selection = '1'
    # When the user does not select x, then keep running the program
    while selection != 'x':
        # Display main menu
        display_main_menu()
        # Prompt user for selection
        selection = get_query_selection()
        # If x, then exit the program
        if selection == 'x':
            print "Thank you for using."
            # Exit gracefully
            sys.exit(0)
        # If select 3, call the delete function
        elif selection == '3':
            delete_rental()
            # Continue the while loop from the beginning
            continue
        # If select 2, call the insert function
        elif selection == '2':
            insert_rental()
            continue
        # If select 1, call the query menu and functions
        elif selection == '1':
            # Display query menu
            display_query_menu()
            # Prompt for the query menu selection
            select = get_menu_selection()
            # If select 1, then display customers info
            if select == '1':
                query_customers()
                # Continue from the beginning of the while loop
                continue
            # If select 2, then dispaly the tools info
            elif select == '2':
                query_tools()
                continue
            # If select 3, then display the rental records
            elif select == '3':
                query_rentals()
                continue
            # If select 4, display the overdue rental records
            elif select == '4':
                query_overdue_rentals()
                continue
    
####################################
####################################
# Call the main function
if __name__ == '__main__':
    try:
        main()
    # Handle the keyboard Interrupt
    except KeyboardInterrupt:
        print '''
Exit by user keyboard interrupt.
'''
        # Exit gracefully
        sys.exit(0)
