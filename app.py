
import streamlit as st
import Hello
import prd_mgmt
import reports
import transaction
import pyrebase
import os

st.set_page_config(
    page_title="Auth page",
    page_icon="👋",
)

st.header("Optiflow Inventory Management ")



# Environment variables are recoed for sensitive information
firebaseConfig = {
  'apiKey': "AIzaSyByGf4CiLaLcpY92DuId9N7rvPH4FOhNo4",
  'authDomain': "im-proj-73a48.firebaseapp.com",
  'projectId': "im-proj-73a48",
  'databaseURL': "https://im-proj-73a48-default-rtdb.firebaseio.com/",
  'storageBucket': "im-proj-73a48.appspot.com",
  'messagingSenderId': "840100920791",
  'appId': "1:840100920791:web:4947461a1db95952009f92",
  'measurementId': "G-GETPQ4DLMX"
};
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

st.sidebar.title("Inventory Management App")

# Log out functionality
if st.session_state['authenticated']:
    if st.sidebar.button('Logout'):
        st.session_state['authenticated'] = False
        st.experimental_rerun()

# If user is not authenticated, show login and signup options
if not st.session_state['authenticated']:
    choice = st.sidebar.selectbox('Login/Signup', ['Login', 'SignUp'])
    email = st.sidebar.text_input('Please enter your email address')
    password = st.sidebar.text_input('Please enter your password', type='password')

    if choice == "SignUp":
        handle = st.sidebar.text_input("Please enter your username", value='Default')
        submit = st.sidebar.button("Create an account")
        if submit:
            user = auth.create_user_with_email_and_password(email, password)
            st.success("Your account is created successfully")
            user = auth.sign_in_with_email_and_password(email, password)
            db.child(user['localId']).child("Handle").set(handle)
            db.child(user['localId']).child("ID").set(user['localId'])
            st.session_state['authenticated'] = True
            st.title('Welcome, ' + handle)
            st.experimental_rerun()

    elif choice == "Login":
        submit = st.sidebar.button("Login")
        if submit:
            user = auth.sign_in_with_email_and_password(email, password)
            if user:
                st.success("Logged in successfully")
                st.session_state['authenticated'] = True
                st.experimental_rerun()
            else:
                st.error("Login failed, please check your credentials.")

# Navigation and page display for authenticated users
if st.session_state['authenticated']:
    import Hello, prd_mgmt, reports, transaction
    PAGES = {
        "Hello Page": Hello,
        "Product Management": prd_mgmt,
        "Reports": reports,
        "Transaction": transaction,
    }
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.main()
else:
    st.warning("Please login to access the application features.")