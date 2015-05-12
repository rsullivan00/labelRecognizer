import sys
import os
import jsonpickle
from keywords import Keywords

type_keys = Keywords.spec_types
keys = Keywords.json

required = [
    keys.calories,
    keys.carbohydrates,
    keys.protein,
    keys.total_fat]


def validate_dir(json_dir):
    if not os.path.isdir(json_dir):
        print("Directory '%s' not found. " % json_dir)
        sys.exit(1)


def all_labels(json_dir="../db"):
    """
    Returns a list of all Label objects we can create
    in the given directory.
    """
    validate_dir(json_dir)
    labels = []
    for f in os.listdir(json_dir):
        try:
            json_file = open(os.path.join(json_dir, f))
            label = jsonpickle.decode(json_file.read())
        except:
            continue

        labels.append(label)

    return labels


def complete_labels(json_dir="../db"):
    """
    Returns a list of every Label object that has
    each of the 'required' attributes populated.
    """
    def complete_test(label):
        return all(label[r] is not None for r in required)

    labels = all_labels(json_dir)
    return [l for l in labels if complete_test(l)]


def easy_labels(json_dir="../db"):
    """
    Returns a list of Label objects that are not marked
    by any of the 'type_keys' specified.
    Each Label object has all required attributes populated.
    """
    def easy_test(label):
        return all([not label[st] for st in type_keys])

    labels = complete_labels(json_dir)
    return [l for l in labels if easy_test(l)]


def spec_type_labels(spec_type, json_dir="../db", exclusive=True):
    """
    Returns a list of Label objects that are marked with
    the specified special type.

    If the 'exclusive' flag is set, Labels with any other special
    type are excluded.
    """

    def spec_type_test(label, spec_type, exclusive):
        try:
            type_pass = label[spec_type]
        except AttributeError:
            return False

        if not type_pass or not exclusive:
            return type_pass

        # Must not have any other special types
        sp_ts = [st for st in type_keys if st is not spec_type]
        for sp_t in sp_ts:
            try:
                # If another special type is present, fail
                if label[sp_t]:
                    return False
            # If key is not found, infer that it is False
            except AttributeError:
                continue

        return True

    labels = complete_labels(json_dir)
    return [l for l in labels if spec_type_test(l, spec_type, exclusive)]


def standard_labels(json_dir="../db"):
    """
    Returns a list of Label objects that are marked as 'standard'.
    """
    return easy_labels(json_dir)


def skewed_labels(json_dir="../db", exclusive=True):
    """
    Returns a list of Label objects that are marked as 'skewed'.

    If the 'exclusive' flag is set, Labels with any other special
    type are excluded.
    """
    return spec_type_labels(type_keys.skewed, json_dir, exclusive)


def lighting_labels(json_dir="../db", exclusive=True):
    """
    Returns a list of Label objects that are marked as 'lighting'.

    If the 'exclusive' flag is set, Labels with any other special
    type are excluded.
    """
    return spec_type_labels(type_keys.lighting, json_dir, exclusive)


def curved_labels(json_dir="../db", exclusive=True):
    """
    Returns a list of Label objects that are marked as 'curved'.

    If the 'exclusive' flag is set, Labels with any other special
    type are excluded.
    """
    return spec_type_labels(type_keys.curved, json_dir, exclusive)


def colored_labels(json_dir="../db", exclusive=True):
    """
    Returns a list of Label objects that are marked as 'colored'.

    If the 'exclusive' flag is set, Labels with any other special
    type are excluded.
    """
    return spec_type_labels(type_keys.color, json_dir, exclusive)


def horizontal_labels(json_dir="../db", exclusive=True):
    """
    Returns a list of Label objects that are marked as 'horizontal'.

    If the 'exclusive' flag is set, Labels with any other special
    type are excluded.
    """
    return spec_type_labels(type_keys.horizontal, json_dir, exclusive)
