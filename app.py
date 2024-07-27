import streamlit as st
import matplotlib.pyplot as plt
from urllib.request import urlretrieve
from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats
import numpy as np
from matplotlib import cm
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch, Polygon, PathPatch
from matplotlib.collections import PatchCollection
from matplotlib.colors import LinearSegmentedColormap, ListedColormap, BoundaryNorm
from matplotlib.path import Path

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
