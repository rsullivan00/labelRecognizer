import re
from Levenshtein import distance
from keywords import Keywords
from label import Label
import numpy as np
from munkres import Munkres

pairs = []

_digits = re.compile('\d')


def contains_digits(s):
    return bool(_digits.search(s))


def make_pairs(raw_text):
    """
    Consume raw OCR text, turning each line into a pair of string values.
    """
    lines = raw_text.split('\n')
    # Remove emtpy lines
    lines = filter(None, lines)
    lines = filter(lambda x: x != ' ', lines)
    pairs = []
    for line in lines:
        words = line.strip().split(' ')
        key = words[0]
        words = words[1:]
        for i, word in enumerate(words):
            if not contains_digits(word):
                key += ' ' + word
            else:
                words = words[i:]
                break

        pairs.append((key, (' ').join(words)))

    return pairs


def match_bipartite(pairs, keywords):
    """
    Uses the Munkres bipartite matching algorithm to find the best
    matching between the OCR pairs and label keywords.

    Returns (keyword, (OCR key, OCR value))
    """
    pairs = list(pairs)
    keywords = list(keywords)

    distances = np.zeros((len(keywords), len(pairs)), dtype=np.int32).tolist()

    for i, key in enumerate(keywords):
        for j, pair in enumerate(pairs):
            distances[i][j] = distance(pair[0], key)

    m = Munkres()
    # Copy distance matrix to preserve distances
    indices = m.compute(distances.copy())

    key_pairs = []
    for i, j in indices:
        keyword = keywords[i]
        # Skip if half of the characters are wrong.
        if distances[i][j] <= len(keyword)/2:
            key_pairs.append((keyword, pairs[j][1]))

    return key_pairs


def keyword_pairs(pairs):
    """
    Take a list of pairs and return a list of pairs,
    with first values having the appropriate keyword.
    (keyword, stuff)
    """

    keywords = Keywords.label.values()

    return match_bipartite(pairs, keywords)


def split_percentages(key_pairs):
    """
    Attempt to intelligently split pairs into 3-tuples.
    (keyword, stuff) -> (keyword, value, percent)
    """
    def calories_tuple(pair):
        return (pair[0], pair[1].split(' ')[0], None)

    def percent_tuple(pair):
        right = pair[1].split(' ')
        amount = right[0]
        if amount[-1] == '9':
            amount = amount[:-1] + 'g'

        pct = (' ').join(right[1:])
        return (pair[0], amount, pct)

    tuples = []
    for key_pair in key_pairs:
        key, right = key_pair
        try:
            if key == Keywords.label.calories:
                tuples.append(calories_tuple(key_pair))
            else:
                tuples.append(percent_tuple(key_pair))
        except IndexError:
            tuples.append((key_pair[0], key_pair[1], None))

    return tuples


def post_process(raw_text, demo=False):
    """
    Consume OCR text, producing a Label object with
    the appropriate information.
    """
    all_pairs = make_pairs(raw_text)
    if all_pairs is False:
        return False
    key_pairs = keyword_pairs(all_pairs)
    if key_pairs is False:
        return False
    key_tuples = split_percentages(key_pairs)
    key_map = dict((a, (b, c)) for a, b, c, in key_tuples)
    return Label(keyword_map=key_map)
