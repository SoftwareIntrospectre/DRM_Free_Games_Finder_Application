import requests

def get_steam_game_list():
    url = 'https://api.steampowered.com/ISteamApps/GetAppList/v2'
    response = requests.get(url)
    data = response.json()
    return data