#include<stdio.h>
#include<stdlib.h>
#include<vector>
#include<string>
#include<opencv2/opencv.hpp>
#include"queue.h"

using namespace cv;

Mat src, src_gray, dst, rsdst, preFill, planarImage;
Mat canvas(1936, 2592, CV_8UC1, Scalar(255));

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

	src = imread(argv[1], 1);

	cvtColor(src, src_gray, COLOR_RGB2GRAY);

	threshold(src_gray, dst, 50, 255, THRESH_BINARY);

	imwrite("grayOutput.jpg", src_gray);	
	imwrite("output.jpg", dst);

	//rsdst = dst.clone();
	dst.copyTo(rsdst);

	std::cout << rsdst.cols << " " << rsdst.rows << std::endl;

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

	imwrite("filledOutput.jpg", rsdst);

	line(rsdst, Point(0, 0), Point(0, (rsdst.rows - 1)), Scalar(0, 0, 255), 2, LINE_8);
	line(rsdst, Point(0, 0), Point((rsdst.cols - 1), 0), Scalar(0, 0, 255), 2, LINE_8);
	line(rsdst, Point(0, (rsdst.rows - 1)), Point((rsdst.cols - 1), (rsdst.rows - 1)), Scalar(0, 0, 255), 2, LINE_8);
	line(rsdst, Point((rsdst.cols - 1), 0), Point((rsdst.cols - 1), (rsdst.rows - 1)), Scalar(0, 0, 255), 2, LINE_8);

	preFill = rsdst;

	unsigned xStart = (unsigned) (rsdst.cols / 2);
	unsigned yStart = (unsigned) (rsdst.rows / 2);

	Scalar start = rsdst.at<uchar>(Point(xStart, yStart));

	while(!doneFlag){

		if(start.val[0] == 255){

			doneFlag = 1;
		}
		else{

			start = rsdst.at<uchar>(Point(++xStart, yStart));
		}
	}

	std::cout << xStart << " " << yStart << std::endl;

	doneFlag = 0; 		

	Q.pushNode(xStart, yStart);

	while(Q.returnHead() != NULL){

		unsigned xCoor = Q.returnHead()->getX();
		unsigned yCoor = Q.returnHead()->getY();

		Scalar center = rsdst.at<uchar>(Point(xCoor, yCoor));

		Scalar NW = rsdst.at<uchar>(Point((xCoor - 1), (yCoor + 1)));
		Scalar N = rsdst.at<uchar>(Point(xCoor, (yCoor + 1)));
		Scalar NE = rsdst.at<uchar>(Point((xCoor + 1), (yCoor + 1)));
		Scalar E = rsdst.at<uchar>(Point((xCoor + 1), yCoor));
		Scalar SE = rsdst.at<uchar>(Point((xCoor + 1), (yCoor - 1)));
		Scalar S = rsdst.at<uchar>(Point(xCoor, (yCoor - 1)));
		Scalar SW = rsdst.at<uchar>(Point((xCoor - 1), (yCoor - 1)));
		Scalar W = rsdst.at<uchar>(Point((xCoor - 1), yCoor));

		if(center.val[0] == 0){

			std::cout << "Error" << std::endl;
		}
		else{

			if((NW.val[0] == 255) && (!present(&Q, (xCoor - 1), (yCoor + 1)))){

				Q.pushNode((xCoor - 1), (yCoor + 1));
			}


			if((N.val[0] == 255) && (!present(&Q, xCoor, (yCoor + 1)))){

				Q.pushNode(xCoor, (yCoor + 1));
			}


			if((NE.val[0] == 255) && (!present(&Q, (xCoor + 1), (yCoor + 1)))){

				Q.pushNode((xCoor + 1), (yCoor + 1));
			}


			if((E.val[0] == 255) && (!present(&Q, (xCoor + 1), yCoor))){

				Q.pushNode((xCoor + 1), yCoor);
			}

			if((SE.val[0] == 255) && (!present(&Q, (xCoor + 1), (yCoor - 1)))){

				Q.pushNode((xCoor + 1), (yCoor - 1));
			}

			if((S.val[0] == 255) && (!present(&Q, xCoor, (yCoor - 1)))){

				Q.pushNode(xCoor, (yCoor - 1));
			}

			if((SW.val[0] == 255) && (!present(&Q, (xCoor - 1), (yCoor - 1)))){

				Q.pushNode((xCoor - 1), (yCoor - 1));
			}

			if((W.val[0] == 255) && (!present(&Q, (xCoor - 1), yCoor))){

				Q.pushNode((xCoor - 1), yCoor);
			}
		}

		rsdst.at<uchar>(Point(xCoor, yCoor)) = 0;

		P.pushNode(xCoor, yCoor);
		Q.popNode();
	}	

	imwrite("final.jpg", rsdst);

	for(int i = 0; i < 4; i += 2){

		coords[i] = xStart;
		coords[(i + 1)] = yStart;
	}

	boundCheck(coords, &P, &BorderQ);

	std::cout << coords[0] << ", " << coords[1] << ", " << coords[2] << ", " << coords[3] << std::endl;

	std::cout << "Height: " << (unsigned) rsdst.rows << ", Width: " << (unsigned) rsdst.cols << std::endl;

	//Mat cropped(rsdst, Rect(coords[3], coords[1], (coords[2] - coords[3]), (coords[0] - coords[1]))); 

	drawCanvas(&P);

	imwrite("clearOutside.jpg", canvas);

	cvtColor(canvas, canvas, COLOR_GRAY2BGR);

	int startScan = 1;
	Scalar ccolor = canvas.at<Vec3b>(Point(0, 0));

	while(!doneFlag && startScan < canvas.rows){

		for(int i = 0; i <= startScan; i++){

			ccolor = canvas.at<Vec3b>(Point((startScan - i), i));	

			if(ccolor[0] == 0 && ccolor[1] == 0 && ccolor[2] == 0){

				std::cout << "Found a corner! (Sort of) " << (startScan - i) << ", " << i << std::endl;

				canvas.at<Vec3b>(Point((startScan - i), i))[0] = 0;
				canvas.at<Vec3b>(Point((startScan - i), i))[1] = 0;
				canvas.at<Vec3b>(Point((startScan - i), i))[2] = 255;

				inputQuad[0] = Point2f((startScan - i), i);

				doneFlag = 1;
				break;
			}
		}

		startScan++;
	}

	doneFlag = 0;
	startScan = 0;
	
	while(!doneFlag){

		for(int i = 0; i <= startScan; i++){

			ccolor = canvas.at<Vec3b>(Point((startScan - i), (canvas.rows - i - 1)));	

			if(ccolor[0] == 0 && ccolor[1] == 0 && ccolor[2] == 0){

				std::cout << "Found a corner! (Sort of) " << (startScan - i) << ", " << (canvas.rows - i - 1) << std::endl;

				canvas.at<Vec3b>(Point((startScan - i), (canvas.rows - i - 1)))[0] = 0;
				canvas.at<Vec3b>(Point((startScan - i), (canvas.rows - i - 1)))[1] = 0;
				canvas.at<Vec3b>(Point((startScan - i), (canvas.rows - i - 1)))[2] = 255;

				inputQuad[3] = Point2f((startScan - i), (canvas.rows - i - 1));

				doneFlag = 1;
				break;
			}
		}

		startScan++;
	}

	doneFlag = 0;
	startScan = 0;
	
	while(!doneFlag){

		for(int i = 0; i <= startScan; i++){

			ccolor = canvas.at<Vec3b>(Point((canvas.cols - (startScan - i) - 1),  i));	

			if(ccolor[0] == 0 && ccolor[1] == 0 && ccolor[2] == 0){

				std::cout << "Found a corner! (Sort of) " << (canvas.cols - (startScan - i) - 1) << ", " << i << std::endl;

				canvas.at<Vec3b>(Point((canvas.cols - (startScan - i) - 1), i))[0] = 0;
				canvas.at<Vec3b>(Point((canvas.cols - (startScan - i) - 1), i))[1] = 0;
				canvas.at<Vec3b>(Point((canvas.cols - (startScan - i) - 1), i))[2] = 255;

				inputQuad[1] = Point2f((canvas.cols - (startScan - i) - 1), i);

				doneFlag = 1;
				break;
			}
		}

		startScan++;
	}

	doneFlag = 0;
	startScan = 0;
	
	while(!doneFlag){

		for(int i = 0; i <= startScan; i++){

			ccolor = canvas.at<Vec3b>(Point((canvas.cols - (startScan - i) - 1), (canvas.rows - i - 1)));	

			if(ccolor[0] == 0 && ccolor[1] == 0 && ccolor[2] == 0){

				std::cout << "Found a corner! (Sort of) " << (canvas.cols - (startScan - i) - 1) << ", " << (canvas.rows - i - 1) << std::endl;

				canvas.at<Vec3b>(Point((canvas.cols - (startScan - i) - 1), (canvas.rows - i - 1)))[0] = 0;
				canvas.at<Vec3b>(Point((canvas.cols - (startScan - i) - 1), (canvas.rows - i - 1)))[1] = 0;
				canvas.at<Vec3b>(Point((canvas.cols - (startScan - i) - 1), (canvas.rows - i - 1)))[2] = 255;

				inputQuad[2] = Point2f((canvas.cols - (startScan - i) - 1), (canvas.rows - i - 1));

				doneFlag = 1;
				break;
			}
		}

		startScan++;
	}
	
	outputQuad[0] = Point2f(0, 0);
	outputQuad[1] = Point2f((coords[2] - coords[3]) - 1, 0);
	outputQuad[2] = Point2f((coords[2] - coords[3]) - 1, (coords[0] - coords[1]) - 1);
	outputQuad[3] = Point2f(0, (coords[0] - coords[1]) - 1);

	imwrite("finalMark.jpg", canvas);

	lambda = Mat::zeros(canvas.rows, canvas.cols, canvas.type());
	lambda = getPerspectiveTransform(inputQuad, outputQuad);

	//warpPerspective(dst, planarImage, lambda, planarImage.size());
	warpPerspective(dst, planarImage, lambda, Size((coords[2] - coords[3]), (coords[0] - coords[1])));

	transpose(planarImage, planarImage);
	flip(planarImage, planarImage, 1);

	imwrite("finalImage.jpg", planarImage);

	return 0;
}
