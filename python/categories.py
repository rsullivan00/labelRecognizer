import sys
import csv
import os
import jsonpickle
from label import Label

types = ['blurry', 'wrinkled', 'shadowed', 'skewed', 'curved']
required = ['calories', 'carbohydrates', 'protein', 'total_fat']

def complete_labels(json_dir="../db"):
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

        if any([label.__dict__[r] is None for r in required]):
            complete_labels.append(label)

    return complete_labels 

def easy_labels(json_dir="../db"):
    if not os.path.isdir(json_dir):
        print("Directory '%s' not found. " % json_dir)
        sys.exit(1)

    labels = complete_labels(json_dir)
    easy_labels = []
    for label in labels:
        if all([not label.__dict__[t] for t in types]):
            easy_labels.append(label)

    return easy_labels

print(easy_labels())
