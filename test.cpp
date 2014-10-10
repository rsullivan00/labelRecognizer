#include <opencv2/objdetect/objdetect.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <iostream>
#include <stdio.h>

using namespace std;
using namespace cv;

/** Function Headers */
void detectAndDisplay( Mat image);

/** Global variables */
String label_cascade_name = "haarcascade_label.xml";
CascadeClassifier label_cascade;
string window_name = "Capture - Label detection";
RNG rng(12345);

/** @function main */
int main( int argc, const char** argv )
{
  Mat image;

  //-- 1. Load the cascades
  if( !label_cascade.load( label_cascade_name ) ){ printf("--(!)Error loading\n"); return -1; };
  //-- 2. Read the image 
  image = imread(argv[1], CV_LOAD_IMAGE_COLOR);

  //-- 3. Apply the classifier to the image
  if( !image.empty() ) { 
      detectAndDisplay( image); 
  } else { 
      printf(" Coult not open or find image"); 
  }

  return 0;
}

/* @function detectAndDisplay */
void detectAndDisplay( Mat image) {

 std::vector<Rect> labels;
 Mat image_gray;

 cvtColor( image, image_gray, CV_BGR2GRAY );
 equalizeHist( image_gray, image_gray );

 //-- Detect labels
 label_cascade.detectMultiScale(image_gray, labels, 1.1, 2, 0|CV_HAAR_SCALE_IMAGE, Size(30, 30) );

 for( size_t i = 0; i < labels.size(); i++ )
 {
   Point center( labels[i].x + labels[i].width*0.5, labels[i].y + labels[i].height*0.5 );
   ellipse( image, center, Size( labels[i].width*0.5, labels[i].height*0.5), 0, 0, 360, Scalar( 255, 0, 255 ), 4, 8, 0 );

   Mat labelROI = image_gray( labels[i] );
}

 //-- Show what you got
 namedWindow(window_name, WINDOW_AUTOSIZE);
 imshow( window_name, image);

 waitKey(0);
} 

