from contours import contour, draw_image
from categories import easy_labels
from text import apply_tesseract
from post_process import post_process
from keywords import *
import cv2
import sys
import os
import jsonpickle
from pprint import pprint
from PIL import Image
from timeit import default_timer as timer
from subprocess import call


def test_all_easy(dirpath):
    """
    Runs a complete label test on every .jpg in the specified directory.
    """
    labels = easy_labels()
    ocr_results = []
    for label in labels:
        impath = os.path.join(dirpath, label.name + '.jpg')
        try:
            correct, nkeys, ocr_label = test_label(impath, label)
            ocr_results.append((correct, nkeys))
        except TypeError:
            print("Label %s failed" % label.name)
            pass

    completed = [x for x in ocr_results if x]
    print('%d/%d labels processed to completion' % (
        len(completed), len(labels)))

    total_correct = sum(x[0] for x in completed)
    total = completed[0][1] * len(completed)
    print('%d/%d keywords correct for completed labels' % (
        total_correct, total))


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
        return False

    print(label)
    # Compare this label with the JSON label object
    if label is not None:
        correct = 0
        for k in Keywords.json:
            if label[k] == ocr_label[k]:
                correct += 1

        return (correct, len(Keywords.json), ocr_label)


def demo_label(impath, jsonpath='../db/demo.json',
               backup_path='./demo/new_1.JPG'):

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


def rotate(img, orientation):
    # Taken from http://stackoverflow.com/questions/
    # 22045882/modify-or-delete-exif-tag-orientation-in-python
    if orientation == 6:
        img = img.rotate(-90)
    elif orientation == 8:
        img = img.rotate(90)
    elif orientation == 3:
        img = img.rotate(180)
    elif orientation == 2:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation == 5:
        img = img.rotate(-90).transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation == 7:
        img = img.rotate(90).transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation == 4:
        img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)

    return img


def end_to_end(impath, show=False, demo=False):
    """
    Return a Label object from a label in the provided image.
    """

    start = timer()
#    try:
#        img = Image.open(impath)
#        exif_data = img._getexif()
#        # orientation tag is 0x0112
#        orientation = exif_data[274]
#        rotate(img, orientation)
#        img.save(impath)
#    except TypeError:
#        pass

    label_im = contour(impath, demo=demo)
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
        elif os.path.isdir(arg):
            test_all_easy(arg)
        elif os.path.isfile(arg):
            test_label(arg)
        else:
            print('Usage:\n\t\'python3 end_to_end.py <path>\'\n\
                    (path should be a file or directory).')
