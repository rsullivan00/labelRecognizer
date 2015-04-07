import sys
import csv
import os
import jsonpickle
from label import Label
from keywords import Keywords

special_types = ['blurry', 'wrinkled', 'shadowed', 'skewed', 'curved', 'not_bw']
required = ['calories', 'carbohydrates', 'protein', 'total_fat']

def complete_labels(json_dir="../db"):
    """ 
    Returns a list of every Label object that has 
    each of the 'required' attributes populated.
    """
    if not os.path.isdir(json_dir):
        print("Directory '%s' not found. " % json_dir)
        sys.exit(1)

    complete_labels = []
    for f in os.listdir(json_dir):
        try:
            json_file = open(os.path.join(json_dir, f))
            label = jsonpickle.decode(json_file.read())
        except:
            continue

        if all([label.__dict__[r] is not None for r in required]):
            complete_labels.append(label)

    return complete_labels 

def easy_labels(json_dir="../db"):
    """
    Returns a list of Label objects that are not marked by any of the 'special_types'
    specified. Each Label object has all required attributes populated.
    """
    if not os.path.isdir(json_dir):
        print("Directory '%s' not found. " % json_dir)
        sys.exit(1)

    labels = complete_labels(json_dir)
    easy_labels = []
    for label in labels:
        if all([not label.__dict__[t] for t in special_types]):
            easy_labels.append(label)

    return easy_labels

