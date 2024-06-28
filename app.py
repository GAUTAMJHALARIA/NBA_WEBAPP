import streamlit as st
import pandas as pd
from Preprocessing import Preprocessor

st.sidebar.title("NBA Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Trends', 'Player Statistics', 'Team Statistics', 'Player Comparison', 'Team Comparison')
)

# reading the dataset
df = pd.read_csv("NBA Player Stats(1950 - 2022).csv")
# Cleaning the Data
df = Preprocessor(df)
per_mode = ["Totals","Per Game","Per 36 Mins","Per 48 Mins"]
if user_menu == 'Trends':
    st.sidebar.header("Trends")
    per_mode = st.sidebar.selectbox("Select Mode",per_mode)

    if per_mode == "Totals" :
        st.title("Totals Stats")