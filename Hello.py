import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd
import mysql.connector
from mysql.connector import Error

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

# Assuming you have already created a connection with your database
# connection = create_server_connection('your_host', 'your_username', 'your_password', 'your_db_name')

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
def fetch_items_count(connection):
    # Your SQL query to count items
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM items"
    cursor.execute(query)
    # Fetches the first row from the results (which contains the count)
    items_count = cursor.fetchone()[0]
    return items_count


def card_ui1(title, content):
    card_html = f"""
    <div style="background-color: #f5392c; padding: 10px; border-radius: 10px; box-shadow: 0 2px 2px 
    rgba(1, 0, 0, 0.2); max-width: 200px; height: 150px; display: flex; flex-direction: column; justify-content: 
    center; margin: auto; margin-bottom: 20px; margin-top: 10px">
        <h3 style="color: #332; text-align: center; margin-bottom: 0; margin-top: 10px;">{title}</h3>
        <h2 style="color: #faeceb; text-align: center; margin-top: auto;">{content}</h2>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def card_ui2(title, content):
    card_html = f"""
    <div style="background-color: #dec5c3; padding: 10px; border-radius: 10px; box-shadow: 0 2px 2px 
    rgba(1, 0, 0, 0.2); max-width: 200px; height: 150px; display: flex; flex-direction: column; justify-content: center; margin: auto margin-botom: 100px">
        <h3 style="color: #332; text-align: center; margin-bottom: 0; margin-top: 0;">{title}</h3>
        <h2 style="color: #ff4b4b; text-align: center; margin-top: 5px;">{content}</h2>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)



def fetch_trans_count(connection):
    # Your SQL query to count items
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM Transaction"
    cursor.execute(query)
    # Fetches the first row from the results (which contains the count)
    items_count = cursor.fetchone()[0]
    return items_count    

def fetch_cusomters_count(connection):
    # Your SQL query to count items
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM users where Role = 'Customer'"
    cursor.execute(query)
    # Fetches the first row from the results (which contains the count)
    items_count = cursor.fetchone()[0]
    return items_count 
   
def fetch_supplier_count(connection):
    # Your SQL query to count items
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM Suppliers "
    cursor.execute(query)
    # Fetches the first row from the results (which contains the count)
    items_count = cursor.fetchone()[0]
    return items_count    

def fetch_sales_count(connection):
    # Your SQL query to count items
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM Orders"
    cursor.execute(query)
    # Fetches the first row from the results (which contains the count)
    items_count = cursor.fetchone()[0]
    return items_count    

def fetch_revenue_count(connection):
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM Orders"
    cursor.execute(query)
    # Fetches the first row from the results (which contains the count)
    items_count = cursor.fetchone()[0]
    return items_count


# Define the layout
st.title('Streamlit Homepage')


def main():
    conn = create_server_connection()
    month_to_num = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }

    
    # Search bar
    search_term = st.text_input('Search an item')

    # Use a single column layout to ensure that the columns below will be full width
    st.write('## Key Metrics')

    # Top row with 3 cards
    col1, col2, col3 = st.columns(3)
    with col1:
        items_count = fetch_items_count(conn)
        card_ui1('Available Items', items_count)
    with col2:
        trans_count = fetch_trans_count(conn)
        card_ui1('Total Transaction', trans_count)
    with col3:
        customers_count = fetch_cusomters_count(conn) 
        card_ui1('Total Customers', customers_count)

    # Bottom row with 2 cards
    col4, col5, col6 = st.columns([1,1,1])
    with col4:
        suppliers_count = fetch_supplier_count(conn)
        card_ui2('Total Suppliers', suppliers_count)
    with col5:
        sales_count = fetch_sales_count(conn)
        card_ui2('Total Sales', sales_count)
    
    with col6:
        revenue_count = fetch_revenue_count(conn)
        card_ui2('Total Revenue', revenue_count)

    st.write("")
    st.write("")   
    st.write("")  


    # Sample data - you would replace this with your actual data
    chart_data = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Sales": np.random.randint(100, 500, size=6),
    "Revenue": np.random.randint(1000, 5000, size=6)
})

    # Add a numerical month column for sorting
    chart_data['MonthNum'] = chart_data['Month'].map(month_to_num)

    # Sort the DataFrame by the numerical month column
    chart_data.sort_values(by='MonthNum', inplace=True)

    # Remove the numerical month column if not needed for plotting
    chart_data.drop('MonthNum', axis=1, inplace=True)


    # Melt the data so that Sales and Revenue are in the same column, 
    # which allows us to color by the variable type (Sales/Revenue) in the bar chart.
    melted_data = chart_data.melt(id_vars='Month', var_name='Type', value_name='Amount')

    # Create a bar chart using Streamlit's built-in functionality
    st.bar_chart(data=melted_data, x="Month", y="Amount", color="Type")
        
    conn.close()

if __name__ == "__main__":
    main()