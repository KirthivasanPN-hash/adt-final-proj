import streamlit as st
import mysql.connector
from mysql.connector import Error

# Connection to MySQL Database
def create_server_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="python19",
            database="optiflow"
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

# Function to query your database
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

# Placeholder function to fetch items (modify with actual query)
def fetch_items(connection):
    cursor = connection.cursor(dictionary=True)  # Set dictionary cursor to fetch column names
    query = "SELECT * FROM items"
    cursor.execute(query)
    items = cursor.fetchall()
    return items

def fetch_suppliers(connection):
    cursor = connection.cursor(dictionary=True)  # Set dictionary cursor to fetch column names
    query = "SELECT * FROM suppliers"
    cursor.execute(query)
    items = cursor.fetchall()
    return items


def fetch_orders(connection):
    cursor = connection.cursor(dictionary=True)  # Set dictionary cursor to fetch column names
    query = "SELECT * FROM orders"
    cursor.execute(query)
    items = cursor.fetchall()
    return items

def fetch_revenue(connection):
    cursor = connection.cursor(dictionary=True)  # Set dictionary cursor to fetch column names
    query = "SELECT * FROM revenue"
    cursor.execute(query)
    items = cursor.fetchall()
    return items

def main():
    st.title("Reports")
   
    # Establish connection with the database
    conn = create_server_connection()

     # Sidebar options
    menu = ["Inventory report", "Supplier report", "Orders report",]
    choice = st.sidebar.selectbox("Menu", menu)
    # Fetch items from the database
    items = fetch_items(conn)
    suppliers = fetch_suppliers(conn)
    orders = fetch_orders(conn)
    # revenue = fetch_revenue(conn)

    if choice == 'Inventory report':
    # Display items in a table
        if items:
            st.write("## Items")
            st.table(items)
        else:
            st.write("No items found.")

    if choice == 'Supplier report':
    # Display items in a table
        if items:
            st.write("## Suppliers")
            st.table(suppliers)
        else:
            st.write("No suppliers found.")
    
    if choice == 'Orders report':
    # Display items in a table
        if items:
            st.write("## Orders")
            st.table(orders)
        else:
            st.write("No orders found.")
        
    # if choice == 'Revenue report':
    # # Display items in a table
    #     if items:
    #         st.write("## Revenue")
    #         st.table(revenue)
    #     else:
    #         st.write("No data found.")
        
    
    


    

    # Close database connection
    conn.close()

if __name__ == "__main__":
    main()
