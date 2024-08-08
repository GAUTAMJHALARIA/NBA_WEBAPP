import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import seaborn as sns

from NBA_DATA import *
from helper import *

st.sidebar.title("NBA Analysis")
user_menu = st.sidebar.radio(
    'Select An Option',
    ('Player-wise', 'Team-wise')
)

if user_menu == 'Player-wise':
    col1, col2 = st.columns(2, vertical_alignment="top", gap="large")
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
            tab1, tab2, tab3 = st.tabs(["Short Chart", "HeatMap", "Hexmap"])
            season_id = get_season_id_list(selected_player)
            selected_season = st.selectbox("select season", season_id)
            with tab1:
                fig1, ax1 = plt.subplots()
                shot_chart_df, league_avg = player_shotchart_detail(player_name=selected_player,
                                                                    season_id=selected_season)
                shot_chart(line_color="black", data=shot_chart_df)
                st.pyplot(fig1)

            with tab2:
                fig2, ax2 = plt.subplots()
                heatmap(shot_chart_df)
                st.pyplot(fig2)

            with tab3:
                    fig3,ax3 = plt.subplots()
                    hexmap_chart(shot_chart_df,league_avg)
                    st.pyplot(fig3)


    st.header("Some other player statistic chart")
