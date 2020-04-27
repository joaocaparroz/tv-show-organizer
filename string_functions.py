import os
import re
from typing import Tuple


def get_season_and_episode(filename) -> Tuple[int, int]:
    match = re.search(r'(?ix)(\d{1,2})(?:\.?[xe])(\d{1,2})', filename)
    if match:
        return int(match.group(1)), int(match.group(2))


def get_show_name(filename) -> str:
    match = re.search(r'(?ix)(.+)(?:[\s\.]S*\d{1,2}\.?[xe]\d{1,2})', filename)
    name = match.group(1).replace('.', ' ')
    name = re.sub(r' +', ' ', name)

    return name


def extract_filenames(input_folder: str) -> Tuple[list, list]:
    mkv_files = []
    srt_files = []
    for root, directories, filenames in os.walk(input_folder):
        for filename in filenames:
            if filename.endswith('.mkv'):
                mkv_files.append(os.path.join(root, filename))
            if filename.endswith('.srt'):
                srt_files.append(os.path.join(root, filename))

    return mkv_files, srt_files
