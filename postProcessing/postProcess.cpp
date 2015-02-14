#include <string>
#include <vector>
#include <map>
#include <utility> /* std::pair */
#include <iostream>
#include <climits> /* INT_MAX */

#include "../helpers/split.cpp"
#include "../helpers/levenshteinDistance.cpp"

using namespace std;

void postProcess(vector<string> &outputs) {
    vector<string> keywords {"Calories", "Total Fat", "Protein", "Total Carbohydrate"};
    vector<pair<string, string> > pairs;
    for (auto &output: outputs) {
        vector<string> wordList = split(output, ' ');
        string key = wordList[0];
        /* Add words without digits to the key. */
        for (auto &word: wordList) {
            bool digit = false;
            for (auto &c: word) {
                if (isdigit(c)) {
                    digit = true;
                    break;
                }
            }
            if (digit)
                break;

            key += " " + word;
        }

        string lastWord = wordList.back();

        if (lastWord.back() == '%') {
            wordList.pop_back();
            lastWord = wordList.back();
        }

        if (lastWord.back() == 'g') {
            lastWord.pop_back();
            if (lastWord.back() == 'm')
                lastWord.pop_back();
        } else if (lastWord.back() == '9') {
            lastWord.pop_back();
        }

        pairs.push_back(make_pair(key, lastWord));
        cout << key << '\t' << lastWord << endl;
    }

    map<string, string> map;

    /* Now see which key is closest to the keywords. */
    for (auto &keyword: keywords) {
        unsigned minIndex=0, minDistance=INT_MAX;
        for (unsigned i = 0; i < pairs.size(); i++) {
            unsigned distance = levenshteinDistance(keyword, get<0>(pairs[i]));
            if (distance < minDistance) {
                minIndex = i;
                minDistance = distance;
            }
        }

        map.insert(make_pair(keyword, get<1>(pairs[minIndex])));
        pairs.erase(pairs.begin() + minIndex);
    }

    cout << "Mapped keywords and strings:" << endl;
    for(auto it = map.cbegin(); it != map.cend(); ++it) {
        cout << it->first << " " << it->second << endl;
    }
}
