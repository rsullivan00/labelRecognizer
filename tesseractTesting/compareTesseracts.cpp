#include "opencv2/text.hpp"
#include "opencv2/core/utility.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"

#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>

#include <iostream>
#include <fstream>

using namespace std;
using namespace cv;
using namespace cv::text;

int main(int argc, char* argv[])
{
    cout << endl << argv[0] << endl << endl;

    Mat img;
    if(argc>1)
        img  = imread(argv[1], IMREAD_GRAYSCALE);
    else
    {
        cout << "    Usage: " << argv[0] << " <input_image> [<gt_word1> ... <gt_wordN>]" << endl;
        return(0);
    }

    cout << "IMG_W=" << img.cols << endl;
    cout << "IMG_H=" << img.rows << endl;

    /*Text Recognition using OpenCV Tesseract integration*/
    Mat imCopy = img.clone();
    Ptr<OCRTesseract> ocr = OCRTesseract::create();
    string output;

    ofstream outFile("outputs/endToEnd.txt");

    vector<Rect>   boxes;
    vector<string> words;
    vector<float>  confidences;
    ocr->run(imCopy, output, &boxes, &words, &confidences, OCR_LEVEL_WORD);
    cout << "OCR output = \"" << output << "\" length = " << output.size() << endl;

    /* Using Tesseract directly. */
    tesseract::TessBaseAPI *api = new tesseract::TessBaseAPI();
    // Initialize tesseract-ocr with English, without specifying tessdata path
    // OEM_TESSERACT_CUBE_COMBINED is slower, but more accurate
    // remove that parameter for default configuration
    if (api->Init(NULL, "eng",  tesseract::OEM_TESSERACT_CUBE_COMBINED)) {
        fprintf(stderr, "Could not initialize tesseract.\n");
        exit(1);
    }

    // Open input image with leptonica library
    Pix *image = pixRead(argv[1]);
    api->SetImage(image);
    // Get OCR result
    char *outText = api->GetUTF8Text();
    printf("OCR output:\n%s", outText);

    // Destroy used object and release memory
    api->End();
    delete [] outText;
    pixDestroy(&image);

    waitKey(0);

    return 0;
}


