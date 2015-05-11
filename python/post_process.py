import re
from Levenshtein import distance
from keywords import Keywords
from label import Label
import numpy as np
from munkres import Munkres

pairs = []

_digits = re.compile('\d')
_alpha = re.compile('[a-zA-Z]')


def contains_digits(s):
    return bool(_digits.search(s))


def contains_alpha(s):
    return bool(_alpha.search(s))


def make_pairs(raw_text):
    """
    Consume raw OCR text, turning each line into a pair of string values.
    """
    lines = raw_text.split('\n')
    # Remove emtpy lines
    lines = filter(None, lines)
    lines = filter(lambda x: x != ' ', lines)
    pairs = []
    i = 0
    for line in lines:
        def check_line(line):
            return len(line) > 5\
                and contains_digits(line)\
                and contains_alpha(line)

        if not check_line(line):
            continue

        words = line.strip().split(' ')
        key = words[0]
        words = words[1:]
        for j, word in enumerate(words):
            if not contains_digits(word):
                key += ' ' + word
            else:
                words = words[j:]
                break

        pairs.append((key, (' ').join(words), i))
        i += 1

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
    # (i, j), for optimal mapping from keywords[i] -> ocr_tuples[j].
    for i, j in indices:
        keyword = keywords[i]
        # Skip if half of the characters are wrong.
        if distances[i][j] <= len(keyword)/2:
            key_pairs.append((keyword, pairs[j][1], pairs[j][2]))

    return key_pairs


def check_keyword_ordering(keyword_pairs):
    # Sort keyword_tuples by line number
    # Compare against ordering
    key_lines = len(Keywords.label.values())
    try:
        start_line = [kp[2] for kp in keyword_pairs
                      if kp[0] is Keywords.label.calories][0]
    except IndexError:
        start_line = 0

    thresh = start_line + key_lines
    wrong_indices = []
    for kp in keyword_pairs:
        if kp[2] > thresh:
            wrong_indices.append(kp[2])

    return wrong_indices


def keyword_pairs(pairs):
    """
    Take a list of pairs and return a list of pairs,
    with first values having the appropriate keyword.
    (keyword, stuff)
    """

    keywords = Keywords.label.values()
    key_pairs = match_bipartite(pairs, keywords)
    remove_indices = check_keyword_ordering(key_pairs)
    for ri in remove_indices:
        for pair in pairs:
            if pair[2] is ri:
                pairs.remove(pair)

    if len(remove_indices) > 0:
        return keyword_pairs(pairs)

    return key_pairs


def split_percentages(key_pairs):
    """
    Attempt to intelligently split pairs into 3-tuples.
    (keyword, stuff) -> (keyword, value, percent)
    """
    def calories_tuple(pair):
        return (pair[0], pair[1].split(' ')[0], None, pair[2])

    def percent_tuple(pair):
        right = pair[1].split(' ')
        amount = right[0]
        if amount[-1] == '9':
            amount = amount[:-1] + 'g'

        pct = (' ').join(right[1:])
        return (pair[0], amount, pct, pair[2])

    tuples = []
    for key_pair in key_pairs:
        key, right, line = key_pair
        try:
            if key == Keywords.label.calories:
                tuples.append(calories_tuple(key_pair))
            else:
                tuples.append(percent_tuple(key_pair))
        except IndexError:
            tuples.append((key_pair[0], key_pair[1], None, key_pair[2]))

    return tuples


def remove_bad_pairs(pairs):
    keywords = Keywords.label.values()

    good_pairs = []

    for pair in pairs:
        bad = True
        for key in keywords:
            thresh = len(key) - 2
            dist = distance(key, pair[0])
            if dist <= thresh:
                bad = False
                break

        if not bad:
            good_pairs.append(pair)

    return good_pairs


def post_process(raw_text, demo=False):
    """
    Consume OCR text, producing a Label object with
    the appropriate information.
    """
    all_pairs = make_pairs(raw_text)
    if all_pairs is False:
        return False
    good_pairs = remove_bad_pairs(all_pairs)
    key_pairs = keyword_pairs(good_pairs)
    key_tuples = split_percentages(key_pairs)
    # Don't use percentages or line numbers for now
    key_map = dict((a, b) for a, b, c, d in key_tuples)
    return Label(keyword_map=key_map)
