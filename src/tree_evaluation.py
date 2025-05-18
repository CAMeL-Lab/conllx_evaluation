import pandas as pd
from sklearn.metrics import f1_score

from align_trees import align_trees
from src.conllx_df import ConllxDf


def evaluate_tree_tokens(ref_tree_tokens, pred_tree_tokens, ref_tree_token_count, pred_tree_token_count):
    # ref_tree and pred_tree have already been aligned
    # the original token counts are required to calculate the f1 score

    token_matches = (ref_tree_tokens == pred_tree_tokens).sum()

    token_recall = token_matches / ref_tree_token_count
    token_precision = token_matches / pred_tree_token_count
    f1_score = (2*token_precision*token_recall / (token_precision+token_recall))
    return {
        'tokenization_f1_score': f1_score*100,
        'tokenization_recall': token_recall*100,
        'tokenization_precision': token_precision*100,
    }

def evaluate_pos(ref_tree, pred_tree, ref_tree_token_count):
    return 100 * ((ref_tree['UPOS'] == pred_tree['UPOS']).sum() / ref_tree_token_count)

def evaluate_label(ref_tree, pred_tree, ref_tree_token_count):
    return 100 * ((ref_tree['DEPREL'] == pred_tree['DEPREL']).sum() / ref_tree_token_count)

def evaluate_uas(ref_tree, pred_tree, ref_tree_token_count):
    return 100 * ((ref_tree['HEAD'] == pred_tree['HEAD']).sum() / ref_tree_token_count)

def evaluate_las(ref_tree, pred_tree, ref_tree_token_count):
    return 100 * (((ref_tree['HEAD'] == pred_tree['HEAD']) & (ref_tree['DEPREL'] == pred_tree['DEPREL'])).sum() / ref_tree_token_count)


def compare_conll_trees(ref_conll: ConllxDf, pred_conll: ConllxDf):
    assert ref_conll.get_sentence_count() == pred_conll.get_sentence_count()

    conll_tree_scores = []
    for i in range(ref_conll.get_sentence_count()):
        ref_tree = ref_conll.get_df_by_id(i)
        pred_tree = pred_conll.get_df_by_id(i)

        ref_tree_aligned, pred_tree_aligned = align_trees(ref_tree, pred_tree)
        conll_tree_scores.append(evaluate_tree_tokens(ref_tree_aligned, pred_tree_aligned, ref_tree.shape[0], pred_tree.shape[0]))
    mean_df = pd.DataFrame(conll_tree_scores).mean()
    return {
        'tokenization_f1_score': mean_df.tokenization_f1_score,
        'tokenization_recall': mean_df.tokenization_recall,
        'tokenization_precision': mean_df.tokenization_precision
    }

