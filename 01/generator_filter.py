"""Script read file and apply filter"""
import os


def read_file_with_filter(file, search_words=None):
    """Get rows from file which contains any from search words"""
    if search_words:
        search_words_set = set(x.lower() for x in search_words)
    if isinstance(file, str):
        file = open(file, 'r', encoding='utf-8')

    with file as file_obj:
        for line in file_obj:
            clear_line = line.rstrip(os.linesep)
            if search_words:
                line_words_set = set(x.lower() for x in clear_line.split(' '))
                if len(search_words_set.intersection(line_words_set)) > 0:
                    yield clear_line
            else:
                yield clear_line
