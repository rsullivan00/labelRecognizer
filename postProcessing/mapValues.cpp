#include <algorithm>
#include <map>
#include <set>
#include <climits>
#include <iostream>
#include <fstream>
#include "../accuracyAndPrecisionTesting/levenshteinDistance.cpp"


using namespace std;

map<string, int> mapReadValues(set<string> oCRWords, set<string> keywords) {
    map<string, int> mappedValues;
    for (auto &keyword: keywords) {
        /* Find closest match to keyword */
        int min = INT_MAX;
        string minString;
        for (auto &word: oCRWords) {
            int distance = levenshteinDistance(word, keyword);
            if (distance < min) {
                min = distance;
                minString = word;
            }
        }

        oCRWords.erase(minString);
        cout << keyword << "\t" << minString << endl;;
    }

    return mappedValues;
}

int main() {
    string keywordList[] = {"Calories", "Total Fats", "Carbohydrates", "Protein"};

    set<string> keywords(keywordList, keywordList + 4);    
    set<string> oCRWords;
    ifstream inFile("../tesseractTesting/outputs/bw/1.txt");

    string word;
    while (inFile >> word) {
        oCRWords.insert(word);
    }

    mapReadValues(oCRWords, keywords); 

    return 0;
}
