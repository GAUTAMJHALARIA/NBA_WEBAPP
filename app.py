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
    season_id = get_season_id_list(selected_player)
    selected_season = st.sidebar.selectbox("select season", season_id)
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
                fig3, ax3 = plt.subplots()
                hexmap_chart(shot_chart_df, league_avg)
                st.pyplot(fig3)

    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10 = st.tabs(
        ["MIN", "PTS", "FG_PCT", "FG3_PCT", "FT_PCT", "REB", "AST", "STL", "BLK", "TOV"])

    with t1:
        st.plotly_chart(line_bar_plot(selected_player, "MIN", title='Total Minutes', scale=20))
    with t2:
        st.plotly_chart(line_bar_plot(selected_player, "PTS", title="Total Points", scale=20))
    with t3:
        st.plotly_chart(line_bar_plot(selected_player, "FG_PCT", title="Field Goal%", scale=1 / 150))
    with t4:
        st.plotly_chart(line_bar_plot(selected_player, "FG3_PCT", title="Field Goal 3%", scale=1 / 150))
    with t5:
        st.plotly_chart(line_bar_plot(selected_player, "FT_PCT", title="Free Throw%", scale=1 / 150))
    with t6:
        st.plotly_chart(line_bar_plot(selected_player, "REB", title="Total Rebounds", scale=5))
    with t7:
        st.plotly_chart(line_bar_plot(selected_player, "AST", title="Total Assist", scale=5))
    with t8:
        st.plotly_chart(line_bar_plot(selected_player, "STL", title="Total Steals", scale=1))
    with t9:
        st.plotly_chart(line_bar_plot(selected_player, "BLK", title="Total Blocks", scale=1))
    with t10:
        st.plotly_chart(line_bar_plot(selected_player, "TOV", title="Total Turnover", scale=5))

    fig4,ax4 = plt.subplots(figsize = (25,20))
    fig4 =radar_chart(selected_player, selected_season)
    st.plotly_chart(fig4)

    fig5,ax5 = plt.subplots()
    fig5 = game_choropleth_map(selected_player,selected_season)
    st.plotly_chart(fig5)

