from nba_api.stats.static import players


def get_players_name_list():
    players_info = players.get_players()
    player_names_list = [player["full_name"] for player in players_info]
    player_names_list = sorted(player_names_list)
    return player_names_list


def get_id(player_name):
    players_info = players.get_players()
    player_id = [player["id"] for player in players_info if player["full_name"] == player_name]
    return player_id[0]
