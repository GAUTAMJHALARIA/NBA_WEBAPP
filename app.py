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
    selected_player = st.sidebar.selectbox("Select Player", get_players_name_list())
    with col1:
        with st.container():
            st.header("Player About")
            image = get_player_img(selected_player)
            c1,c2 = st.columns(2)
            with c1:
                st.image(
                    image,
                    width =200,
                    channels="RGB"
                )
            with c2:
                st.write("going to implement common details for {}".format(selected_player))



    with col2:
        with st.container():
            tab1, tab2 = st.tabs(["Short Chart", "HeatMap"])

            with tab1:
                st.header("This is Shortchart")
                st.write("Short chart for {}".format(selected_player))

            with tab2:
                st.header("This is for heatmap")
                st.write("Heat map for {}".format(selected_player))





