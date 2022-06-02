
"""A simplified version of class_conllx used in conllu_analysis"""
from pathlib import Path
import pandas as pd

# class sentence contains text, sentenceText, and a DataFrame containing token information
class Sentence:
    def __init__(self, text='', sentence_tokens='', tree_tokens='', 
                sentence_comments=None, dependency_tree=None):
        self.id = -1
        self.text = text
        self.sentence_tokens = sentence_tokens
        self.tree_tokens = tree_tokens
        if sentence_comments is None:
            sentence_comments = []
        self.sentence_comments = sentence_comments
        if dependency_tree is None:
            dependency_tree = []
        self.dependency_tree = dependency_tree


class Conllx:
    """
    Contains methods responsible for reading/writing conllx files,
    as well as converting between conllx and DataFrame formats.
    Conllx can also add catibex to the conllx file and
    run parse from maltparser.
    """

    def __init__(self, file_name='', file_path=None, file_data=None):
        if file_data is None:
            file_data = []
        if file_path is None:
            file_path = 'data'

        self.file_data = file_data
        self.file_path = file_path
        self.file_name = file_name

    @staticmethod
    def get_conllx_header():
        return ['ID', 'FORM', 'LEMMA', 'UPOS', 'XPOS',
            'FEATS', 'HEAD', 'DEPREL', 'DEPS', 'MISC']

    def __len__(self):
        return len(self.file_data)

    def read_file(self):
        """
        Reads a file. Removes extra whitespaces, newlines, and carriage returns 
        from the end of lines.
        """
        data = []
    
        # sometimes a character that is not valid in utf8 is used, use this line
        # with open(Path(self.file_path) / self.file_name, encoding='latin-1') as file:
        with open(Path(self.file_path) / self.file_name, encoding='utf-8-sig') as file:
            data = file.readlines()
        
        data = [x.rstrip() for x in data]
        data = [x+'\n' for x in data if x != '\n']
        self.file_data = data

    def conllx_to_sentence_list(self, columns=None):
        """
        Converts the conllx file to a list of Sentence objects.

        A Sentence object contains text and sentenceText variables,
        as well as a DataFrame of the dependency tree
        """
        assert self.file_data != [], "conllx file is empty!"
        
        if not columns: # if columns are not provided (i.e. Conll)
            columns = Conllx.get_conllx_header()

        data = self.file_data

        sentence_list = []
        i = 0
        while i < len(data):
            temp_sentence = Sentence()
            temp_sentence.id = len(sentence_list) # assigns an id to the sentence
            temp_list = []
            while i < len(data) and data[i].strip('\n') + '\n' != '\n':
                if data[i].startswith('# text'):
                    temp_sentence.text = data[i][9:].strip()
                # not using sentence_tokens for now
                # elif data[i].startswith('# sentenceTokens'):
                #     temp_sentence.sentence_tokens = data[i][19:].strip()
                # treeTokens and sentenceText are stored in tree_tokens
                elif data[i].startswith('# treeTokens'):
                    temp_sentence.tree_tokens = data[i][15:].strip()
                elif data[i].startswith('# sentenceText'):
                    temp_sentence.tree_tokens = data[i][17:].strip()
                elif data[i].startswith('#'): # keep a list of non-text comments
                    temp_sentence.sentence_comments.append(data[i].strip())
                else:
                    temp_list.append(data[i].rstrip('\n'))
                i += 1
            i += 1
            # print('here')
            # print(temp_list)
            temp_df = pd.DataFrame([x.split('\t')
                                    for x in temp_list], columns=columns)
            temp_df = temp_df.astype({'ID': 'int64', 'HEAD': 'int64'})
            
            # if Conll columns are used, add missing columns
            if list(temp_df.columns) != Conllx.get_conllx_header():
                temp_df = Conllx.add_missing_columns(temp_df)
            
            temp_sentence.dependency_tree = temp_df
            
            if not temp_sentence.dependency_tree.empty:
                sentence_list.append(temp_sentence)
            elif temp_sentence.text or temp_sentence.sentence_comments:
                raise ValueError('no dependency tree, yet comments are present!')
        return sentence_list