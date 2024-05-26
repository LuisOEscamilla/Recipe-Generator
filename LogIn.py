"""app.py"""
import streamlit as st
import bcrypt
import hmac
from google.cloud import bigquery
import main

client = bigquery.Client('concise-option-413819')
st.session_state.status = st.session_state.get("status", "unverified")
st.title("Login Page")


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    tmp = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return tmp.decode('utf-8')


def check_password():
    QUERY = ("SELECT * FROM `concise-option-413819.food_data.user_data` WHERE username = '" +
             st.session_state.username + "'")
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "username", "STRING", st.session_state.username),
        ]
    )
    query_job = client.query(QUERY, job_config=job_config)
    rows = query_job.result()
    if rows.total_rows > 0:
        for row in rows:
            if bcrypt.checkpw(st.session_state.password.encode('utf-8'), row.hashed_password.encode('utf-8')):
                st.session_state.status = "verified"
                main.user_name = st.session_state.username
                
    if st.session_state.status != "verified":
        st.session_state.status = "incorrect"


def login_prompt():
    st.text_input("Enter username:", key="username")
    st.text_input("Enter password:", key="password")
    st.button("Create user", on_click=create_user)
    st.button("Log in", on_click=check_password)
    if st.session_state.status == "incorrect":
        st.warning("Incorrect username and password. Please try again")
    if st.session_state.status == "user_already_exists":
        st.warning("Username already exists")


def logout():
    st.session_state.status = "unverified"
    main.user_name = "New User" 


def create_user():
    QUERY = ("SELECT hashed_password FROM `concise-option-413819.food_data.user_data` WHERE username = '" +
             st.session_state.username + "'")
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "username", "STRING", st.session_state.username),
        ]
    )
    query_job = client.query(QUERY, job_config=job_config)
    rows = query_job.result()
    if rows.total_rows == 0:
        myquery = "INSERT INTO `concise-option-413819.food_data.user_data` (username, hashed_password) VALUES (\"%s\", \"%s\")" % (
            st.session_state.username, get_hashed_password(st.session_state.password))
        QUERY = (myquery)
        query_job = client.query(QUERY)  # API request
        rows = query_job.result()  # Waits for query to finish
        st.session_state.status = "unverified"
        st.write("Sign up successful. Please log in.")
    else:
        st.session_state.status = "user_already_exists"


def welcome():
    st.success("Login successful.")
    st.button("Log out", on_click=logout)


if st.session_state.status != "verified":
    login_prompt()
    st.stop()
welcome()
