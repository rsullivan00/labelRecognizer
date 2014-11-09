#include<iostream>
#include<fstream>
#include<string>

int main(int argc, char** argv){

	std::string line;

	int tessCount = 0;
	int controlCount = 0;
	int matchCount = 0;

	int tessCharacters[94];
	int controlCharacters[94];
	double matchCharacters[94];

	for(int j = 0; j < 94; j++){

		tessCharacters[j] = 0;
		controlCharacters[j] = 0;
		matchCharacters[j] = 0;
	}

	if(argc != 3){

		std::cout << "Incorrect number of arguments...Should be two text files" << std::endl;

		return -1;
	}

	std::ifstream tessFile (argv[1], std::ios::in);

	if(tessFile.is_open()){

		while(getline(tessFile, line)){

			for(unsigned int i = 0; i < line.length(); i++){

				if(line[i] > 32 && line[i] < 127){

					tessCharacters[(line[i] - 33)]++;

					tessCount++;
				}
			}
		}
	}
	else{

		std::cout << "Unable to open Tesseract text file" << std::endl;

		return -1;
	}

	tessFile.close();

	std::ifstream controlFile (argv[2], std::ios::in);

	if(controlFile.is_open()){

		while(getline(controlFile, line)){

			for(unsigned int k = 0; k < line.length(); k++){

				if(line[k] > 32 && line[k] < 127){

					controlCharacters[(line[k] - 33)]++;

					controlCount++;
				}
			}
		}
	}
	else{

		std::cout << "Unable to open Control text file" << std::endl;

		return -1;
	}

	controlFile.close();

	std::cout << "Number of characters in Tesseract file: " << tessCount << std::endl;
	std::cout << "Number of characters in Control file: " << controlCount << std::endl;	

	for(unsigned int i = 0; i < 94; i++){

		std::cout << "Number of " << ((char) (i + 33)) << "'s in Tesseract file: " << tessCharacters[i] << std::endl;
		std::cout << "Number of " << ((char) (i + 33)) << "'s in Control file: " << controlCharacters[i] << std::endl;
		std::cout << std::endl;

		if(controlCharacters[i] != 0){

			matchCharacters[i] = 100 * ((double) tessCharacters[i] / (double) controlCharacters[i]);
		}
		else if(tessCharacters[i] == 0){

			matchCharacters[i] = -1;
		}
		else{

			matchCharacters[i] = -2;
		}
		

		if(tessCharacters[i] >= controlCharacters[i]){

			matchCount += controlCharacters[i];
		}
		else{

			matchCount += tessCharacters[i];
		}
	}

	std::cout << "--------------" << std::endl;

	for(unsigned int i = 0; i < 94; i++){

		if(matchCharacters[i] == -1){

			std::cout << "There are " << controlCharacters[i] << " " << ((char) (i + 33)) << "'s in the Control file, Tesseract correctly identified " << tessCharacters[i] << " of them." << std::endl;
		}
		else if(matchCharacters[i] == -2){

			std::cout << "There are " << controlCharacters[i] << " " << ((char) (i + 33)) << "'s in the Control file, Tesseract incorrectly indentified " << tessCharacters[i] << " of them." << std:: endl;
		}
		else{
  
			std::cout << "Tesseract detected " << matchCharacters[i] << ((char) 37) << " of the " << ((char) (i + 33)) << "'s in the control file." << std::endl;
		}
	}

	std::cout << std::endl << "Tesseract identified " << matchCount << " of the " << controlCount << " characters in the Control file and " << tessCount - matchCount << " addtional characters" << std::endl;

	return 0;
}
