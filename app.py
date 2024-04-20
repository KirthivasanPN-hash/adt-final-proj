import streamlit as st
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import Hello
import prd_mgmt
import reports
import transaction

# Set page configuration
st.set_page_config(
    page_title="Login page",
    page_icon="👋",
)

# --- USER AUTHENTICATION ---
usernames = ["kirthivasan"]
names = ["Admin_pnk"]  # This list should correspond to usernames

# Load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

# Update credentials structure to include names
credentials = {
    'usernames': {
        usernames[i]: {
            'name': names[i],           # Include the name here
            'password': hashed_passwords[i],
            'logged_in': False
        } for i in range(len(usernames))
    }
}

# Initialize the authenticator with the correct parameters
authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name='hello_page',  # Set the cookie name for session management
    cookie_key='wswsws',  # Set a secret key for cookie encryption/signing
    cookie_expiry_days=2  # Optional: cookie expiration duration
)

name, authentication_status, username = authenticator.login(fields=['username', 'password'])

if authentication_status is False:
    st.error("Username/password is incorrect")

if authentication_status is None:
    st.warning("Please enter your username and password")

if authentication_status:
    PAGES = {
        "Hello Page": Hello,
        "Product Management": prd_mgmt,
        "Reports": reports,
        "Transaction": transaction
    }

    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]
    page.main()
