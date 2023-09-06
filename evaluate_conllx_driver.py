"""
Evaluates a parsed CoNLL file against gold or 
    a directory containing parsed CoNLL files against a gold directory.

Usage:
    evaluate_conllx_driver ((-g <gold> | --gold=<gold>) (-p <parsed> | --parsed=<parsed>) | ((--gold_dir=<gold_dir>) (--parsed_dir=<parsed_dir>)))
        [-x | --transliterate_pnx]
        [-n | --transliterate_num]
        [-a | --normalize_alef_yeh_ta]
    evaluate_conllx_driver (-h | --help)

Options:
    -g <gold> --gold=<gold>
        The gold CoNLL file.
    -p <parsed> --parsed=<parsed>
        The parsed CoNLL file.
    --gold_dir=<gold_dir>
        The directory containing gold CoNLL files.
    --parsed_dir=<parsed_dir>
        The directory containing parsed CoNLL files.
    -x --transliterate_pnx
        Transliterate punctuation to Roman script (punctuation will always match regardless of script)
    -n --transliterate_num
        Transliterate numbers to Roman script (numbers will always match regardless of script)
    -a --normalize_alef_yeh_ta
        Normalizes alef, alef maksura, and teh marbuta
    -h --help
        Show this screen.

"""

import pathlib
from docopt import docopt

from pandas import DataFrame, Series
from conllx_scores import get_scores_means
from conllx_counts import get_sentence_list_counts
from class_conllx import Conllx
from char_map import bw2ar_map_lines
from normalization import normalize_alef_yeh_ta
from utils import get_file_names

arguments = docopt(__doc__)

def get_synced_file_names(gold_file_names, parsed_file_names):
    tuple_list = []
    for gold_file in gold_file_names:
        # a_start = a_file
        parsed_file = [x for x in parsed_file_names if x == gold_file][0]
        tuple_list.append((gold_file, parsed_file))
    return tuple_list

def get_file_path_details(file_path):
    full_path = pathlib.Path(file_path)
    dir_path = full_path.parent
    file_name = full_path.name
    return dir_path, file_name

if __name__ == '__main__':
    if arguments["--gold"] and arguments["--parsed"]:
        gold_dir_path, gold_file_name = get_file_path_details(arguments["--gold"])
        parsed_dir_path, parsed_file_name = get_file_path_details(arguments["--parsed"])
        print('comparing two files')
        tuple_list = [(gold_file_name, parsed_file_name)]
    elif arguments["--gold_dir"] and arguments["--parsed_dir"]:
        print('comparing two directories')
        gold_dir_path = pathlib.Path(arguments["--gold_dir"])
        parsed_dir_path = pathlib.Path(arguments["--parsed_dir"])
        gold_file_names = get_file_names(arguments["--gold_dir"], '.conllx')
        parsed_file_names = get_file_names(arguments["--parsed_dir"], '.conllx')
        
        # matching files
        tuple_list = get_synced_file_names(gold_file_names, parsed_file_names)
    else:
        raise ValueError('Invalid arguments')


    # reading files and storing scores for each file
    tree_counts_list = []
    tree_matches_list = []
    alignment_numbers_list = []
    num_sentences_list = []

    for gold_file, parsed_file in tuple_list:
        gold_conllx = Conllx(file_name=gold_file, file_path=gold_dir_path)
        gold_conllx.read_file()
        parsed_conllx = Conllx(file_name=parsed_file, file_path=parsed_dir_path)
        parsed_conllx.read_file()
        if arguments['--transliterate_pnx']:
            gold_conllx.file_data = bw2ar_map_lines(gold_conllx.file_data, 'punctuation')
            parsed_conllx.file_data = bw2ar_map_lines(parsed_conllx.file_data, 'punctuation')
        if arguments['--transliterate_num']:
            gold_conllx.file_data = bw2ar_map_lines(gold_conllx.file_data, 'numbers')
            parsed_conllx.file_data = bw2ar_map_lines(parsed_conllx.file_data, 'numbers')
        if arguments['--normalize_alef_yeh_ta']:
            gold_conllx.file_data = normalize_alef_yeh_ta(gold_conllx.file_data)
            parsed_conllx.file_data = normalize_alef_yeh_ta(parsed_conllx.file_data)
        
        conllx_file_statistics = get_sentence_list_counts(gold_conllx.conllx_to_sentence_list(), parsed_conllx.conllx_to_sentence_list())
        tree_counts_list.append(conllx_file_statistics.tree_counts)
        tree_matches_list.append(conllx_file_statistics.tree_matches)
        alignment_numbers_list.append(conllx_file_statistics.alignment_numbers)
        num_sentences_list.append(conllx_file_statistics.sentence_number)

    subcorpus_scores = get_scores_means(tree_matches_list, tree_counts_list, num_sentences_list)

    # print("\t".join(map(str, list(Series(subcorpus_scores.__dict__.copy()).values))))
    # print(DataFrame(alignment_numbers_list).sum())
    print(Series(subcorpus_scores.__dict__.copy()))
    print()
    
    results = DataFrame(alignment_numbers_list).sum()
    results.to_csv('results.tsv', sep='\t', index=False)
