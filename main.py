import logging

import api_functions
import auxiliary_functions
import classes
import functions
import string_functions

logging.basicConfig(level=logging.INFO)

CONFIG = auxiliary_functions.load_config()

INPUT_FOLDER = CONFIG['input_folder']
OUTPUT_FOLDER = CONFIG['output_folder']
API_KEY = CONFIG['api_key']
TEMP_FOLDER = CONFIG['temp_folder']


def main():
    logging.info('Starting script...')
    tv_show_names_equivalency_list = classes.EquivalencyList()
    tv_shows_info = classes.TVShowsInfo()

    logging.info('Extracting filenames...')
    mkv_files, srt_files = string_functions.extract_filenames(INPUT_FOLDER)

    logging.info('Standardizing filenames...')
    mkv_files = functions.files_standardizer(mkv_files, tv_show_names_equivalency_list, API_KEY)
    srt_files = functions.files_standardizer(srt_files, tv_show_names_equivalency_list, API_KEY)
    video_files = mkv_files

    video_files = functions.merge_video_and_subs_files(video_files, srt_files)

    logging.info('Getting episode names...')
    for file in video_files:
        episode_name = tv_shows_info.get_episode_name(file['tv_show_name'], file['season_number'],
                                                      file['episode_number'])
        if not episode_name:
            episode_info = api_functions.get_show_info(file['show_id'], API_KEY)
            tv_shows_info.add_to_list(episode_info)
            episode_name = tv_shows_info.get_episode_name(file['tv_show_name'], file['season_number'],
                                                          file['episode_number'])
        if episode_name:
            file['episode_name'] = episode_name

    logging.info('Generating output filenames...')
    for file in video_files:
        output_filename = f"{file['tv_show_name']} S{str(file['season_number']).zfill(2)}E{str(file['episode_number']).zfill(2)} - {file['episode_name']}.{file['input_extension']}"
        output_file_path = f"{OUTPUT_FOLDER}\\{file['tv_show_name']}\\Season {file['season_number']}\\{output_filename}"
        dict_to_add = {'output_filename': output_filename,
                       'output_file_path': output_file_path}
        file.update(dict_to_add)

    logging.info('Processing files...')
    for file in video_files:
        functions.process_file(file, TEMP_FOLDER)


if __name__ == '__main__':
    main()
