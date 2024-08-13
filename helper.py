import seaborn as sns
import pandas as pd
import plotly.graph_objs as go

from NBA_DATA import *
from urllib.request import urlretrieve
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc, PathPatch
from matplotlib.collections import PatchCollection
from matplotlib.path import Path
from matplotlib.colors import LinearSegmentedColormap, ListedColormap, BoundaryNorm
from scipy.stats import percentileofscore


def get_player_img(player_name):
    player_id = get_id(player_name)
    url = "https://cdn.nba.com/headshots/nba/latest/1040x760/{}.png".format(player_id)
    img_file = str(player_name) + ".png"
    pic = urlretrieve(url, img_file)
    player_img = plt.imread(pic[0])
    return player_img


def draw_court(ax=None, color="black", lw=1, outer_lines=False):
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

    for element in court_elements:
        ax.add_patch(element)

    return ax


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


def heatmap(data, title="", color="b",
            xlim=(-250, 250), ylim=(422.5, -47.5), line_color="white",
            court_color="white", court_lw=2, outer_lines=False,
            flip_court=False, gridsize=None,
            ax=None, despine=False, **kwargs):
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

    x = data['LOC_X']
    y = data['LOC_Y']

    sns.kdeplot(x=x, y=y, fill=True, cmap='inferno', ax=ax, alpha=1, n_levels=30, bw_adjust=1)

    ax.scatter(x, y, facecolors='w', s=2, linewidths=0.1, **kwargs)

    draw_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines)
    plt.gca().set_facecolor('black')
    # Set the spines to match the rest of court lines, makes outer_lines
    # somewhate unnecessary
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

    return ax


def sized_hexbin(ax, hc, hc2, cmap, norm):
    offsets = hc.get_offsets()
    orgpath = hc.get_paths()[0]
    verts = orgpath.vertices
    values1 = hc.get_array()
    values2 = hc2.get_array()
    ma = values1.max()
    patches = []

    for offset, val in zip(offsets, values1):
        # Adding condition for minimum size
        # offset is the respective position of each hexagons

        # remove 0 to compare frequency without 0s
        filtered_list = list(filter(lambda num: num != 0, values1))

        # we also skip frequency counts that are 0s
        # this is to discount hexbins with no occurences
        # default value hexagons are the frequencies
        if (int(val) == 0):
            continue
        elif (percentileofscore(filtered_list, val) < 33.33):
            # print(percentileofscore(values1, val))
            # print("bot")
            v1 = verts * 0.3 + offset
        elif (percentileofscore(filtered_list, val) > 69.99):
            # print(percentileofscore(values1, val))
            # print("top")
            v1 = verts + offset
        else:
            # print("mid")
            v1 = verts * 0.6 + offset

        path = Path(v1, orgpath.codes)
        patch = PathPatch(path)
        patches.append(patch)

    pc = PatchCollection(patches, cmap=cmap, norm=norm)
    # sets color
    # so hexbin with C=data['FGP']
    pc.set_array(values2)

    ax.add_collection(pc)
    hc.remove()
    hc2.remove()


def hexmap_chart(data, league_avg, title="", color="b",
                 xlim=(-250, 250), ylim=(422.5, -47.5), line_color="white",
                 court_color="#1a477b", court_lw=2, outer_lines=False,
                 flip_court=False, gridsize=None,
                 ax=None, despine=False, **kwargs):
    LA = league_avg.loc[:, ['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE', 'FGA', 'FGM']].groupby(
        ['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE']).sum()
    LA['FGP'] = 1.0 * LA['FGM'] / LA['FGA']
    player = data.groupby(['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE', 'SHOT_MADE_FLAG']).size().unstack(fill_value=0)
    player['FGP'] = 1.0 * player[1] / player.sum(axis=1)
    player_vs_league = (player.loc[:, 'FGP'] - LA.loc[:, 'FGP']) * 100

    data = pd.merge(data, player_vs_league, on=['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE'], how='right')

    if ax is None:
        ax = plt.gca()
        ax.set_facecolor(court_color)

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

    x = data['LOC_X']
    y = data['LOC_Y']

    # for diverging color map
    colors = ['#2b7cb6', '#abd9e9', '#ffffbf', '#fdaf61', '#d7191c']
    cmap = ListedColormap(colors)
    # The 5 colors are separated by -9, -3, 0, 3, 9
    boundaries = [-9, -3, 0, 3, 9]
    norm = BoundaryNorm(boundaries, cmap.N, clip=True)

    # first hexbin required for bincount
    # second hexbin for the coloring of each hexagons
    hexbin = ax.hexbin(x, y, gridsize=40, cmap=cmap, norm=norm, extent=[-275, 275, -50, 425])
    hexbin2 = ax.hexbin(x, y, C=data['FGP'], gridsize=40, cmap=cmap, norm=norm, extent=[-275, 275, -50, 425])
    sized_hexbin(ax, hexbin, hexbin2, cmap, norm)

    # Set the spines to match the rest of court lines, makes outer_lines
    # somewhate unnecessary
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

    return ax


def line_bar_plot(player_name, stat,title,scale):
    player_id = get_id(player_name)
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    stats = career.get_data_frames()[0]

    df = stats[
        ["SEASON_ID", "GP", "MIN", "FG_PCT", "FG3_PCT", "FT_PCT", "OREB", "DREB", "REB", "AST", "STL", "BLK", "TOV",
         "PTS", "PF"]].copy()
    df['SEASON_ID'] = df['SEASON_ID'].apply(lambda x: int(x.split('-')[0]))

    plot1 = go.Scatter(
        x=df['SEASON_ID'],
        y=df[stat],
        mode='lines+markers',
        name=stat,
        line=dict(color='blue'),
        marker=dict(size=8),
        hovertemplate='%{y}<extra></extra>'
    )
    plot2 = go.Bar(
        x=df['SEASON_ID'],
        y=df['GP'] * scale,
        name='Games Played',
        marker=dict(color='brown'),
        opacity=0.6,
        hovertemplate='Season: %{x}<br>Games Played: %{customdata} <extra></extra>',
        customdata=df['GP']
    )
    layout = go.Layout(
        xaxis=dict(title='Season', tickvals = df['SEASON_ID']),
        yaxis=dict(title=title.format(stat)),
        yaxis2=dict(title='Games Played', overlaying='y', side='right'),
        legend=dict(x=0.1, y=1.1, orientation='h'),
    )

    fig = go.Figure(data=[plot1, plot2], layout=layout)
    return fig

def radar_chart(player_name,season):
    game_stats = get_player_gamelogs(player_name,season)
    relevant_stats = ['PTS', 'AST', 'REB', 'STL', 'BLK', 'TOV', 'MIN', 'FG_PCT', 'FT_PCT', 'FG3M']

    season_stats = game_stats[relevant_stats].mean()
    def normalize_data(stats, stats_min, stats_max):
        return (stats - stats_min) / (stats_max - stats_min)

    normalized_season_stats = normalize_data(season_stats, season_stats.min(), season_stats.max())


    plot1 = go.Scatterpolar(
        r=normalized_season_stats.tolist() + [normalized_season_stats.tolist()[0]],  # Complete the loop
        theta=relevant_stats + [relevant_stats[0]],  # Complete the loop
        name='Season',
        line_color= 'blue'
    )

    # Function to update interval stats
    def get_interval_trace(interval_size):
        interval_stats = game_stats[relevant_stats].head(interval_size).mean()
        normalized_interval_stats = normalize_data(interval_stats, season_stats.min(), season_stats.max())
        return normalized_interval_stats.tolist() + [normalized_interval_stats.tolist()[0]]  # Complete the loop

    # Initial interval size
    initial_interval_size = 5
    plot2_r_values = get_interval_trace(initial_interval_size)

    # Create the plot for interval stats
    plot2 = go.Scatterpolar(
        r=plot2_r_values,
        theta=relevant_stats + [relevant_stats[0]],  # Complete the loop
        name=f'Interval',
        line_color='red'
    )

    # Set up layout with slider
    layout = go.Layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        title= "Players Interval stats",
        showlegend=True,
        sliders=[{
            'active': initial_interval_size - 1,
            'currentvalue': {"prefix": "Interval Size: "},
            'pad': {"b": 10},
            'steps': [
                {
                    'label': f'Last {i + 1} Games',
                    'method': 'restyle',
                    'args': [
                        {'r': [get_interval_trace(i + 1)]},
                        [1]  # Target the second trace (interval trace)
                    ]
                } for i in range(len(game_stats))
            ]
        }]
    )

    # Create the figure and show it
    fig = go.Figure(data=[plot1, plot2], layout=layout)
    return fig

