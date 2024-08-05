import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import seaborn as sns

from NBA_DATA import *
from helper import get_player_img, draw_court

st.sidebar.title("NBA Analysis")
user_menu = st.sidebar.radio(
    'Select An Option',
    ('Player-wise', 'Team-wise')
)

if user_menu == 'Player-wise':
    col1, col2 = st.columns(2)
    selected_player = st.sidebar.selectbox("Select Player", get_players_name_list())
    with col1:
        with st.container():
            st.header("Player About")
            image = get_player_img(selected_player)
            c1, c2 = st.columns(2)
            with c1:
                st.image(
                    image,
                    use_column_width="auto",
                    channels="RGB"

                )
            with c2:
                age = get_player_age(selected_player)
                st.markdown(f"**Age:** {age}")
                country = get_player_country(selected_player)
                st.markdown(f"**Country:** {country}")
                position = get_player_position(selected_player)
                st.markdown(f"**Position:** {position}")
                school = get_player_school(selected_player)
                st.markdown(f"**School:** {school}")

    with col2:
        with st.container():
            tab1, tab2 = st.tabs(["Short Chart", "HeatMap"])

            with tab1:
                st.header("This is Shortchart")
                st.write("Short chart for {}".format(selected_player))
                fig, ax = plt.subplots()
                xlim = (-250, 250)
                ylim = (422.5, -47.5)
                ax = plt.gca()
                ax.set_xlim(xlim[::-1])
                ax.set_ylim(ylim[::-1])
                draw_court(ax, outer_lines=False)
                st.pyplot(fig)

            with tab2:
                st.header("This is for heatmap")
                st.write("Heat map for {}".format(selected_player))
                draw_court(ax, outer_lines=False)
                st.pyplot(fig)