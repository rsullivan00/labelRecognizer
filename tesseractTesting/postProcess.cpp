#include <string>
#include <vector>
#include <map>
#include <utility>

using namespace std;

void postProcess(vector<string> &outputs) {
    vector<string> keywords("Calories", "Total Fat", "Protein", "Total Carbohydrate");
    vector<pair<string, string> > pairs;
    for (auto &output: outputs) {
        vector<string> wordList = split(output, ' ');
        string key = wordList[0];
        /* Add words without digits to key. */
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

    /* Now see which key is closest to the keywords. */
    for (auto &keyword: keywords) {
    }
}
