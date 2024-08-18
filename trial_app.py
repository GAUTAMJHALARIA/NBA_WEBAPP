import streamlit as st
import matplotlib.pyplot as plt
from urllib.request import urlretrieve
from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import seaborn as sns
from NBA_DATA import *
from matplotlib import cm
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch, Polygon, PathPatch
from matplotlib.collections import PatchCollection
from matplotlib.colors import LinearSegmentedColormap, ListedColormap, BoundaryNorm
from matplotlib.path import Path


st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.sidebar.title("NBA Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Player Statistics', 'Team Statistics')
)


def get_player_img(player_id):
    """
    Returns the image of the player from stats.nba.com as a numpy array and
    saves the image as PNG file in the current directory.

    Parameters
    ----------
    player_id: int
        The player ID used to find the image.

    Returns
    -------
    player_img: ndarray
        The multidimensional numpy array of the player image, which matplotlib
        can plot.
    """
    url = "https://cdn.nba.com/headshots/nba/latest/1040x760/{}.png".format(player_id)
    img_file = str(player_id) + ".png"
    pic = urlretrieve(url, img_file)
    player_img = plt.imread(pic[0])
    return player_img


def get_players_shotchartdetail(player_name, season_id):
    # creating player dictionary
    nba_player = players.get_players()
    player_dict = [player for player in nba_player if player['full_name'] == player_name][0]

    # creating players career dataframe
    career = playercareerstats.PlayerCareerStats(player_id=player_dict['id'])
    career_df = career.get_data_frames()[0]

    # geting team_id of the season
    team_id = career_df[career_df["SEASON_ID"] == season_id]['TEAM_ID']

    # creating shotchart  dataframe
    shotchart_df = shotchartdetail.ShotChartDetail(team_id=int(team_id),
                                                   player_id=int(player_dict['id']),
                                                   season_type_all_star='Regular Season',
                                                   season_nullable=season_id,
                                                   context_measure_simple="FGA"
                                                   ).get_data_frames()
    return shotchart_df[0], shotchart_df[1]  # shot details and league average


# drawing court function
def draw_court(ax=None, color="blue", lw=1, outer_lines=False):
    if ax is None:
        ax = plt.gca()

    # Basketball Hoop
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # backboard
    backboard = Rectangle((-30, -12.5), 60, 0, linewidth=lw, color=color)

    # The paint
    # outer box
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    # inner box
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)

    # Free Throw Top Arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)

    # Free Bottom Top Arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)

    # Restricted Zone
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

    # Three Point Line
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)

    # list of court shapes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw, bottom_free_throw, restricted,
                      corner_three_a, corner_three_b, three_arc, center_outer_arc, center_inner_arc]

    # outer_lines=True
    if outer_lines:
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw, color=color, fill=False)
        court_elements.append(outer_lines)

    for element in court_elements:
        ax.add_patch(element)
    court_elements = [hoop]

    for elements in court_elements:
        ax.add_patch(elements)


# shot chart function
def shot_chart(data, title="", xlim=(-250, 250), ylim=(422.5, -47.5), line_color="blue", court_color="white",
               court_lw=2, outer_lines=False, flip_court=False, gridsize=None, ax=None, despine=False):
    if ax is None:
        ax = plt.gca()

    if not flip_court:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    else:
        ax.set_xlim(xlim[::-1])
        ax.set_ylim(ylim[::-1])

    ax.tick_params(labelbottom="off", labelleft="off")
    ax.set_title(title, fontsize=18)

    # draws the court
    draw_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines)

    # separate color by make or miss

    x_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_X']
    y_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_Y']

    x_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_X']
    y_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_Y']

    ax.scatter(x_missed, y_missed, c='r', marker="x", s=300, linewidth=3, alpha=0.4)
    ax.scatter(x_made, y_made, facecolors='none', edgecolors='g', marker='o', s=100, linewidths=3, alpha=0.4)

    # set the spine to match the rest of court lines , makes outerlines somewhaat unnecessary

    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

    return ax


player_shotchart_df, league_avg = get_players_shotchartdetail("LeBron James", "2019-20")
image = get_player_img(2544)
players_list = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming']

colm1, colm2 = st.columns(2, gap="small")
with colm1:
    with st.container():
        col1, col2 = st.columns(2, gap="large", )
        with col1:
            st.image(
                image,
                width=200,
                channels="RGB"
            )
            st.selectbox("players", players_list)

        with col2:
            st.markdown(f"**Age:** 38")
            st.markdown(f"**Country:** USA")
            st.markdown(f"**Position:** F")
            st.markdown(f"**School:** Vincent-St. Mary")
            st.markdown(f"**Draft Year:** 2003")
            st.markdown(f"**Championships:** 1")

with (colm2):
    fig,ax = plt.subplots()
    ax = shot_chart(player_shotchart_df, title="LeBron shot Chart 2019-20")
    st.pyplot(fig)


co1,co2 = st.columns(2)
with co1 :
    categories = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG3M', 'FT%', 'FG%', 'MIN', 'TOV']
    season_stats = [25, 10, 7, 2, 1, 3, 85, 45, 35, 5]  # Example season stats
    interval_stats = [30, 8, 6, 1, 0.5, 2, 80, 50, 40, 7]  # Example interval stats

    # Number of variables
    num_vars = len(categories)

    # Compute angle of each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Ensure the plot is circular

    # The radar chart requires the data to be in circular form
    season_stats += season_stats[:1]
    interval_stats += interval_stats[:1]

    # Plotting
    fig1, ax1 = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # Draw one axe per variable
    ax1.set_theta_offset(np.pi / 2)
    ax1.set_theta_direction(-1)

    # Draw axis per variable and add labels
    plt.xticks(angles[:-1], categories)

    # Draw y-labels
    ax1.set_rscale('log')
    plt.yticks([10, 20, 30, 40, 50], ["10", "20", "30", "40", "50"], color="grey", size=7)
    plt.ylim(0, 50)

    # Plot data
    ax1.plot(angles, season_stats, linewidth=1, linestyle='solid', label="Season",marker=".")
    ax1.fill(angles, season_stats, 'b', alpha=0)

    ax1.plot(angles, interval_stats, linewidth=1, linestyle='solid', label="Interval",marker=".")
    ax1.fill(angles, interval_stats, 'r', alpha=0)

    # Add a legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    # Show the plot
    st.pyplot(fig1)



data = {
    'Season': ['2003-04', '2004-05', '2005-06', '2006-07', '2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20', '2020-21', '2021-22', '2022-23', '2023-24'],
    'MIN': [1000, 2000, 3000, 2500, 3200, 3100, 3000, 2800, 2900, 2700, 2600, 2500, 2400, 2300, 2200, 2100, 2000, 1900, 1800, 1700, 1600],
    'Games_Played': [50, 60, 70, 80, 75, 78, 76, 72, 74, 71, 70, 68, 67, 65, 63, 62, 60, 58, 56, 54, 52]
}

df = pd.DataFrame(data)
with co2:
    sns.set(style="darkgrid")

    # Create a figure and axis
    fig2, ax2 = plt.subplots(figsize=(12, 6))

    # Plot total minutes as a line plot
    ax2.plot(df['Season'], df['MIN'], color='b', marker='o', label='MIN')
    ax2.set_xlabel('Season')
    ax2.set_ylabel('Total Minutes', color='b')
    ax2.tick_params(axis='y', labelcolor='b')

    # Create another axis for the bar plot
    ax3 = ax2.twinx()
    ax3.bar(df['Season'], df['Games_Played'], alpha=0.6, color='brown', label='Game Played')
    ax3.set_ylabel('Games Played', color='brown')
    ax3.tick_params(axis='y', labelcolor='brown')

    # Add legends
    ax2.legend(loc='upper left')
    ax3.legend(loc='upper right')

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Show the plot
    plt.title('Total Minutes and Games Played per Season')
    st.pyplot(fig2)

st.header("Some other player statistic chart")
t1, t2, t3, t4, t5, t6, t7, t8, t9, t10 = st.tabs(
    ["MIN", "PTS", "FG_PCT", "FG3M", "FT_PCT", "REB", "AST", "STL", "BLK", "TOV"])

with t1:
    player_id = '2544'  # Replace with the player's ID
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    stats = career.get_data_frames()[0]

    # Filter data for relevant columns
    df = stats[['SEASON_ID', 'MIN', 'GP']].copy()
    df['SEASON_ID'] = df['SEASON_ID'].apply(lambda x: int(x.split('-')[0]))

    trace1 = go.Scatter(
        x=df['SEASON_ID'],
        y=df['MIN'],
        mode='lines+markers',
        name='Total Minutes',
        line=dict(color='blue'),
        marker=dict(size=8),
        hovertemplate='Season: %{x}<br>Total Minutes: %{y}<extra></extra>',

    )
    text = [g for g in zip(df['GP'])],
    trace2 = go.Bar(
        x=df['SEASON_ID'],
        y=df['GP'] * 20,
        name='Games Played',
        marker=dict(color='brown'),
        opacity=0.6,
        hovertemplate=('Season: %{x}<br>Games Played: %{customdata} <extra></extra>'),
        customdata=df['GP']
    )

    # Create the layout
    layout = go.Layout(
        title='NBA Player Minutes and Games Played Over Seasons',
        xaxis=dict(title='Season'),
        yaxis=dict(title='Total Minutes', tickvals=[1000, 2000, 3000]),
        yaxis2=dict(title='Games Played', overlaying='y', side='right'),
        legend=dict(x=0.1, y=1.1, orientation='h'),
    )

    # Create the figure

    fig = go.Figure(data=[trace1, trace2], layout=layout)

    # Display the figure
    st.plotly_chart(fig)

with t2:
    pass
with t3:
    pass
with t4:
    pass
with t5:
    pass
with t6:
    pass
with t7:
    pass
with t8:
    pass
with t9:
    pass
with t10:
    pass
