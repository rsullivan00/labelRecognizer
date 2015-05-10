import cv2
import sys
import os
import math
import random
import numpy as np
from categories import easy_labels


def get_random_color():
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )


def corners(cnt):
    """
    Reorders 4 corners into clockwise order.
    (starting with the top-left corner)
    """
    # Axis to look at depends on the number of dimensions of contour
    a = len(cnt.shape)-1

    rect = np.zeros(cnt.shape, dtype=cnt.dtype)

    s = np.sum(cnt, axis=a)
    rect[0] = cnt[np.argmin(s)]
    rect[2] = cnt[np.argmax(s)]

    diff = np.diff(cnt, axis=a)
    rect[1] = cnt[np.argmin(diff)]
    rect[3] = cnt[np.argmax(diff)]

    return rect


def filter_contours_size(contours, size_thresh):
    """
    Filters list of contours to contours that are at least
    the size of the threshold passed (size is pixel area).
    """
    filtered_contours = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > size_thresh:
            filtered_contours.append(cnt)

    print('%d/%d large contours found' % (
        len(filtered_contours), len(contours)))
    return filtered_contours


def filter_contours_centroid(contours, distance_thresh, centroid):
    """
    Calculate Euclidean distances of contour centroids,
    only keeping contours with distances less than the
    second passed parameter.
    """
    filtered_contours = []
    cx_im, cy_im = centroid
    for cnt in contours:
        # Moments of the contour
        M = cv2.moments(cnt)

        # Find the centroid
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        # Euclidean distance from center
        dist = math.sqrt((cx - cx_im)**2 + (cy - cy_im)**2)

        if dist < distance_thresh:
            filtered_contours.append(cnt)

    print('%d/%d centroid contours found' % (
        len(filtered_contours), len(contours)))
    return filtered_contours


def filter_contours_center(contours, centroid):
    """
    Eliminate all contours that do not contain the center of the image.
    """
    filtered_contours = []
    # Find contour in the middle of the image
    for cnt in contours:
        # Check if contour contains the center of the image
        if cv2.pointPolygonTest(cnt, centroid, False) > 0:
            filtered_contours.append(cnt)

    print('%d/%d center contours found' % (
        len(filtered_contours), len(contours)))
    return filtered_contours


def draw_image(image, name):
    """
    Draws the Mat image on a frame with name 'name,
    waits for a keypress, then closes the window.'
    """
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.startWindowThread()
    cv2.resizeWindow(name, 1500, 2300)
    cv2.imshow(name, image)
    cv2.waitKey()
    cv2.destroyWindow(name)


def invert_color(image):
    inverted = 255 - image
    return inverted


# Most images seem to be approximately 5,000,000 pixels large.
def downscale_im(im, threshold=2000000):
    """
    Recursively resize image until its size is less than the provided
    threshold.

    Returns the resized image.
    """
    im_x = len(im[0])
    im_y = len(im)
    im_size = im_x * im_y
    if im_size > threshold:
        return downscale_im(cv2.resize(im, (0, 0), fx=0.5, fy=0.5))

    return im


def adaptive_threshold(image):
    return cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 101, 5
    )


def contour(imagepath, invert=False, demo=False):
    """
    Finds a label contour in the specified image.
    Returns an image with just the extracted label, or False if
    no label is found.
    """

    if not os.path.exists(imagepath):
        print("Could not find %s" % imagepath)
        return False

    fileName = os.path.basename(imagepath)

    filenames = {}
    image_types = ["gray", "blur", "thresholdg", "thresholdm",
                   "contour", "original", "hist", "final"]
    for it in image_types:
        dir_path = it.upper()
        if demo:
            dir_path = 'demo'
        filenames[it] = os.path.join(dir_path, it.lower()) + fileName

    im = cv2.imread(imagepath)
    im = downscale_im(im)
    cv2.imwrite(filenames['original'], im)
    im_x = len(im[0])
    im_y = len(im)
    im_size = im_x * im_y

    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    if invert:
        imgray = invert_color(imgray)

    imageToBeCut = imgray
    cv2.imwrite(filenames['gray'], imgray)
    imgray = cv2.medianBlur(imgray, 3)
    cv2.imwrite(filenames['blur'], imgray)
    cv2.equalizeHist(imgray, imgray)
    cv2.imwrite(filenames['hist'], imgray)

    imgray = cv2.bilateralFilter(imgray, 5, 20, 50)
    cv2.imwrite(filenames['thresholdm'], imgray)
    thresh = adaptive_threshold(imgray)

    cv2.imwrite(filenames['thresholdg'], thresh)
    image, contours, hierarchy = cv2.findContours(
        thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
    )

    # Filter based on contour size
    large_contours = filter_contours_size(contours, im_size/10)

    # Now filter based on the location of the contour's centroid
    centroid = (int(im_x/2), int(im_y/2))

#    for x, j in enumerate(large_contours):
#        name = filenames['contour'].replace('.jpg', '-' + str(x) + '.jpg')
#        cv2.drawContours(im, [j], -1, get_random_color(), -5)
#        cv2.circle(im, centroid, 20, (0, 0, 0), thickness=-1)
#        cv2.imwrite(name, im)
#        im = cv2.imread(imagepath)

    # Filter to contours containing central point
    label_contours = filter_contours_center(large_contours, centroid)

    if len(label_contours) == 0:
        return False

    name = filenames['contour']
    cv2.drawContours(im, [label_contours[0]], -1, get_random_color(), -5)
    cv2.circle(im, centroid, 20, (0, 0, 0), thickness=-1)
    cv2.imwrite(name, im)

    epsilon = 50
    label_corners = None
    label_contour = None

    # Iteratively apply approximations to try to achieve a rectangle.
    for i in range(2):
        for l_c in label_contours:
            contour_corners = cv2.approxPolyDP(l_c, epsilon, True)
            if len(contour_corners) == 4:
                label_corners = contour_corners
                label_contour = l_c
                break
        epsilon *= 2

    if label_contour is None:
        print('No rectangular contour found')
        return False

    # Arrange corners in clockwise order
    label_corners = corners(label_corners)

    # Draw contour on original image
    cv2.drawContours(im, [label_contour], -1, get_random_color(), -5)
    cv2.imwrite(filenames['contour'], im)

    # Find minimum containing (rotated) rectangle
    # to set up transformation image
    min_rect = cv2.minAreaRect(label_contour)
    size = (int(min_rect[1][0]), int(min_rect[1][1]))
    angle = min_rect[2]

    # Account for rotated images
    if abs(angle) > 45:
        angle = angle % 45
        size = (size[1], size[0])

    new_corners = corners(
        np.array(
            [[0, 0], [size[0], 0], [size[0], size[1]], [0, size[1]]],
            np.float32
        )
    )
    M = cv2.getPerspectiveTransform(
        np.array(label_corners, np.float32),
        new_corners
    )
    label_im = cv2.warpPerspective(imageToBeCut, M, dsize=size)

    thresh = adaptive_threshold(label_im)
    cv2.equalizeHist(thresh, thresh)
    cv2.imwrite(filenames['final'], thresh)
    return thresh


def process_all_easy(dirpath):
    """
    Convenience method for running the contour function on all
    jpg files in a directory.
    """
    labels = easy_labels()
    for label in labels:
        print(label.name)
        contour(os.path.join(dirpath, label.name + '.jpg'))


def main():
    pass

# Run when called from command line, not import.
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.isdir(arg):
            process_all_easy(arg)
        elif os.path.isfile(arg):
            contour(arg)
        else:
            print('Usage:\n\t\'python3 contours.py <path>\'\n\
                    (path should be a file or directory).')
