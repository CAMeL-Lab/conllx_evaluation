import pandas as pd

from align_trees import align_trees
from conllx_df import ConllxDf


def evaluate_tree_tokens(ref_tree_tokens, pred_tree_tokens, total_ref_tree_token_count, total_pred_tree_token_count):
    # ref_tree and pred_tree have already been aligned
    # the original token counts are required to calculate the f1 score

    token_matches = (ref_tree_tokens == pred_tree_tokens).sum()

    token_recall = token_matches / total_ref_tree_token_count
    token_precision = token_matches / total_pred_tree_token_count
    f1_score = (2*token_precision*token_recall / (token_precision+token_recall))
    return {
        'tokenization_f1_score': f1_score*100,
        'tokenization_recall': token_recall*100,
        'tokenization_precision': token_precision*100,
    }

def evaluate_pos(ref_tree, pred_tree, total_ref_tree_token_count):
    return 100 * ((ref_tree['UPOS'] == pred_tree['UPOS']).sum() / total_ref_tree_token_count)

def evaluate_label(ref_tree, pred_tree, total_ref_tree_token_count):
    return 100 * ((ref_tree['DEPREL'] == pred_tree['DEPREL']).sum() / total_ref_tree_token_count)

def evaluate_uas(ref_tree, pred_tree, total_ref_tree_token_count):
    return 100 * ((ref_tree['HEAD'] == pred_tree['HEAD']).sum() / total_ref_tree_token_count)

def evaluate_las(ref_tree, pred_tree, total_ref_tree_token_count):
    return 100 * (((ref_tree['HEAD'] == pred_tree['HEAD']) & (ref_tree['DEPREL'] == pred_tree['DEPREL'])).sum() / total_ref_tree_token_count)


# TODO compares two full conll files and not single trees, possibly rename
def compare_conll_trees(ref_conll: ConllxDf, pred_conll: ConllxDf):
    assert ref_conll.get_sentence_count() == pred_conll.get_sentence_count()

    conll_tree_scores = []
    aligned_df_gold_list = []
    aligned_df_pred_list = []

    total_ref_tree_token_count = 0
    total_pred_tree_token_count = 0
    for i in range(ref_conll.get_sentence_count()):
        ref_tree = ref_conll.get_df_by_id(i)
        pred_tree = pred_conll.get_df_by_id(i)
        total_ref_tree_token_count += ref_tree.shape[0]
        total_pred_tree_token_count += pred_tree.shape[0]
        
        ref_tree_aligned, pred_tree_aligned = align_trees(ref_tree, pred_tree)
        aligned_df_gold_list.append(ref_tree_aligned)
        aligned_df_pred_list.append(pred_tree_aligned)
    
    gold_df = pd.concat(aligned_df_gold_list)
    pred_df = pd.concat(aligned_df_pred_list)
    
    # import pdb; pdb.set_trace()
    
    # f1_score, precision, and recall
    tokenization_scores = evaluate_tree_tokens(gold_df.FORM, pred_df.FORM, total_ref_tree_token_count, total_pred_tree_token_count)

    pos_score = {'pos': evaluate_pos(gold_df, pred_df, total_ref_tree_token_count)}
    
    attachment_scores = {
        'label_score': evaluate_label(gold_df, pred_df, total_ref_tree_token_count),
        'uas_score': evaluate_uas(gold_df, pred_df, total_ref_tree_token_count),
        'las_score': evaluate_las(gold_df, pred_df, total_ref_tree_token_count)
    }

    scores_combined = {**tokenization_scores, **pos_score, **attachment_scores}
    conll_tree_scores.append(scores_combined)

    # TODO conll_tree_scores var can possibly be removed
    mean_df = pd.DataFrame(conll_tree_scores).mean()
    return {
        'tokenization_f1_score': mean_df.tokenization_f1_score,
        'tokenization_precision': mean_df.tokenization_precision,
        'tokenization_recall': mean_df.tokenization_recall,
        'pos': mean_df.pos,
        'uas_score': mean_df.uas_score,
        'label_score': mean_df.label_score,
        'las_score': mean_df.las_score
    }

