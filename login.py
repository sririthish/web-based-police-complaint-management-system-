import pandas as pd  # pip install pandas openpyxl
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import time
import database as db
import update_database as ud
from streamlit_option_menu import option_menu

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Crime portal",
                   page_icon=":blossom:")


placeholder = st.empty()

users = db.fetch_all_users()

usernames = [user["key"] for user in users]
names = [user["name"] for user in users]
passwords = [user["password"] for user in users]

credentials = {"usernames": {}}

for un, name, pw in zip(usernames, names, passwords):
    user_dict = {"name": name, "password": pw}
    credentials["usernames"].update({un: user_dict})


selected3 = option_menu(None, ["Sign-in", "Sign-up"],
                        icons=['box-arrow-in-right',
                               'arrow-right-square-fill'],
                        menu_icon="cast", default_index=0, orientation="horizontal")

st.session_state["user_id"] = ""

authenticator = stauth.Authenticate(
    credentials, 'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)
if selected3 == "Sign-in":
    # name = st.text_input("Name", placeholder='Enter your name')
    # username = st.text_input("Username", placeholder='Enter username')
    # password = st.text_input("password", placeholder='Enter the password')

    name, authentication_status, username = authenticator.login(
        "Login", "main")

    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Please enter your username and password")

    if authentication_status:
        st.write('Welcome {0}!'.format(name))
        st.session_state["user_id"] = name
        # placeholder.empty()


if selected3 == "Sign-up":
    name = st.text_input("Name", placeholder='Enter your name')
    username = st.text_input("Username", placeholder='Enter username')
    password = st.text_input("password", placeholder='Enter the password')
    if st.button('submit'):
        ud.signup(name, username, password)
        st.session_state["user_id"] = name
        st.write('Welcome', name)

authenticator.logout("Logout", "sidebar")

# with st.co6y()

# with st.sidebar:
#     with st.echo():
#         st.write("This code will be printed to the sidebar.")

# with st.spinner("Loading..."):
#     time.sleep(5)
# st.success("Done!")

# ---- HIDE STREAMLIT STYLE ----
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=False)
