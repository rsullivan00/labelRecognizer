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
    # Remove empty lines
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

        alpha = 0
        lastAlpha = False
        for i in range(len(line)):
            if(contains_alpha(line[i])):
                alpha += 1
                lastAlpha = True
            if(contains_digits(line[i]) and (alpha > 3)):
                if(lastAlpha):
                    line = line[0:(i - 1)] + ' ' + line[i:(len(line) - 1)]
                break

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

    Returns (keyword, OCR value, OCR line)
    """
    pairs = list(pairs)
    keywords = list(keywords)

    distances = np.zeros((len(keywords), len(pairs)), dtype=np.int32).tolist()
    for i, key in enumerate(keywords):
        for j, pair in enumerate(pairs):
            distances[i][j] = distance(pair[0], key)

#    keywords_ordered = Keywords.ordered
#    start_line = 3
#    for i, key in enumerate(keywords):
#        for j, pair in enumerate(pairs):
#            line = pair[2] - start_line
#            expected_line = keywords_ordered.index(key)
#            tol = (int(0.2 * expected_line) + 2)
#            diff = np.abs((expected_line - line)) - tol
#            diff = max(diff, 0)
#            diff = np.log(diff + 1)
#            print(diff, key, pair, expected_line)
#            distances[i][j] += diff

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
#    key_lines = len(Keywords.label.values())
#    try:
#        start_line = [kp[2] for kp in keyword_pairs
#                      if kp[0] is Keywords.label.calories][0]
#    except IndexError:
#        start_line = 0
#
#    thresh = start_line + key_lines
#    wrong_indices = []
#    for kp in keyword_pairs:
#        if kp[2] > thresh:
#            wrong_indices.append(kp[2])
#
#    return wrong_indices

    numLines = len(keyword_pairs)

    wrong_indices = []
    for kp in keyword_pairs:
        if kp[2] > numLines:
            wrong_indices.append(kp[2])

    return wrong_indices


def keyword_pairs(pairs):
    """
    Take a list of pairs and return a list of pairs,
    with first values having the appropriate keyword.
    (keyword, stuff)
    """
    i = 1
    newKeys = []
    for k in pairs:
        newKeys.append((k[0], k[1], i))
        i += 1
    #print(pairs)
    #print(newKeys)
    keywords = Keywords.label.values()
    key_pairs = match_bipartite(newKeys, keywords)
    print(key_pairs)
    print('\n\n')
    remove_indices = check_keyword_ordering(key_pairs)
    for ri in remove_indices:
        for nk in newKeys:
            if nk[2] is ri:
                newKeys.remove(nk)

    if len(remove_indices) > 0:
        key_pairs = match_bipartite(newKeys, keywords)

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
            slide = (len(pair[0]) - len(key)) + 1
            if(slide < 1):
                slide = 1
            for i in range(slide):
                thresh = len(key) / 2
                temp = pair[0]
                #print(temp[i:(len(key) - 1 + i)])
                dist = distance(key, temp[i:(len(key) - 1 + i)])
                if dist <= thresh:
                    bad = False
                    break

        if not bad:
            good_pairs.append(pair)

    return good_pairs


def clean_values(tuples, index=1):
    """
    Cleans text values in the specified index of the tuple.

    Removes all non-number characters except for '.'
    """
    clean_tuples = []
    for t in tuples:
        t_new = list(t)
        val = t_new[index]
        if val is not None:
            val = re.sub('[^mg0-9.]', '', val)
            if len(val) > 0 and val[-1] == '9':
                val = val[:-1] + 'g'
            val = re.sub('[^0-9.]', '', val)

        t_new[index] = val
        clean_tuples.append(tuple(t_new))

    return clean_tuples


def fix_garbage_sugar(pairs):
    betterPairs = []
    i = -1
    done = False

    for pair in pairs:
        slide = (len(pair[0]) - 6) + 1
        if(slide < 1):
            slide = 1
        for i in range(slide):
            temp = pair[0]
            #print(temp[i:(5 + i)])
            dist = distance(Keywords.label.sugars, temp[i:(5 + i)])
            if dist <= 2:
                i = pair[2]
                done = True
                break
        if(done):
            break

    for pair in pairs:
        name = pair[0]
        if(pair[2] == i):
            name = Keywords.label.sugars
        betterPairs.append((name, pair[1], pair[2]))

    return betterPairs


def post_process(raw_text, demo=False):
    """
    Consume OCR text, producing a Label object with
    the appropriate information.
    """
    all_pairs = make_pairs(raw_text)
    print(all_pairs)
    print('\n\n')
    if all_pairs is False:
        return False
    good_pairs = remove_bad_pairs(all_pairs)
    print(good_pairs)
    print('\n\n')
    better_pairs = fix_garbage_sugar(good_pairs)
    print(better_pairs)
    print('\n\n')
    key_pairs = keyword_pairs(better_pairs)
    print(key_pairs)
    print('\n\n')
    key_tuples = split_percentages(key_pairs)
    key_tuples = clean_values(key_tuples)
    # Don't use percentages or line numbers for now
    key_map = dict((a, b) for a, b, c, d in key_tuples)
    return Label(keyword_map=key_map)
