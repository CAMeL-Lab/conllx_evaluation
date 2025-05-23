import os
from pathlib import Path

from utils.char_map import bw2ar_map_lines
from utils.normalization import normalize_alef_yeh_ta

def get_file_names(data_path, endswith=''):
    ret_files = []
    if not os.path.isdir(Path(data_path)):
        raise FileNotFoundError(f'Directory not found: {data_path}')
    for dirpath, _, files in os.walk(data_path):
        print(f"Found directory: {dirpath}")

        for file_name in files:
            ret_files.append(file_name)
        
        if 'Icon\r' in ret_files:
            ret_files.remove('Icon\r')
        if '.DS_Store' in ret_files:
            ret_files.remove('.DS_Store')
        
        if endswith:
            ret_files = [f_name for f_name in ret_files if f_name.endswith(endswith)]
        # done within the os.walk for loop so 
        # it doesn't traverse subdirectories
        return ret_files

def transliterate_and_normalize(arguments, gold_conllx, parsed_conllx):
    if arguments['--transliterate_pnx']:
        bw2ar_map_lines(gold_conllx.df, 'punctuation')
        bw2ar_map_lines(parsed_conllx.df, 'punctuation')
    if arguments['--transliterate_num']:
        bw2ar_map_lines(gold_conllx.df, 'numbers')
        bw2ar_map_lines(parsed_conllx.df, 'numbers')
    if arguments['--normalize_alef_yeh_ta']:
        normalize_alef_yeh_ta(gold_conllx.df)
        normalize_alef_yeh_ta(parsed_conllx.df)