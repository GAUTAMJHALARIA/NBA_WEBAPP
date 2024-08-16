from nba_api.stats.static import players
from datetime import datetime
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import BoxScoreSummaryV2

import pandas as pd


def get_game_location_df(player_name, season):
    game_logs = get_player_gamelogs(player_name=player_name, season=season)
    game_id_list = list(game_logs["Game_ID"])
    home_team_id = []
    for game_id in game_id_list:
        game_info = BoxScoreSummaryV2(game_id=str(game_id))
        home_team_id.append(game_info.game_summary.get_dict()['data'][0][6])

    city_list = []
    for i, game_id in zip(home_team_id, game_id_list):
        game_info = BoxScoreSummaryV2(game_id=str(game_id))
        temp_df = game_info.line_score.get_data_frame()
        city_name = temp_df[temp_df["TEAM_ID"] == i]["TEAM_CITY_NAME"]
        city_list.append(list(city_name)[0])

    nba_city_states = {
        'Atlanta': 'Georgia',
        'Baltimore': 'Maryland',  # No current team, former Bullets
        'Boston': 'Massachusetts',
        'Brooklyn': 'New York',
        'Charlotte': 'North Carolina',
        'Chicago': 'Illinois',
        'Cincinnati': 'Ohio',  # No current team, former Royals
        'Cleveland': 'Ohio',
        'Dallas': 'Texas',
        'Denver': 'Colorado',
        'Detroit': 'Michigan',
        'Fort Wayne': 'Indiana',  # No current team, former Pistons
        'Golden State': 'California',  # Warriors (current in San Francisco)
        'Houston': 'Texas',
        'Indiana': 'Indiana',
        'Kansas City': 'Missouri',  # No current team, former Kings
        'Los Angeles': 'California',  # For both Lakers and Clippers
        'LA': 'California',
        'Memphis': 'Tennessee',
        'Miami': 'Florida',
        'Milwaukee': 'Wisconsin',
        'Minnesota': 'Minnesota',
        'New Orleans': 'Louisiana',
        'New York': 'New York',  # Knicks
        'Newark': 'New Jersey',  # Former home of the Nets
        'Oklahoma City': 'Oklahoma',
        'Orlando': 'Florida',
        'Philadelphia': 'Pennsylvania',
        'Phoenix': 'Arizona',
        'Portland': 'Oregon',
        'Rochester': 'New York',  # No current team, former Royals
        'Sacramento': 'California',
        'Salt Lake City': 'Utah',
        'San Antonio': 'Texas',
        'San Diego': 'California',  # No current team, former Clippers
        'Seattle': 'Washington',  # No current team, former SuperSonics
        'St. Louis': 'Missouri',  # No current team, former Hawks
        'Syracuse': 'New York',  # No current team, former Nationals
        'Toronto': 'Ontario',  # Canada, only current Canadian team
        'Vancouver': 'British Columbia',  # Canada, former Grizzlies team
        'Washington': 'District of Columbia',
        'Las Vegas': 'Nevada',  # No current NBA team, potential future expansion
        'Louisville': 'Kentucky',  # No current NBA team, potential future expansion
        'New Jersey': 'New Jersey',
        'Akron': 'Ohio',  # Former home of the Akron Firestone Non-Skids, early NBL team
        'Chicago Heights': 'Illinois',  # Former home of the Chicago Stags, early BAA team
        'Flint': 'Michigan',  # Former home of the Flint Tropics, early NBL team
        'Jersey City': 'New Jersey',  # Former home of the Jersey Reds, early NBL team
        'Pittsburgh': 'Pennsylvania',  # Former home of the Pittsburgh Pirates (BAA team)
        'Providence': 'Rhode Island',  # Former home of the Providence Steamrollers, early NBA team
        'Utah': 'Utah'
    }
    state_abbrev = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO',
        'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
        'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
        'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
        'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
        'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA',
        'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY', 'Ontario': 'ON',
        'District of Columbia': 'DC'
    }
    df = pd.DataFrame(city_list).value_counts().sort_values().reset_index().rename(
        columns={0: "City", "count": "Game Played"})
    states = []
    for city in df["City"].str.split("/"):
        states.append(nba_city_states[city[0]])
    df["State"] = states

    final_df = df.groupby("State")["Game Played"].sum().reset_index()
    state_iso2 = []
    for state in final_df["State"]:
        state_iso2.append(state_abbrev[state])
    final_df["State_ISO2"] = state_iso2


    temp_df = df.groupby(["State", "City"])["Game Played"].sum().reset_index()

    data = []
    for state in final_df["State"]:
        data.append(temp_df[temp_df["State"] == state][["City", "Game Played"]].set_index("City").rename(
            columns={"count": "Cities"}).to_dict())

    final_df["Data"] = data

    return final_df


def get_player_gamelogs(player_name, season):
    player_id = get_id(player_name)
    player_gamelog = playergamelog.PlayerGameLog(player_id=player_id, season=season)
    game_stats = player_gamelog.get_data_frames()[0]

    return game_stats


def get_season_id_list(player_name):
    player_id = get_id(player_name=player_name)
    career_df = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]
    seasons = career_df["SEASON_ID"]
    return seasons


def get_players_name_list():
    players_info = players.get_players()
    player_names_list = [player["full_name"] for player in players_info]
    player_names_list = sorted(player_names_list)
    return player_names_list


def get_id(player_name):
    players_info = players.get_players()
    player_id = [player["id"] for player in players_info if player["full_name"] == player_name]
    return player_id[0]


def get_player_age(player_name):
    player_id = get_id(player_name)
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_dict()
    birth_date_str = player_info['resultSets'][0]['rowSet'][0][7]  # Birthdate is typically at index 7
    birth_date = datetime.strptime(birth_date_str[0:10], '%Y-%m-%d')

    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    return age


def get_player_country(player_name):
    player_id = get_id(player_name)
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_dict()
    country = player_info['resultSets'][0]['rowSet'][0][9]

    return country


def get_player_position(player_name):
    player_id = get_id(player_name)
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_dict()
    position = player_info['resultSets'][0]['rowSet'][0][15]

    return position


def get_player_school(player_name):
    player_id = get_id(player_name)
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_dict()
    school = player_info['resultSets'][0]['rowSet'][0][8]
    return school


def player_shotchart_detail(player_name, season_id):
    player_id = get_id(player_name)
    career_df = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]
    team_id = career_df[career_df["SEASON_ID"] == season_id]['TEAM_ID']
    shot_chart_df = shotchartdetail.ShotChartDetail(team_id=team_id,
                                                    player_id=player_id,
                                                    season_nullable=season_id,
                                                    season_type_all_star='Regular Season',
                                                    context_measure_simple='FGA'
                                                    ).get_data_frames()

    return shot_chart_df[0], shot_chart_df[1]
