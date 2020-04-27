import json
import os
import logging


def load_config() -> dict:
    with open('config.json', encoding='utf-8') as json_file:
        config = json.load(json_file)

    return config


def check_subtitles(mkv, lang: str = 'por') -> bool:
    selected_language_subtitles = [x for x in mkv.tracks if x.track_type == 'subtitles' and x.track_codec == 'SubRip/SRT' and x.language == lang]
    return len(selected_language_subtitles) != 0


def check_and_create_directory(directory: str):
    check_directory_list = []
    for split in directory.split('\\')[:-1]:
        check_directory_list.append(split)
        check_directory_str = '\\'.join(check_directory_list)
        if not os.path.exists(check_directory_str):
            logging.info(f'Output directory does not exists. Creating {check_directory_str}')
            os.mkdir(check_directory_str)
