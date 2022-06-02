
from typing import List
from pandas import DataFrame, Series


def get_children_ids_of(current_token_id, conllx_df) -> List[int]:
    """Returns a list of ids of the children of the current token.

    Args:
        current_token_id (int): ID of the parent token
        conllx_df (DataFrame): tree data

    Returns:
        List[int]: list of children ids
    """
    # return list(conllx_df[conllx_df['HEAD'] == str(current_token_id)]["ID"])
    return list(conllx_df[conllx_df['HEAD'] == current_token_id]["ID"])

def get_sentence_column_data(sen_df: DataFrame, column_name: str) -> List[Series]:
    """Given a sentence DataFrame, return the data of a column in a list

    Args:
        sen_df (DataFrame): a sentence
        column_name (str): name of column

    Returns:
        list: a column of the DataFrame
    """
    return list(sen_df[column_name])
