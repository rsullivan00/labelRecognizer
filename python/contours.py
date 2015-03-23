import cv2
import sys
import os
import math
import random
import numpy as np
from categories import easy_labels

# Can be used to reorder 4 corners into clockwise order
# (starting with the top-left corner)
def corners(cnt):
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

def contour(imagepath, show=True):
    print(imagepath)
    if not os.path.exists(imagepath):
        print("Could not find %s" % imagepath)
        return False

    im = cv2.imread(imagepath)
    im_x = len(im)
    im_y = len(im[0])
    im_size = im_x * im_y
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
#    imgray = cv2.medianBlur(imgray,7)
    ret,thresh = cv2.threshold(imgray,127,255,0)
#    thresh = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,0)
    image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    # Filter based on contour size
    large_contours = []
    contour_area_thresh = im_size/8
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > contour_area_thresh:
            large_contours.append(cnt)

    print('%d large contours found' % len(large_contours))

    # Now filter based on the location of the contour's centroid
    possible_label_contours = []
    cx_im = im_x/2
    cy_im = im_y/2
    centroid_distance_thresh = im_size/2000
    print('Euclidean thresh: %d' % centroid_distance_thresh)
    for cnt in large_contours:
        # Moments of the contour
        M = cv2.moments(cnt)

        # Find the centroid
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        # Euclidean distance from center
        dist = math.sqrt((cx-im_x)**2 + (cy-im_y)**2)

        if dist < centroid_distance_thresh:
            possible_label_contours.append(cnt)
            print('Euclidean distance: %d' % dist)

    removed = len(large_contours) - len(possible_label_contours)
    if removed > 0:
        print('%d contours removed for location' % removed)

    label_contours = []
    # Find contour in the middle of the image
    for cnt in possible_label_contours:
        # Check if contour contains the center of the image
        if cv2.pointPolygonTest(cnt, (cx_im, cy_im), False) > 0:
            label_contours.append(cnt)

    removed = len(possible_label_contours) - len(label_contours)
    if removed > 0:
        print('%d contours removed after center check' % removed)

    print('%d contours found' % len(label_contours))

    if len(label_contours) == 0:
        return False

    contour = label_contours[0]
    contour_corners = cv2.approxPolyDP(contour, 50, True)
    if len(contour_corners) != 4:
        print("Contour not rectangular, but of size %s" % len(contour_corners))
        return False

    # Array corners in clockwise order
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
    label_im = cv2.Canny(label_im,70,200,5)
    # Draw contour on original image
    cv2.drawContours(im, [contour], -1, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), -5)
    #contour_corners.reshape((-1,1,2))
    #print(contour_corners)
    #cv2.polylines(label_im, [contour_corners], True, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))

    if show:
        cv2.namedWindow('contour', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('contour', 800, 800)
        cv2.namedWindow('label_im', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('label_im', 800, 800)
        cv2.imshow('contour', im)
        cv2.imshow('label_im', label_im)
        cv2.waitKey()

    return label_im

def processAllImages(dirpath):
    labels = easy_labels()
    for label in labels:
        print(label.name)
        contour(os.path.join(dirpath, label.name + '.jpg'), show=True)

if len(sys.argv) > 1:
    contour(sys.argv[1])
else:
    processAllImages('../labels/')
