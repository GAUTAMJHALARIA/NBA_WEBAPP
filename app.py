import pandas as pd
import matplotlib as plt
import streamlit as st
import numpy as np
import seaborn as sns

tab1,tab2 = st.tabs(["Player-wise", "Team-wise"])
col1,col2 = st.columns(2)

with tab1:
    with col1:
        with st.container():
            st.header("This is Tab 1")
            st.write("Content in Tab 1's container of col 1")

    with col2:
        with st.container():
            st.header("This is Tab 1")
            st.write("Content in Tab 1's container of col 2")
