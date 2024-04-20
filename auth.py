import streamlit_authenticator as stauth
import pickle
from pathlib import Path
from streamlit_authenticator.utilities.hasher import Hasher

name = ["Admin_pnk"]
usernames = ["kirthivasan"]
passwords = ["XXX"]

hashed_passwords = Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)

    