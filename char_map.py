
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

def bw2ar_map_line(line, selected_map):
    for k, v in selected_map.items():
        line = line.replace(k, v)
    return line

def bw2ar_map_lines(lines, map_name):
    selected_map = maps[map_name]
    return [bw2ar_map_line(line, selected_map) for line in lines]