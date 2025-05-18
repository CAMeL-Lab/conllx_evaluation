import pytest
import pandas as pd

from align_trees import align_trees
from src.conllx_df import ConllxDf
from src.tree_evaluation import compare_conll_trees, evaluate_tree_tokens

@pytest.fixture
def gold_tree():
    return pd.read_csv('tests/data/gold_sample.tsv', sep='\t')

@pytest.fixture
def parsed_tree():
    return pd.read_csv('tests/data/parsed_sample.tsv', sep='\t')

def test_evaluate_tree_tokens(gold_tree, parsed_tree):
    new_g, new_p = align_trees(gold_tree, parsed_tree)
    tree_token_scores = evaluate_tree_tokens(new_g, new_p, gold_tree.shape[0], parsed_tree.shape[0])
    assert tree_token_scores['tokenization_f1_score'].round(3) == 88.000
    assert tree_token_scores['tokenization_precision'].round(3) == 84.615
    assert tree_token_scores['tokenization_recall'].round(3) == 91.667

def test_compare_conll_trees():
    gold_conll = ConllxDf('tests/data/gold_sample_2.conllx')
    parsed_conll = ConllxDf('tests/data/parsed_sample_2.conllx')
    
    conll_token_scores = compare_conll_trees(gold_conll, parsed_conll)
    assert conll_token_scores['tokenization_f1_score'].round(3) == 90.444
    assert conll_token_scores['tokenization_precision'].round(3) == 90.774
    assert conll_token_scores['tokenization_recall'].round(3) == 90.385
