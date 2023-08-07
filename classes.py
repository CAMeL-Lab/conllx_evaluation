
from dataclasses import dataclass


@dataclass
class AlignmentNumbers:
    insertion_count: int
    deletion_count: int

@dataclass
class TreeMatches:
    tokenization_matches: int
    pos_matches: int
    uas_matches: int
    label_matches: int
    las_matches: int
    word_matches: int

@dataclass
class TreeCounts:
    ref_token_count: int
    pred_token_count: int
    full_token_count: int
    ref_word_count: int

@dataclass
class ConllxScores:
    tokenization_f_score: float
    tokenization_precision: float
    tokenization_recall: float
    word_accuracy: float
    pos: float
    uas: float
    label: float
    las: float

@dataclass
class ConllxStatistics:
    tree_counts: TreeCounts
    tree_matches: TreeMatches
    # conllx_scores: ConllxScores
    alignment_numbers: AlignmentNumbers
