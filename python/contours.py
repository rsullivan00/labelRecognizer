import cv2
import sys
import os
import math
import random

def contour(imagepath, show=True):
	im = cv2.imread(imagepath)
	im_x = len(im)
	im_y = len(im[0])
	im_size = im_x * im_y
	imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(imgray,127,255,0)
#	thresh = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,0)
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

	# Draw remaining contours on original image
	if show:
		for i in range(len(label_contours)):
			cv2.drawContours(im, label_contours, i, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), -5)
		cv2.namedWindow('contour', cv2.WINDOW_NORMAL)
		cv2.imshow('contour', im)
		cv2.waitKey()


def processAllImages(dirpath):
	for file in os.listdir(dirpath):
		print(file)
		if file.endswith(".jpg"):
			contour(os.path.join(dirpath, file), show=False)
	

#processAllImages('../labels/')
contour(sys.argv[1])
