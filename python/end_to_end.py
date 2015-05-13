from contours import contour, draw_image
from categories import (
    easy_labels, skewed_labels, lighting_labels, standard_labels,
    curved_labels, colored_labels, horizontal_labels)
from text import apply_tesseract
from post_process import post_process
from keywords import Keywords
import cv2
import sys
import os
import jsonpickle
from pprint import pprint
from PIL import Image
from timeit import default_timer as timer
from subprocess import call
from attrdict import AttrDict


def test_labels(dirpath, labels=None):
    """
    Runs a complete label test on every .jpg in the specified directory.
    """
    if labels is None:
        labels = easy_labels()
    ocr_results = []
    failed = []
    for label in labels:
        impath = os.path.join(dirpath, label.name + '.jpg')
        ret = test_label(impath, label)
        if ret:
            results, ocr_label = ret
            ocr_results.append((results, label))
        else:
            print("Label %s failed" % label.name)
            failed.append(label)

    completed = [x for x in ocr_results if x]
    print('%d/%d labels processed to completion' % (
        len(completed), len(labels)))
    failed_str = ', '.join([l.name for l in failed])
    print('Failed labels: %s' % failed_str)

    total_correct = sum(len(x.correct) for x, y in completed)
    total = total_correct + sum(len(x.incorrect) for x, y in completed)
    print('%d/%d keywords correct for completed labels' % (
        total_correct, total))

    pct_rank = [(len(x.correct)/(len(x.incorrect) + len(x.correct)), y.name)
                for x, y in completed]
    pct_rank.sort(key=lambda tup: tup[0])

    pct_rank_str = ', '.join(
        ['%s: %.2f%%' % (x[1], 100*x[0]) for x in pct_rank])
    print('Labels %% correct: %s' % pct_rank_str)

    # Gather keyword accuracy data
    default_result = {'correct': 0, 'incorrect': 0}
    tuples = [(v, default_result.copy()) for v in Keywords.json.values()]
    keyword_results = AttrDict(dict(tuples))
    for k in Keywords.json:
        for result, label in ocr_results:
            if k in result.correct:
                keyword_results[k]['correct'] += 1
            else:
                keyword_results[k]['incorrect'] += 1
        print("Key: %s\n%s" % (k, keyword_results[k]))

    keywords_rank = []
    for k in Keywords.json:
        # Create accuracy ratings for each keywords
        correct = keyword_results[k]['correct']
        incorrect = keyword_results[k]['incorrect']
        accuracy = correct / (correct + incorrect)
        keywords_rank.append((k, accuracy))

    # Rank keywords by accuracy
    keywords_rank.sort(key=lambda tup: tup[1])

    pct_completed = len(completed)/len(labels)
    pct_accurate = total_correct/total
    return (pct_completed, pct_accurate, keywords_rank, pct_rank)


def test_categories(dirpath):
    std_ret = test_labels(dirpath, standard_labels())
    skew_ret = test_labels(dirpath, skewed_labels())
    light_ret = test_labels(dirpath, lighting_labels())
    curve_ret = test_labels(dirpath, curved_labels())
    horiz_ret = test_labels(dirpath, horizontal_labels())
    color_ret = test_labels(dirpath, colored_labels())

    def print_results(ret, label_type=''):
        ret_str = '%.2f%% completed, %.2f%% accurate' %\
            (ret[0]*100, ret[1]*100)
        print('%s labels: %s' % (label_type, ret_str))

    print_results(std_ret, 'Standard')
    print_results(skew_ret, 'Skewed')
    print_results(light_ret, 'Lighting')
    print_results(curve_ret, 'Curved')
    print_results(horiz_ret, 'Horizontal')
    print_results(color_ret, 'Colored')


def test_label(impath, label=None, jsonpath=None, demo=False):
    """
    Test for a label found in the given image, and compare with the
    second 'label' argument.
    If the jsonpath argument is provided, information
    from that file is used instead of the other specified arguments.
    """
    if jsonpath is not None:
        json_file = open(jsonpath)
        label = jsonpickle.decode(json_file.read())

    if label is not None:
        print('Label %s' % label.name)
    ocr_label = end_to_end(impath, show=False, demo=demo)
    if ocr_label is False:
        print('Label Error')
        return False

    print(ocr_label)
    print('')
    # Compare this label with the JSON label object
    if label is not None and ocr_label is not None:
        results = AttrDict({'correct': [], 'incorrect': []})
        for k in Keywords.json.values():
            if label[k] == ocr_label[k]:
                results.correct.append(k)
            else:
                results.incorrect.append(k)

        return (results, ocr_label)

    return ocr_label


def demo_label(impath, jsonpath='../db/demo.json',
               backup_path='./demo/demo_2.jpg'):

    # Check to make sure it worked the first time
    correct, count, label = test_label(impath, jsonpath=jsonpath, demo=True)

    # If failed, move to backup image
    if correct < count:
        impath = backup_path

    # Actually demo now
    correct, count, label = test_label(impath, jsonpath=jsonpath, demo=True)

    image_order = ["original", "gray", "blur", "hist", "thresholdm",
                   "thresholdg", "contour", "final"]
    image_paths = []
    basename = os.path.basename(impath)
    demo_dir = 'demo'
    for i, im_prefix in enumerate(image_order):
        prev_name = os.path.join(demo_dir, im_prefix + basename)
        new_name = os.path.join(demo_dir, str(i) + im_prefix + basename)
        os.rename(prev_name, new_name)
        image_paths.append(new_name)

    base = os.path.splitext(basename)[0]
    text_filenames = ["tess_" + base + ".txt", "result_" + base + ".js"]
    text_filepaths = [os.path.join(demo_dir, x) for x in text_filenames]

    # Write label object to text file
    with open(text_filepaths[-1], 'w') as result_file:
        pprint(label.__dict__, stream=result_file)

    call(['xdg-open', image_paths[0]])
    call(['xdg-open', text_filepaths[0]])
    call(['xdg-open', text_filepaths[1]])


def end_to_end(impath, show=False, demo=False):
    """
    Return a Label object from a label in the provided image.
    """

    start = timer()
#    try:
    img = Image.open(impath)
    exif_data = img._getexif()

    orientation = 1
    if exif_data is not None:
        # orientation tag is 0x0112
        o_data = exif_data[274]
        if o_data is not None:
            orientation = int(o_data)

    label_im = contour(impath, demo=demo, orientation=orientation)
    if label_im is False:
        label_im = contour(impath, invert=True, demo=demo)
        if label_im is False:
            return False

    end = timer()
    print('Pre process time: %2f' % (end-start))

    basename = os.path.basename(impath)
    label_impath = impath.replace(basename, 'tmp_' + basename)
    # label_impath = impath.lower().replace('.jpg', 'label_tmp.jpg')
    cv2.imwrite(label_impath, label_im)

    start = timer()
    # Apply Tesseract to image
    output = apply_tesseract(label_impath, demo=demo)

    end = timer()
    print('OCR time: %2f' % (end-start))
    os.remove(label_impath)

    start = timer()
    ocr_label = post_process(output, demo=demo)

    end = timer()
    print('Post process time: %2f' % (end-start))

    if show:
        draw_image(label_im, 'Transformed label: %s' % impath)

    return ocr_label


def main():
    pass

# Run when called from command line, not import.
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == 'demo':
            demo_label(sys.argv[2])
        elif arg == 'categories':
            test_categories(sys.argv[2])
        elif os.path.isdir(arg):
            test_labels(arg)
        elif os.path.isfile(arg):
            json_path = None
            if len(sys.argv) > 2:
                json_path = '../db/' + sys.argv[2] + '.json'
            ret = test_label(arg, jsonpath=json_path)
            if ret is not None:
                if len(ret) == 1:
                    label = ret
                else:
                    res, label = ret
                    print('%d/%d Correct' % (len(res.correct),
                                            (len(res.correct) +
                                                len(res.incorrect))))
        else:
            print('Usage:\n\t\'python3 end_to_end.py <path>\'\n\
                    (path should be a file or directory).')
