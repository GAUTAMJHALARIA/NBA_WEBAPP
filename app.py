import pandas as pd
import matplotlib as plt
import streamlit as st
import numpy as np
import seaborn as sns

from NBA_DATA import get_players_name_list
from helper import get_player_img

st.sidebar.title("NBA Analysis")
user_menu = st.sidebar.radio(
    'Select An Option',
    ('Player-wise','Team-wise')
)

if user_menu == 'Player-wise':
    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            st.header("Player About")
            selected_player = st.selectbox("Select Player", get_players_name_list())
            image = get_player_img(selected_player)
            c1,c2 = st.columns(2)
            with c1:
                st.image(
                    image,
                    width =200,
                    channels="RGB"
                )
            with c2:
                pass



    with col2:
        with st.container():
            tab1, tab2 = st.tabs(["Short Chart", "HeatMap"])
            st.header("This is Container")
            st.write("Content in  container of col 2")





