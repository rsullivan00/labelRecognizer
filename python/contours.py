import cv2
import sys
import os
import math
import random
import numpy as np
from categories import easy_labels

def contour(imagepath, show=True):
    print(imagepath)
    if not os.path.exists(imagepath):
        print("Could not find %s" % imagepath)
        return None

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
        return

    contour = cv2.approxPolyDP(label_contours[0], 50, True)
    #contour = label_contours[0]
    rect = cv2.minAreaRect(contour)
    center = rect[0]
    size = (int(rect[1][0]), int(rect[1][1]))
    angle = rect[2]

    pts = cv2.boxPoints(rect)
    print('Contour: %s, \nrect: %s' % ([x for [x] in contour], pts))
    M = cv2.getPerspectiveTransform(np.array([x for [x] in contour], dtype='Float32'), pts)
    contour = cv2.warpPerspective(thresh, M, size)

    if abs(angle) > 45:
        print('Angle change %s' % str(angle))
        angle = angle % 45

    print('Angle: %s' % str(angle))

#    map_matrix_cv = cv2.fromarray([[np.cos(angle), -np.sin(angle), center[0]], 
#        [np.sin(angle), np.cos(angle), center[1]]])

# Get four corners of contour
# Then use warpPerspective function
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    thresh = cv2.warpAffine(thresh, rotation_matrix, dsize=(len(thresh), len(thresh[0])), dst=thresh)
    pix = cv2.getRectSubPix(thresh, size, center)
    print(len(contour))

    # Draw contour on original image
    if show:
        cv2.medianBlur(pix, 3)
        edges = cv2.Canny(pix,70,200,5)
        cv2.drawContours(im, [contour], -1, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), -5)
        cv2.namedWindow('contour', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('contour', 800, 800)
        cv2.namedWindow('edge', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('edge', 800, 800)
        cv2.imshow('contour', im)
        cv2.imshow('edge', edges)
        cv2.waitKey()


def processAllImages(dirpath):
    labels = easy_labels()
    for label in labels:
        print(label.name)
        contour(os.path.join(dirpath, label.name + '.jpg'), show=True)

if len(sys.argv) > 1:
    contour(sys.argv[1])
else:
    processAllImages('../labels/')
