import plotly.graph_objs as go

from NBA_DATA import *

def  line_bar_plot(player_name,stat):
    player_id = get_id(player_name)
    career = playercareerstats.PlayerCareerStats(player_id = player_id)
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
        y=df['GP'] * 20,
        name='Games Played',
        marker=dict(color='brown'),
        opacity=0.6,
        hovertemplate='Season: %{x}<br>Games Played: %{customdata} <extra></extra>',
        customdata=df['GP']
    )