#include<math.h>
#include<stdio.h>
#include<stdlib.h>
#include<vector>
#include<string>
#include<opencv2/opencv.hpp>
//#include<opencv2/imgproc.hpp>
//#include<opencv2/highgui.hpp>
#include"queue.h"
#define fillRun 2

using namespace cv;

Mat src, src_gray, dst, preFill, planarImage;
Mat canvas(1936, 2592, CV_8UC1, Scalar(255));
//Mat rsdst(1936, 2592, CV_8UC1, Scalar(255));
Mat rsdst;

void boundCheck(unsigned* coordinates, MyQueue* queue, MyQueue* bqueue){

	MyNode* iterator = queue->returnHead();

	unsigned N, S, E, W;

	N = coordinates[1];
	S = coordinates[1];
	E = coordinates[0];
	W = coordinates[0];

	std::cout << "----------------" << std::endl;
	std::cout << "Start Queue: " << std::endl;

	while(iterator != NULL){

		//std::cout << iterator->getX() << "," << iterator->getY() << std::endl;
	
		if(iterator->getX() > E){

			E = iterator->getX();
		}

		if(iterator->getX() < W){

			W = iterator->getX();
		}
		
		if(iterator->getY() > N){

			N = iterator->getY();
		}

		if(iterator->getY() < S){

			S = iterator->getY();
		}

		iterator = iterator->getNext();		
	}

	std::cout << N << "," << E << "," << S << "," << W << std::endl;

	std::cout << "End Queue" << std::endl;
	std::cout << "-----------------" << std::endl;

	coordinates[0] = N;
	coordinates[1] = S;
	coordinates[2] = E;
	coordinates[3] = W;

	return;
}

int present(MyQueue* queue, unsigned xC, unsigned yC){

	//std::cout << "Running present on " << xC << "," << yC << std::endl;

	MyNode* iterator = queue->returnHead();

	while(iterator != NULL){

		//std::cout << xC << "," << yC << " " << iterator->getX() << "," << iterator->getY() << std::endl;

		if((iterator->getX() == xC) && (iterator->getY() == yC)){

			
			//std::cout << "------------------" << std::endl;

			return 1;
		}

		iterator = iterator->getNext();
	}

	//std::cout << "------------------" << std::endl;

	return 0;
}

void drawCanvas(MyQueue* queue){

	MyNode* iterator = queue->returnHead();

	while(iterator != NULL){

		canvas.at<uchar>(Point(iterator->getX(), iterator->getY())) = 0;
	
		iterator = iterator->getNext();
	}
	
	return;
}		

int main(int argc, char** argv){

	std::vector<Vec4i> lines;
	std::string coordinate;

	MyQueue Q;
	MyQueue P;
	MyQueue BorderQ;
	MyQueue borderSet;

	int doneFlag = 0;
	unsigned coords[4];
	
	Point2f inputQuad[4];
	Point2f outputQuad[4];

	Mat lambda(2, 4, CV_32FC1);

	if(argc != 2){

		printf("Improper number of arguments\n");

		return 0;
	}

	/*
	src = imread(argv[1], 1);

	cvtColor(src, src_gray, COLOR_RGB2GRAY);

	threshold(src_gray, dst, 60, 255, THRESH_BINARY);

	imwrite("grayOutput.jpg", src_gray);	
	imwrite("output.jpg", dst);

	dst.copyTo(rsdst);

	std::cout << rsdst.cols << " " << rsdst.rows << std::endl;

	for(int n = 0; n < fillRun; n++){

		for(int i = 1; i < (rsdst.cols - 2); i++){

			for(int j = 1; j < (rsdst.rows - 2); j++){

				Scalar color = rsdst.at<uchar>(Point(i, j));

				if(color.val[0] == 255){

					Scalar colorN = rsdst.at<uchar>(Point(i, (j + 1)));				
					Scalar colorS = rsdst.at<uchar>(Point(i, (j - 1)));				
					Scalar colorW = rsdst.at<uchar>(Point((i - 1), j));				
					Scalar colorE = rsdst.at<uchar>(Point((i + 1), j));

					if( ( (colorN.val[0] == 0) && (colorS.val[0] == 0) ) || ( (colorW.val[0] == 0) && (colorE.val[0] == 0) ) ){

						rsdst.at<uchar>(Point(i, j)) = 0;
					}
				}
			}
		}
	}

	imwrite("filledOutput.jpg", rsdst);

	line(rsdst, Point(0, 0), Point(0, (rsdst.rows - 1)), Scalar(0, 0, 255), 2, LINE_8);
	line(rsdst, Point(0, 0), Point((rsdst.cols - 1), 0), Scalar(0, 0, 255), 2, LINE_8);
	line(rsdst, Point(0, (rsdst.rows - 1)), Point((rsdst.cols - 1), (rsdst.rows - 1)), Scalar(0, 0, 255), 2, LINE_8);
	line(rsdst, Point((rsdst.cols - 1), 0), Point((rsdst.cols - 1), (rsdst.rows - 1)), Scalar(0, 0, 255), 2, LINE_8);

	preFill = rsdst;
	*/

	rsdst = imread(argv[1], 1);

	cvtColor(rsdst, rsdst, COLOR_RGB2GRAY);

	//adaptiveThreshold(rsdst, rsdst, 60, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY, 11, 2);
	threshold(rsdst, rsdst, 60, 255, THRESH_BINARY);
	imwrite("grayed.jpg", rsdst);

	std::vector<std::vector<Point> > contours;
	std::vector<Vec4i> hierarchy;
	
	findContours(rsdst, contours, hierarchy, RETR_TREE, CHAIN_APPROX_SIMPLE, Point(0, 0));
	
	cvtColor(rsdst, rsdst, COLOR_GRAY2BGR);

	for(int idx = 0; idx >= 0; idx = hierarchy[idx][0]){
	
		drawContours(rsdst, contours, idx, Scalar(rand() % 255, rand() % 255, rand() % 255), FILLED, 8, hierarchy);
	}

	/*
	for(int idx = 0; idx >= 0; idx = hierarchy[idx][1]){
	
		drawContours(rsdst, contours, idx, Scalar(rand() % 255, rand() % 255, rand() % 255), FILLED, 8, hierarchy);
	}*/

	//drawContours(rsdst, contours, -1, Scalar(rand() % 255, rand() % 255, rand() % 255), FILLED, 4);

	/*for(unsigned i = 0; i < contours.size(); i++){

		std::cout << 
	*/

	imwrite("finfin.jpg", rsdst);

	//int spot = 0;
	//int max = 0;

	/*
	for(unsigned i = 0; i < contours.size(); i++){

		for(unsigned j = 0; j < 4; j++){

			std::cout << contours[i][j];
		}
	}

	inputQuad[0] = Point2f(contours[0][0].x, contours[0][0].y);
	inputQuad[1] = Point2f(contours[0][1].x, contours[0][1].y);
	inputQuad[2] = Point2f(contours[0][2].x, contours[0][2].y);
	inputQuad[3] = Point2f(contours[0][3].x, contours[0][3].y);
	*/


	/*
	outputQuad[0] = Point2f(0, 0);
	outputQuad[1] = Point2f((coords[2] - coords[3]) - 1, 0);
	outputQuad[2] = Point2f((coords[2] - coords[3]) - 1, (coords[0] - coords[1]) - 1);
	outputQuad[3] = Point2f(0, (coords[0] - coords[1]) - 1);

	//imwrite("finalMark.jpg", canvas);

	lambda = Mat::zeros(canvas.rows, canvas.cols, canvas.type());
	lambda = getPerspectiveTransform(inputQuad, outputQuad);

	//warpPerspective(dst, planarImage, lambda, planarImage.size());
	warpPerspective(dst, planarImage, lambda, Size((coords[2] - coords[3]), (coords[0] - coords[1])));

	transpose(planarImage, planarImage);
	flip(planarImage, planarImage, 1);

	imwrite("finalImage.jpg", planarImage);
*/
	return 0;
}
