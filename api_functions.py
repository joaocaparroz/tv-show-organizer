import re

import requests


def get_show_id(name: str, api_key: str):
    params = {
        'api_key': api_key,
        'query': name
    }
    response = requests.get(f'https://api.themoviedb.org/3/search/tv', params=params)

    show_info = response.json()

    if show_info['total_results'] > 1:
        show_list = [x['name'] for x in show_info['results']]
        if name not in show_list:
            show_str = [f"{i} - {show_list[i]}" for i in range(len(show_list))]
            show_str = '\n'.join(show_str)
            selection = input(f'Select the corresponding match to ***{name}***: \n' + show_str + '\n')
            return show_info['results'][int(selection)]['id'], show_info['results'][int(selection)]['name']
        else:
            return show_info['results'][show_list.index(name)]['id'], show_info['results'][show_list.index(name)][
                'name']

    return show_info['results'][0]['id'], show_info['results'][0]['name']


def get_show_info(show_id: int, api_key: str):
    params = {
        'api_key': api_key
    }
    response = requests.get(f'https://api.themoviedb.org/3/tv/{show_id}', params=params)

    show_info = response.json()

    episode_list = list()

    for season in show_info['seasons']:
        season_info = get_season_info(season=season['season_number'], show_id=show_id, api_key=api_key)
        for episode in season_info['episodes']:
            episode_dict = {
                'tv_show_name': show_info['name'],
                'season': season['season_number'],
                'episode': episode['episode_number'],
                'episode_name': re.sub(r'[\\/\:*"<>\|%\$\^&£?]', "", episode['name'])
            }
            episode_list.append(episode_dict)

    return episode_list


def get_season_info(season, show_id: int, api_key: str):
    params = {
        'api_key': api_key
    }
    response = requests.get(f'https://api.themoviedb.org/3/tv/{show_id}/season/{season}', params=params)

    season_info = response.json()

    return season_info
