import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Harish Pariyar", "Veni Tiwari", "Rishi Sharma",
         "Anadya Sahai", "Suvidha Srivastva", "Sachin Kansal"]
usernames = ["hpariyar", "vtiwari", "rsharma",
             "asahai", "ssrivastva", "skansal"]
passwords = ["xxx", "xxx", "xxx", "xxx", "xxx", "xxx"]


hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)
