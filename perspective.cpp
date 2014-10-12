#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>

void edgeMap(cv::Mat bw, cv::Mat edgeImage) {
    /* Get the edge map using the canny operator */
    cv::Canny(bw, bw, 100, 100, 3, true);
    //cv::Canny(bw, bw, 50, 200, 3);
}

std::vector<cv::Vec4i>detectLines(cv::Mat bw) {
    std::vector<cv::Vec4i> lines;
    //cv::HoughLinesP(bw, lines, 1, CV_PI/180, 70, 30, 10);
    cv::HoughLinesP(bw, lines, 1, CV_PI/180, 150, 90, 20);
    return lines;
}

std::vector<cv::Vec4i>detectOuterLines(cv::Mat bw) {
    std::vector<cv::Vec4i> lines;
    cv::HoughLinesP(bw, lines, 1, CV_PI/180, 70, 100, 10);
    return lines;
}

cv::Point2f computeIntersect(cv::Vec4i a, cv::Vec4i b)
{
    int x1 = a[0], y1 = a[1], x2 = a[2], y2 = a[3];
    int x3 = b[0], y3 = b[1], x4 = b[2], y4 = b[3];

    if (float d = ((float)(x1-x2) * (y3-y4)) - ((y1-y2) * (x3-x4)))
    {
        cv::Point2f pt;
        pt.x = ((x1*y2 - y1*x2) * (x3-x4) - (x1-x2) * (x3*y4 - y3*x4)) / d;
        pt.y = ((x1*y2 - y1*x2) * (y3-y4) - (y1-y2) * (x3*y4 - y3*x4)) / d;
        return pt;
    }
    else
        return cv::Point2f(-1, -1);
}

void sortCorners(std::vector<cv::Point2f>& corners, cv::Point2f center)
{
    std::vector<cv::Point2f> top, bot;

    for (int i = 0; i < corners.size(); i++)
    {
        if (corners[i].y < center.y)
            top.push_back(corners[i]);
        else
            bot.push_back(corners[i]);
    }

    cv::Point2f tl = top[0].x > top[1].x ? top[1] : top[0];
    cv::Point2f tr = top[0].x > top[1].x ? top[0] : top[1];
    cv::Point2f bl = bot[0].x > bot[1].x ? bot[1] : bot[0];
    cv::Point2f br = bot[0].x > bot[1].x ? bot[0] : bot[1];

    corners.clear();
    corners.push_back(tl);
    corners.push_back(tr);
    corners.push_back(br);
    corners.push_back(bl);
}

void drawLines(cv::Mat image, std::vector<cv::Vec4i> lines) {
    // Draw lines
    for (int i = 0; i < lines.size(); i++) {
        cv::Vec4i v = lines[i];
        cv::line(image, cv::Point(v[0], v[1]), cv::Point(v[2], v[3]), CV_RGB(0,255,0));
    }
}

int main(int argc, char** argv) {
    if(argc != 2) {
         std::cout <<" Usage: display_bw ImageToLoadAndDisplay" << std::endl;
         return -1;
    }

    cv::Mat image = cv::imread(argv[1], CV_LOAD_IMAGE_COLOR);   // Read the file
    cv::Mat bw;   // Read the file
    cv::cvtColor(image, bw, CV_BGR2GRAY);

    /* Check for valid input */
    if(!bw.data) {
        std::cout <<  "Could not open or find the bw" << std::endl;
        return -1;
    }

    edgeMap(bw, bw);

    cv::Mat lineImage = image.clone();
    cv::Mat contourImage = bw.clone();
    std::vector<std::vector<cv::Point> > contours;
    cv::findContours(contourImage, contours, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
    cv::Mat contourLineImage = image.clone();

    std::vector<cv::Vec4i> lines = detectLines(bw);
    std::cout << lines.size() << " lines" << std::endl;

    drawLines(lineImage, lines);
    lines = detectLines(contourImage);
    drawLines(contourLineImage, lines);
    
/*
    std::vector<cv::Point2f> corners;
    for (int i = 0; i < lines.size(); i++)
    {
        for (int j = i+1; j < lines.size(); j++)
        {
            cv::Point2f pt = computeIntersect(lines[i], lines[j]);
            if (pt.x >= 0 && pt.y >= 0) {
                corners.push_back(pt);
            }
        }
    }
*/

/*
    std::vector<cv::Point2f> approx;
    cv::approxPolyDP(cv::Mat(corners), approx, 
                     cv::arcLength(cv::Mat(corners), true) * 0.02, true);

    if (approx.size() != 4)
    {
        std::cout << "The object is not quadrilateral!" << std::endl;
        //return -1;
    }

    // Get mass center
    cv::Point2f center(0,0);
    for (int i = 0; i < corners.size(); i++)
        center += corners[i];

    center *= (1. / corners.size());
    sortCorners(corners, center);
*/
//    cv::imshow("Original", image);
    cv::imshow("Edge detected bw", bw);
    cv::imshow("Lines found", lineImage);
    cv::imshow("Contours found", contourImage);
    cv::imshow("Lines found from contours", contourLineImage);

    cv::imwrite("edge.jpg", bw);
    cv::imwrite("lines.jpg", lineImage);
    cv::imwrite("contours.jpg", contourImage);

    cv::waitKey(0);                   
    return 0;
}

