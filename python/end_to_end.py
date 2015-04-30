from contours import contour, draw_image
from categories import easy_labels
from text import apply_tesseract
from post_process import post_process
from keywords import *
import cv2
import sys
import os
import jsonpickle
from timeit import default_timer as timer

def test_all_easy(dirpath):
    """
    Runs a complete label test on every .jpg in the specified directory.
    """
    labels = easy_labels()
    ocr_results = []
    for label in labels:
        impath = os.path.join(dirpath, label.name + '.jpg')
        results = test_label(impath, label)
        ocr_results.append(results)

    completed = [x for x in ocr_results if x]
    print('%d/%d labels processed to completion' % (len(completed), len(labels)))

    total_correct = sum(x[0] for x in completed)
    total = completed[0][1] * len(completed)
    print('%d/%d keywords correct for completed labels' % (total_correct, total))


def test_label(impath, label, jsonpath=None):
    """
    Test for a label found in the given image, and compare with the
    second 'label' argument.
    If the jsonpath argument is provided, information
    from that file is used instead of the other specified arguments.
    """
    if jsonpath is not None:
        label = jsonpickle.decode(jsonpath)
    print('Label %s' % label.name)
    ocr_label = end_to_end(impath, show=False)
    if ocr_label is False:
        return False

    # Compare this label with the JSON label object
    correct = 0
    for k in Keywords.json:
        if label[k] == ocr_label[k]:
            correct += 1

    return (correct, len(Keywords.json))


def end_to_end(impath, show=False):
    """
    Return a Label object from a label in the provided image.
    """

    start = timer()
    label_im = contour(impath)
    if label_im is False:
        label_im = contour(impath, invert=True)
        if label_im is False:
            return False

    end = timer()
    print('Pre process time: %2f' % (end-start))

    label_impath = impath.replace('.jpg', '_label_tmp.jpg')
    cv2.imwrite(label_impath, label_im)

    start = timer()
    # Apply Tesseract to image
    output = apply_tesseract(label_impath)

    end = timer()
    print('OCR time: %2f' % (end-start))
    os.remove(label_impath)

    start = timer()
    ocr_label = post_process(output)
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
        if os.path.isdir(arg):
            test_all_easy(arg)
        elif os.path.isfile(arg):
            end_to_end(arg)
        else:
            print('Usage:\n\t\'python3 end_to_end.py <path>\'\n(path should be a file or directory).')
