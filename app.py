import streamlit as st
import pandas as pd

st.sidebar.title("NBA Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Trends', 'Player Statistics', 'Team Statistics', 'Player Comparison', 'Team Comparison')
)
