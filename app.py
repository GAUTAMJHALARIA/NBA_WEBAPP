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