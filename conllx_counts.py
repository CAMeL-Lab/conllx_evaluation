""" This script contains functions used to evaluate two ConllX files.
The Sentence lists of the ConllX files are passed to the get_sentence_list_counts
functions, and the tokenization, POS tag, UAS, label, and LAS scores are computed.

First the sentences are aligned using ced_word_alignment,
then the scores for each sentence are computed.
Finally, the mean of each score is obtained for all sentences.

"""

from typing import List, Tuple

from pandas import DataFrame, Series
from align_trees import align_trees
from classes import AlignmentNumbers, ConllxStatistics, TreeCounts, TreeMatches
from class_conllx import Sentence


def get_alignment_numbers(gold_df, parsed_df):
    insertion_count = (gold_df['FORM'] == 'tok').sum()
    deletion_count = (parsed_df['FORM'] == 'tok').sum()
    
    return AlignmentNumbers(insertion_count, deletion_count)
    
def get_column_matches(col_1: Series, col_2: Series) -> float:
    """Returns the number of matches given two columns.

    Args:
        col_1 (Series): selected column of the first DataFrame
        col_2 (Series): selected column of the second DataFrame

    Returns:
        float: the number of matches given two columns
    """
    return (col_1 == col_2).sum()

def get_las_matches(head_1: Series, deprel_1: Series, head_2: Series, deprel_2: Series) -> float:
    """Returns the number of matches of the label and attachments between two trees
    (the HEAD and DEPREL columns).

    Args:
        head_1 (Series): HEAD column of the first tree
        deprel_1 (Series): DEPREL column of the first tree
        head_2 (Series): HEAD column of the second tree
        deprel_2 (Series): DEPREL column of the second tree

    Returns:
        float: the number of matches of the labels and attachments
    """
    # import pdb; pdb.set_trace()
    return ((head_1 == head_2) & (deprel_1 == deprel_2)).sum()

def get_tree_matches(gold_df: DataFrame, parsed_df: DataFrame) -> Tuple[TreeMatches, TreeCounts]:
    """Gets the matches of two trees. The matches are on
    tokenization, POS tags, UAS, label, and LAS
    
    assumption: gold_df and parsed_df are aligned by adding null alignment tok
    
    TODO: we insert null alignment tokens ... add to align_trees
    C=correct match
    S=Sub
    I=Inserted in prediction
    D=Deleted in prediction

    Length of Reference R=C+S+D (length of gold without null alignment tok)
    Length of Prediction P=C+S+I (length of parsed without null alignment tok)

    Precision of edits PREC= C / P (what is correct of the prediction)
    Recall of edits REC = C / R (what is correct of the reference)

    The Tokenization F-score = 2*PREC*REC / (PREC+REC)

    Args:
        gold_df (DataFrame): the first tree
        parsed_df (DataFrame): the second tree

    Returns:
        TreeMatches: matching scores of two the trees
    """
    assert gold_df.shape[0] == parsed_df.shape[0], 'trees must be aligned!'
    
    tokenization_matches = get_column_matches(gold_df['FORM'], parsed_df['FORM'])
    
    dfs = gold_df.merge(parsed_df, on='ID', suffixes=('_gold', '_parsed'))
    
    # remove insertions before calculating matches other than tokenization
    dfs = dfs[dfs['FORM_gold'] != 'tok']
    
    return TreeMatches(
        tokenization_matches,
        get_column_matches(dfs['UPOS_gold'], dfs['UPOS_parsed']),
        get_column_matches(dfs['HEAD_gold'], dfs['HEAD_parsed']),
        get_column_matches(dfs['DEPREL_gold'], dfs['DEPREL_parsed']),
        get_las_matches(dfs['HEAD_gold'], dfs['DEPREL_gold'], dfs['HEAD_parsed'], dfs['DEPREL_parsed']),
    )

def get_tree_counts(gold_df, parsed_df):
    assert gold_df.shape[0] == parsed_df.shape[0], 'trees must be aligned!'
    dfs = gold_df.merge(parsed_df, on='ID', suffixes=('_gold', '_parsed'))
    ref_token_count = dfs[dfs['FORM_gold'] != 'tok'].shape[0]
    pred_token_count = dfs[dfs['FORM_parsed'] != 'tok'].shape[0]
    return TreeCounts(
        ref_token_count,
        pred_token_count,
        gold_df.shape[0]
    )
    
def get_sentence_list_counts(
    gold_sen_list: List[Sentence], 
    parsed_sen_list: List[Sentence]
    ) -> ConllxStatistics:
    """Given two Sentence lists, compute the following scores:
    tokenization, POS tags, UAS, label, and LAS

    Args:
        gold_sen_list (List[Sentence]): first sentence list
        parsed_sen_list (List[Sentence]): second sentence list

    Returns:
        DataFrame: TreeCounts for all sentences
    """
    
    assert len(gold_sen_list) == len(parsed_sen_list)

    sentence_matches_list = []
    sentence_counts_list = []
    alignment_numbers_list = []
    for g_sen, p_sen in zip(gold_sen_list, parsed_sen_list):
        g_df = g_sen.dependency_tree.copy()
        p_df = p_sen.dependency_tree.copy()
        g_df, p_df = align_trees(g_df, p_df)
        
        sentence_counts_list.append(get_tree_counts(g_df, p_df))
        sentence_matches_list.append(get_tree_matches(g_df, p_df))
        alignment_numbers_list.append(get_alignment_numbers(g_df, p_df))
    
    sentence_counts = DataFrame(sentence_counts_list).sum()
    sentence_matches = DataFrame(sentence_matches_list).sum()
    alignment_numbers = DataFrame(alignment_numbers_list).sum()
    
    return ConllxStatistics(
        sentence_counts,
        sentence_matches,
        alignment_numbers
    )