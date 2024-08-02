from NBA_DATA import get_id
from urllib.request import urlretrieve
import matplotlib.pyplot as plt


def get_player_img(player_name):
    player_id = get_id(player_name)
    url = "https://cdn.nba.com/headshots/nba/latest/1040x760/{}.png".format(player_id)
    img_file = str(player_id) + ".png"
    pic = urlretrieve(url, img_file)
    player_img = plt.imread(pic[0])
    return player_img
