import re
from Levenshtein import distance
from keywords import *
from label import Label

keywords = Keywords.label
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

def keyword_pairs(pairs):
    """
    Take a list of pairs and return a list of pairs,
    with first values having the appropriate keyword.
    (keyword, stuff)
    """
    if len(pairs) < len(keywords):
        return False

    keyword_pairs = []
    for keyword in keywords:
        keyword = keywords[keyword]
        min_match = (-1, 9999)
        for i,p in enumerate(pairs):
            d = distance(keyword, p[0])
            if d < min_match[1]:
                 min_match = (i, d)

        keyword_pairs.append((keyword, pairs.pop(min_match[0])[1]))

    return keyword_pairs

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
        pct = (' ').join(right[1:])
        return (pair[0], amount, pct)

    tuples = []
    for key_pair in key_pairs:
        key, right = key_pair
        try:
            if key == keywords.calories:
                tuples.append(calories_tuple(key_pair))
            else:
                tuples.append(percent_tuple(key_pair))
        except:
            tuples.append((key_pair[0], key_pair[1], None))

    return tuples

def post_process(raw_text):
    """
    Consume OCR text, producing a Label object with
    the appropriate information.
    """
    all_pairs = make_pairs(raw_text)
    if not all_pairs:
        return False
    key_pairs = keyword_pairs(all_pairs)
    if not keyword_pairs: 
        return False
    key_tuples = split_percentages(key_pairs)
    key_map = dict((a, (b,c)) for a, b, c, in key_tuples)
    return Label(keyword_map=key_map)
