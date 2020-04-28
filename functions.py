import os
import shutil
from pymkv import MKVFile
import logging

from api_functions import get_show_id
from auxiliary_functions import check_subtitles, check_and_create_directory
from classes import EquivalencyList
from string_functions import get_season_and_episode, get_show_name


def files_standardizer(files: list, tv_show_names_equivalency_list: EquivalencyList, api_key) -> list:
    files = [{'input_file_path': x,
              'input_filename': x.split('\\')[-1],
              'input_extension': x.split('.')[-1]} for x in files]

    for episode in files:
        episode['season_number'], episode['episode_number'] = get_season_and_episode(episode['input_filename'])
        episode['tv_show_name'] = get_show_name(episode['input_filename'])
        if tv_show_names_equivalency_list.get_from_list(episode['tv_show_name']):
            episode['tv_show_name'] = tv_show_names_equivalency_list.get_from_list(episode['tv_show_name'])
        episode['show_id'], show_name = get_show_id(episode['tv_show_name'], api_key)
        tv_show_names_equivalency_list.add_to_list({episode['tv_show_name']: show_name})
        episode['tv_show_name'] = show_name

    return files


def process_file(file: dict, temp_folder: str):
    logging.info(f"Processing file {file['input_file_path']}...")
    if not file.get('subtitle_file_path'):
        logging.info("Subtitle not found!")
        if file['input_file_path'] != file['output_file_path']:
            logging.info("Moving file...")
            check_and_create_directory(file['output_file_path'])
            shutil.move(file['input_file_path'], file['output_file_path'])
    else:
        logging.info("Subtitle found!")
        if temp_folder:
            if not os.path.exists(temp_folder):
                logging.info(f'Temp dir does not exists. Creating {temp_folder}...')
                os.mkdir(temp_folder)
            file['temp_file_path'] = f"{temp_folder}\\{file['input_filename']}"
            logging.info(f"Copying file from {file['input_file_path']} to {file['temp_file_path']}...")
            shutil.copyfile(file['input_file_path'], file['temp_file_path'])
            file['temp_output_file_path'] = f"{file['temp_file_path'][:-4]}_output{file['temp_file_path'][-4:]}"

        mkv_input = file.get('temp_file_path')
        mkv_output = file.get('temp_output_file_path')
        if not mkv_input:
            mkv_input = file.get('input_file_path')
        if not mkv_output:
            mkv_output = file.get('output_file_path')

        if mkv_input == mkv_output:
            mkv_output = f"{mkv_input[:-4]}_output{mkv_input[-4:]}"

        mkv = MKVFile(mkv_input)
        if not check_subtitles(mkv):
            logging.info("Adding subtitle...")
            mkv.add_track(file['subtitle_file_path'])
            mkv.title = file['episode_name']
            mkv.tracks[-1].language = 'por'
            mkv.mux(mkv_output)
            check_and_create_directory(file['output_file_path'])
            logging.info(f'Moving {mkv_output} to {file["output_file_path"]}...')
            shutil.move(mkv_output, file['output_file_path'])
            logging.info(f"Removing {file['subtitle_file_path']}...")
            os.remove(file['subtitle_file_path'])
            if file['input_file_path'] != file['output_file_path']:
                logging.info(f"Removing {file['input_file_path']}...")
                os.remove(file['input_file_path'])
        else:
            logging.info("Subtitle already added. Skipping...")

        if file.get('temp_file_path'):
            logging.info(f"Removing temp file {mkv_input}...")
            os.remove(mkv_input)


def merge_video_and_subs_files(videos: list, subs: list) -> list:
    for subtitle in subs:
        for video_file in videos:
            if subtitle['tv_show_name'] == video_file['tv_show_name'] and subtitle['season_number'] == video_file['season_number'] and subtitle['episode_number'] == video_file['episode_number']:
                video_file.update({'subtitle_file_path': subtitle['input_file_path'],
                                   'subtitle_filename': subtitle['input_filename']})

    return videos
