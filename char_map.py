
# ..,;:?!؟،؛!.
punctuation_map = {
    '.': '.',
    ',': '،',
    ';': '؛',
    '?': '؟',
    '!': '!',
}

numbers_map = {
    '0': '٠',
    '1': '١',
    '2': '٢',
    '3': '٣',
    '4': '٤',
    '5': '٥',
    '6': '٦',
    '7': '٧',
    '8': '٨',
    '9': '٩',
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