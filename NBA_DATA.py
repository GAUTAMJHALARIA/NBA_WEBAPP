from nba_api.stats.static import players
from datetime import datetime
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import shotchartdetail


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
