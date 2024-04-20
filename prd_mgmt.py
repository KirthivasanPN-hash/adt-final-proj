
import streamlit as st
import mysql.connector

st.sidebar.header("Product management page")

# Establish connection to MySQL database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="python19",
        database="optiflow"
    )

# Create product table if not exists
def create_product_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            index_number INT AUTO_INCREMENT PRIMARY KEY,
            SHIPPING_LOCATION VARCHAR(255),
            DEPARTMENT VARCHAR(255),
            category VARCHAR(255),
            Breadcrumbs VARCHAR(255),
            SKU VARCHAR(255),
            PRODUCT_URL VARCHAR(255),
            PRODUCT_NAME VARCHAR(255),
            BRAND VARCHAR(255),
            PRICE_RETAIL VARCHAR(50),
            PRICE_CURRENT VARCHAR(50),
            PRODUCT_SIZE INT
        )
    """)
    conn.commit()

# Function to insert a product into the database
def insert_product(conn, product_data):
    cursor = conn.cursor()
    query = """
        INSERT INTO items (SHIPPING_LOCATION, DEPARTMENT, category, Breadcrumbs, SKU, PRODUCT_URL, PRODUCT_NAME, BRAND, PRICE_RETAIL, PRICE_CURRENT, PRODUCT_SIZE)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, product_data)
    conn.commit()
    return cursor.lastrowid

# Function to update a product in the database
def update_product(conn, product_id, product_data):
    cursor = conn.cursor()
    query = """
        UPDATE items
        SET SHIPPING_LOCATION = %s, DEPARTMENT = %s, category = %s, Breadcrumbs = %s, SKU = %s, PRODUCT_URL = %s, PRODUCT_NAME = %s, BRAND = %s, PRICE_RETAIL = %s, PRICE_CURRENT = %s, PRODUCT_SIZE = %s
        WHERE index_number = %s
    """
    cursor.execute(query, (*product_data, product_id))
    conn.commit()

# Function to delete a product from the database
def delete_product(conn, product_id):
    cursor = conn.cursor()
    query = """
        DELETE FROM items WHERE index_number = %s
    """
    cursor.execute(query, (product_id,))
    conn.commit()

# Main function
def main():
    st.title("Product Management App")

    # Connect to database
    conn = connect_to_db()
    create_product_table(conn)

    # Sidebar options
    menu = ["Insert Product", "Update Product", "Delete Product"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Insert Product":
        st.subheader("Insert Product")
        # Collect product details
        SHIPPING_LOCATION = st.text_input("Shipping Location")
        DEPARTMENT = st.text_input("Department")
        category = st.text_input("Category")
        Breadcrumbs = st.text_input("Breadcrumbs")
        SKU = st.text_input("SKU")
        PRODUCT_URL = st.text_input("Product URL")
        PRODUCT_NAME = st.text_input("Product Name")
        BRAND = st.text_input("Brand")
        PRICE_RETAIL = st.text_input("Retail Price")
        PRICE_CURRENT = st.text_input("Current Price")
        PRODUCT_SIZE = st.number_input("Product Size", value=0)

        if st.button("Insert"):
            insert_product(conn, (
            SHIPPING_LOCATION, DEPARTMENT, category, Breadcrumbs, SKU, PRODUCT_URL, PRODUCT_NAME, BRAND, PRICE_RETAIL,
            PRICE_CURRENT, PRODUCT_SIZE))
            st.success("Product inserted successfully!")
    elif choice == "Update Product":
        st.subheader("Update Product")
        product_id = st.number_input("Enter Index Number")
        # Collect updated product details
        SHIPPING_LOCATION = st.text_input("Shipping Location")
        DEPARTMENT = st.text_input("Department")
        category = st.text_input("Category")
        Breadcrumbs = st.text_input("Breadcrumbs")
        SKU = st.text_input("SKU")
        PRODUCT_URL = st.text_input("Product URL")
        PRODUCT_NAME = st.text_input("Product Name")
        BRAND = st.text_input("Brand")
        PRICE_RETAIL = st.text_input("Retail Price")
        PRICE_CURRENT = st.text_input("Current Price")
        PRODUCT_SIZE = st.number_input("Product Size", value=0)

        if st.button("Update"):
            try:
                update_product(conn, product_id, (
                    SHIPPING_LOCATION, DEPARTMENT, category, Breadcrumbs, SKU, PRODUCT_URL, PRODUCT_NAME, BRAND,
                    PRICE_RETAIL,
                    PRICE_CURRENT, PRODUCT_SIZE))
                st.success("Product updated successfully!")
            except Exception as e:
                st.error(f"Error updating product: {e}")

    elif choice == "Delete Product":
        st.subheader("Delete Product")
        product_id = st.number_input("Enter Product ID")

        if st.button("Delete"):
            delete_product(conn, product_id)
            st.success("Product deleted successfully!")

    # Close database connection
    conn.close()

if __name__ == "__main__":
    main()
