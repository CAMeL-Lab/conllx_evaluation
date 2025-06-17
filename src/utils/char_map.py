
# ..,;:?!؟،؛!.
punctuation_map = {
    '.': '.',
    '،': ',',
    '؛': ';',
    '؟': '?',
    '!': '!',
}

numbers_map = {
    '٠': '0',
    '١': '1',
    '٢': '2',
    '٣': '3',
    '٤': '4',
    '٥': '5',
    '٦': '6',
    '٧': '7',
    '٨': '8',
    '٩': '9',
}

maps = {
    'punctuation': punctuation_map,
    'numbers': numbers_map,
}

def bw2ar_map_lines(conll_df, map_name):
    selected_map = maps[map_name]
    conll_df.FORM = conll_df.FORM.map(selected_map).fillna(conll_df.FORM)