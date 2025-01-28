import requests

def get_gog_game_list():
    url = 'https://api.gog.com/games'
    response = requests.get(url)
    data = response.json()
    return data