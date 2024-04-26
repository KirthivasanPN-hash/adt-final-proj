import streamlit as st
import mysql.connector
from mysql.connector import Error
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# Connection to MySQL Database
def create_server_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="y5s2h87f6ur56vae.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
            port=3306,
            user="fpb88ek60sl39cgj",
            password="h0up9wllusrv5ss6",
            database="f0uk4v9q5xl7dodx"
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
def fetch_transaction(connection):
    cursor = connection.cursor(dictionary=True)  # Set dictionary cursor to fetch column names
    query = "SELECT * FROM Transaction"
    cursor.execute(query)
    items = cursor.fetchall()
    return items

def insert_invoice(conn, invoice_data):
    cursor = conn.cursor()
    query = """
        INSERT INTO invoice (TransactionID, ItemID, TransactionType, Quantity, TransactionDate, Notes)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, invoice_data)
    conn.commit()
    return cursor.lastrowid

def main():
    conn = create_server_connection()
     # Sidebar options
    menu = ["View Transactions", "Update invoice", "Transaction analysis report"]
    choice = st.sidebar.selectbox("Menu", menu)
    

    transactions = fetch_transaction(conn)
    

    if choice == 'View Transactions':
    # Display items in a table
        if transactions:
            st.write("## Transactions")
            st.table(transactions)
        else:
            st.write("No data found.")


    if choice == "Update invoice":
        st.subheader("Invoice")
        # Collect invoice details
        TransactionID = st.number_input("Transaction ID", value=0)
        ItemID = st.number_input("Item ID", value=0)
        TransactionType = st.text_input("Transaction Type")
        Quantity = st.number_input("Quantity", value=0)
        TransactionDate = st.date_input("Transaction Date")
        Notes = st.text_input("Notes")

        if st.button("Insert"):
            insert_invoice(conn, (
                TransactionID, ItemID, TransactionType, Quantity, TransactionDate, Notes))
            st.success("Invoice inserted successfully!")

    if choice == "Transaction analysis report":
        st.subheader("Transaction Analysis")
        query = """
            SELECT TransactionID, ItemID, TransactionType, Quantity, TransactionDate, Notes
            FROM Transaction
            """

        df = pd.read_sql(query, conn)
        transaction_counts = df.groupby('ItemID').size().reset_index(name='counts')
        
       

        fig, ax = plt.subplots()
        ax.bar(transaction_counts['ItemID'], transaction_counts['counts'])
        ax.set_xlabel('Item ID')
        ax.set_ylabel('Number of Transactions')
        ax.set_title('Transaction Count by Item ID')

        st.pyplot(fig)


        st.write("")
        st.write("")


        query1 = """
            SELECT ItemID, Quantity
            FROM Transaction
            """
        
        df1 = pd.read_sql(query1, conn)
        quantity_sum = df1.groupby('ItemID')['Quantity'].sum().reset_index()
        fig, ax = plt.subplots()
        ax.bar(quantity_sum['ItemID'], quantity_sum['Quantity'])
        ax.set_xlabel('Item ID')
        ax.set_ylabel('Sum of Quantities Sold')
        ax.set_title('Quantity of Items Sold by Item ID')

        st.pyplot(fig)


        st.write("")
        st.write("")



        query4 = """
            SELECT TransactionType
            FROM Transaction
            """
        df4 = pd.read_sql(query4, conn)
        transaction_counts = df4['TransactionType'].value_counts().reset_index()
        transaction_counts.columns = ['TransactionType', 'Count']
        fig, ax = plt.subplots()
        ax.bar(transaction_counts['TransactionType'], transaction_counts['Count'], color='teal')
        ax.set_xlabel('Transaction Type')
        ax.set_ylabel('Count of Transactions')
        ax.set_title('Transactions by Transaction Type')
        ax.set_xticklabels(transaction_counts['TransactionType'], rotation=45)

        st.pyplot(fig)


        st.write("")
        st.write("")



        # query3 = """
        #     SELECT TransactionType, Quantity
        #     FROM transaction
        #     """
        
        # avg_quantity = df.groupby('TransactionType')['Quantity'].mean().reset_index()
        # df3 = pd.read_sql(query3, conn)
        # # Plotting
        # fig, ax = plt.subplots()
        # ax.bar(avg_quantity['TransactionType'], avg_quantity['Quantity'], color='skyblue')
        # ax.set_xlabel('Transaction Type')
        # ax.set_ylabel('Average Quantity')
        # ax.set_title('Average Quantity of Transactions by Type')
        # ax.set_xticklabels(avg_quantity['TransactionType'], rotation=45)

        # st.pyplot(fig)


        # st.write("")
        # st.write("")


        # query4 = """
        #     SELECT TransactionType
        #     FROM your_table_name
        #     """
        # df4 = pd.read_sql(query4, conn)

        # fig, ax = plt.subplots()
        # ax.bar(transaction_counts['TransactionType'], transaction_counts['Count'], color='teal')
        # ax.set_xlabel('Transaction Type')
        # ax.set_ylabel('Count of Transactions')
        # ax.set_title('Transactions by Transaction Type')
        # ax.set_xticklabels(transaction_counts['TransactionType'], rotation=45)

        # st.pyplot(fig)