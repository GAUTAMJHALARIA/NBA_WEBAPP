import streamlit as st
import pandas as pd

st.sidebar.title("NBA Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Player Statistics', 'Team Statistics')
)

