import sys
sys.path.insert(0, 'src')

import pytest
import pandas as pd

from src.align_trees import align_trees
from src.conllx_df import ConllxDf
from src.tree_evaluation import compare_conll_trees, evaluate_columns, evaluate_las, evaluate_tree_tokens

@pytest.fixture
def gold_tree():
    return pd.read_csv('tests/data/gold_sample.tsv', sep='\t')

@pytest.fixture
def parsed_tree():
    return pd.read_csv('tests/data/parsed_sample.tsv', sep='\t')

def test_evaluate_tree_tokens(gold_tree, parsed_tree):
    new_g, new_p = align_trees(gold_tree, parsed_tree)
    tree_token_scores = evaluate_tree_tokens(new_g.FORM, new_p.FORM, gold_tree.shape[0], parsed_tree.shape[0])
    assert tree_token_scores['tokenization_f1_score'].round(3) == 88.000
    assert tree_token_scores['tokenization_precision'].round(3) == 84.615
    assert tree_token_scores['tokenization_recall'].round(3) == 91.667

def test_evaluate_columns_pos(gold_tree, parsed_tree):
    new_g, new_p = align_trees(gold_tree, parsed_tree)
    pos_score = evaluate_columns(new_g['UPOS'], new_p['UPOS'], gold_tree.shape[0])
    assert pos_score.round(3) == 75.0

def test_evaluate_label(gold_tree, parsed_tree):
    new_g, new_p = align_trees(gold_tree, parsed_tree)
    pos_score = evaluate_columns(new_g['DEPREL'], new_p['DEPREL'], gold_tree.shape[0])
    assert pos_score.round(3) == 8.333

def test_evaluate_uas(gold_tree, parsed_tree):
    new_g, new_p = align_trees(gold_tree, parsed_tree)
    pos_score = evaluate_columns(new_g['HEAD'], new_p['HEAD'], gold_tree.shape[0])
    assert pos_score.round(3) == 8.333

def test_evaluate_las(gold_tree, parsed_tree):
    new_g, new_p = align_trees(gold_tree, parsed_tree)
    pos_score = evaluate_las(new_g, new_p, gold_tree.shape[0])
    assert pos_score == 0.0


def test_compare_conll_trees():
    gold_conll = ConllxDf('tests/data/wiki/wiki_sample_gold/CamelTB_WikiNews_art_1.conllx')
    parsed_conll = ConllxDf('tests/data/wiki/wiki_sample_parsed/CamelTB_WikiNews_art_1.conllx')
    
    conll_scores = compare_conll_trees(gold_conll, parsed_conll)	
    assert conll_scores['tokenization_f1_score'].round(3) == 93.865
    assert conll_scores['tokenization_precision'].round(3) == 92.727
    assert conll_scores['tokenization_recall'].round(3) == 95.031
    assert conll_scores['pos'].round(3) == 86.335
    assert conll_scores['uas_score'].round(3) == 86.957
    assert conll_scores['label_score'].round(3) == 88.199
    assert conll_scores['las_score'].round(3) == 83.851
    assert conll_scores['pp_uas_score'].round(3) == 30.000
    assert conll_scores['pp_label_score'].round(3) == 40.000
    assert conll_scores['pp_las_score'].round(3) == 30.000
    # TODO add functionality to get these
    # word acc 89.116
