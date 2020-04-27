import logging


class EquivalencyList(object):
    def __init__(self):
        self.equivalence_list = {}

    def add_to_list(self, new_equivalency: dict):
        self.equivalence_list.update(new_equivalency)

    def get_from_list(self, value: str):
        return self.equivalence_list.get(value)


class TVShowsInfo(object):
    def __init__(self):
        self.shows_info = []

    def add_to_list(self, new_show_info: dict):
        self.shows_info += new_show_info

    def get_episode_name(self, tv_show_name, season, episode):
        logging.info(f'Getting episode name for {tv_show_name} S{season}E{episode}...')
        episode_list = [x for x in self.shows_info if
                        x['tv_show_name'] == tv_show_name and x['season'] == season and x['episode'] == episode]
        if len(episode_list) > 1:
            raise Exception('Tem mais de um episódio com esses dados!')
        elif len(episode_list) == 0:
            return None
        else:
            return episode_list[0].get('episode_name')