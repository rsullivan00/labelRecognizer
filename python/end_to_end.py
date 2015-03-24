from contours import contour
from categories import easy_labels
from text import apply_tesseract
from post_process import post_process
import cv2
import sys
import os

def process_all_easy(dirpath):
    labels = easy_labels()
    for label in labels:
        print(label.name)
        end_to_end(os.path.join(dirpath, label.name + '.jpg'))

def end_to_end(impath):
    label_im = contour(impath, show=True)
    if label_im is False:
        return False

    label_impath = impath.replace('.jpg', '_label_tmp.jpg')
    cv2.imwrite(label_impath, label_im)
    # Apply Tesseract to image
    output = apply_tesseract(label_impath)
    os.remove(label_impath)
    
    post_process(output)
    # Post process Tesseract output
    # Compare post process output to ground truth

def main():
    pass

# Run when called from command line, not import.
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.isdir(arg):
            process_all_easy(arg)
        elif os.path.isfile(arg):
            end_to_end(arg)
        else:
            print('Usage:\n\t\'python3 end_to_end.py <path>\'\n(path should be a file or directory).')
