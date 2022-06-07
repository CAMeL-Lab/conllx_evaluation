import pathlib

from pandas import DataFrame, Series
from conllx_scores import get_scores_means
from conllx_counts import get_sentence_list_counts
from class_conllx import Conllx
from handle_args import Argument, generate_argparser_with_arguments
from utils import get_file_names

SCRIPT_DESCRIPTION = 'This script takes 2 CoNLL-X files or 2 directories of ConllX files and evaluates the scores.'

def get_synced_file_names(gold_file_names, parsed_file_names):
    tuple_list = []
    for gold_file in gold_file_names:
        # a_start = a_file
        parsed_file = [x for x in parsed_file_names if x == gold_file][0]
        tuple_list.append((gold_file, parsed_file))
    return tuple_list

if __name__ == '__main__':
    arg_list = [
        Argument('-g', '--gold', str, 'the gold ConllX file'),
        Argument('-p', '--parsed', str, 'the parsed ConllX file'),
        Argument('-gd', '--gold_dir', str, 'the gold directory containing ConllX files'),
        Argument('-pd', '--parsed_dir', str, 'the parsed directory containing ConllX files')
        ]

    args = generate_argparser_with_arguments(arg_list, script_description=SCRIPT_DESCRIPTION)

    if args.gold and args.parsed:
        gold_full_path = pathlib.Path(args.gold)
        parsed_full_path = pathlib.Path(args.parsed)
        gold_dir_path = gold_full_path.parent
        parsed_dir_path = parsed_full_path.parent
        
        tuple_list = [(gold_full_path.name, parsed_full_path.name)]
    elif args.gold_dir and args.parsed_dir:
        gold_dir_path = pathlib.Path(args.gold_dir)
        parsed_dir_path = pathlib.Path(args.parsed_dir)
        gold_file_names = get_file_names(args.gold_dir, '.conllx')
        parsed_file_names = get_file_names(args.parsed_dir, '.conllx')
        
        # matching files
        tuple_list = get_synced_file_names(gold_file_names, parsed_file_names)
            
    # reading files and storing scores for each file
    tree_counts_list = []
    tree_matches_list = []
    alignment_numbers_list = []
    for gold_file, parsed_file in tuple_list:
        gold_conllx = Conllx(file_name=gold_file, file_path=gold_dir_path)
        gold_conllx.read_file()
        parsed_conllx = Conllx(file_name=parsed_file, file_path=parsed_dir_path)
        parsed_conllx.read_file()
        
        conllx_file_statistics = get_sentence_list_counts(gold_conllx.conllx_to_sentence_list(), parsed_conllx.conllx_to_sentence_list())
        tree_counts_list.append(conllx_file_statistics.tree_counts)
        tree_matches_list.append(conllx_file_statistics.tree_matches)
        alignment_numbers_list.append(conllx_file_statistics.alignment_numbers)
    
    subcorpus_scores = get_scores_means(tree_counts_list, tree_matches_list)

    print(Series(subcorpus_scores.__dict__.copy()))
    print(DataFrame(alignment_numbers_list).sum())
