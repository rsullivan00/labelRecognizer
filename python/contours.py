import cv2
import sys
import os
import math
import random
import numpy as np
from categories import easy_labels

fileNumber = 0;

def corners(cnt):
    """
    Reorders 4 corners into clockwise order.
    (starting with the top-left corner)
    """
    # Axis to look at depends on the number of dimensions of contour
    a = len(cnt.shape)-1

    rect = np.zeros(cnt.shape, dtype=cnt.dtype)

    s = np.sum(cnt, axis = a)
    rect[0] = cnt[np.argmin(s)]
    rect[2] = cnt[np.argmax(s)]

    diff = np.diff(cnt, axis = a)
    rect[1] = cnt[np.argmin(diff)]
    rect[3] = cnt[np.argmax(diff)]

    return rect

def contour_filter_size(contours, size_thresh):
    """
    Filters list of contours to contours that are at least
    the size of the threshold passed (size is pixel area).
    """
    filtered_contours = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > size_thresh:
            filtered_contours.append(cnt)

    print('%d/%d large contours found' % (len(filtered_contours), len(contours)))
    return filtered_contours

def contour_filter_centroid(contours, distance_thresh, centroid):
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

    print('%d/%d centroid contours found' % (len(filtered_contours), len(contours)))
    return filtered_contours

def contour_filter_center(contours, centroid):
    """
    Eliminate all contours that do not contain the center of the image.
    """
    filtered_contours = []
    # Find contour in the middle of the image
    for cnt in contours:
        # Check if contour contains the center of the image
        if cv2.pointPolygonTest(cnt, centroid, False) > 0:
            filtered_contours.append(cnt)

    print('%d/%d center contours found' % (len(filtered_contours), len(contours)))
    return filtered_contours

def draw_image(image, name):
    """
    Draws the Mat image on a frame with name 'name.'
    """
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, 800, 800)
    cv2.imshow(name, image)

def contour(imagepath, show=False, show_fail=False):
    """
    Finds a label contour in the specified image.
    The show flags control whether we display the results visually
    (this waits for a manual key press).
    Returns an image with just the extracted label, or False if
    no label is found.
    """
    global fileNumber

    fileNameGray = "GRAY/gray" + str(fileNumber) + ".jpg"
    fileNameBlur = "BLUR/blur" + str(fileNumber) + ".jpg"
    fileNameThresh = "THRESHOLD/thresh" + str(fileNumber) + ".jpg"
    fileNameContour = "CONTOUR/contour" + str(fileNumber) + ".jpg"

    if not os.path.exists(imagepath):
        print("Could not find %s" % imagepath)
        return False

    im = cv2.imread(imagepath)
    im_x = len(im)
    im_y = len(im[0])
    im_size = im_x * im_y
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    cv2.imwrite(fileNameGray, imgray)
    imgray = cv2.medianBlur(imgray,3)
    cv2.imwrite(fileNameBlur, imgray)
    ret,thresh = cv2.threshold(imgray,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imwrite(fileNameThresh, thresh)
#    thresh = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    image, contours, hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    fileNumber += 1

    # Filter based on contour size
    large_contours = contour_filter_size(contours, im_size/10)

    # Now filter based on the location of the contour's centroid
    centroid = (im_x/2, im_y/2)
    # Is this actually useful?
    #    possible_label_contours = contour_filter_centroid(large_contours, im_size/2000, centroid)

    # This should only return a single contour...and will supercede any other filtering. Should we only use this type of filtering?
    label_contours = contour_filter_center(large_contours, centroid)

    if len(label_contours) == 0:
        return False

    contour = label_contours[0]
    epsilon = 50
    contour_corners = cv2.approxPolyDP(contour, epsilon, True)
    # Iteratively apply approximations to try to achieve a rectangle.
    for i in range(4):
        if len(contour_corners) == 4:
            break
        epsilon *= 2 
        contour_corners = cv2.approxPolyDP(contour, epsilon, True)

    # If we did not find a rectangle, fail.
    if len(contour_corners) != 4:
        print("Contour not rectangular, but of size %s" % len(contour_corners))
        #if show_fail:
            #cv2.drawContours(thresh, [contour], -1, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), -5)
            #cv2.drawContours(im, [contour_corners], -1, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), -5)
            #draw_image(im, 'Failed: approx')
            #draw_image(thresh, 'Failed: contour')
            #cv2.waitKey()
        return False

    # Arrange corners in clockwise order
    contour_corners = corners(contour_corners)

    # Find minimum containing (rotated) rectangle and relevant info
    min_rect = cv2.minAreaRect(contour)
    center = min_rect[0]
    size = (int(min_rect[1][0]), int(min_rect[1][1]))
    angle = min_rect[2]

    # Account for rotated images
    if abs(angle) > 45:
        angle = angle % 45
        size = (size[1], size[0])

    new_corners = corners(np.array([[0,0], [size[0],0], [size[0],size[1]], [0,size[1]]], np.float32))
    M = cv2.getPerspectiveTransform(np.array(contour_corners, np.float32), new_corners)
    label_im = cv2.warpPerspective(thresh, M, dsize=size)

    # Draw contour on original image
    cv2.drawContours(im, [contour], -1, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), -5)
    cv2.imwrite(fileNameContour, im)
    #contour_corners.reshape((-1,1,2))
    #print(contour_corners)
    #cv2.polylines(label_im, [contour_corners], True, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))

    #if show:
        #draw_image(im, 'contour')
        #draw_image(label_im, 'label')
        #cv2.waitKey()

    return label_im

def process_all_easy(dirpath):
    labels = easy_labels()
    for label in labels:
        print(label.name)
        contour(os.path.join(dirpath, label.name + '.jpg'), show=True)

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
            print('Usage:\n\t\'python3 contours.py <path>\'\n(path should be a file or directory).')
