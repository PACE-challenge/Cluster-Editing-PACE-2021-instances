#include <iostream>
#include <vector>

using namespace std;


size_t lcs(vector<char> a, vector<char> b) {
	size_t D[a.size() + 1][b.size() + 1];

	for (size_t i = 0; i <= a.size(); i++)
		for (size_t j = 0; j <= b.size(); j++)
			D[i][j] = 0;

	for (size_t i = 1; i <= a.size(); i++)
		for (size_t j = 1; j <= b.size(); j++) {
			if (a[i-1] == b[j-1])
				D[i][j] = 1 + D[i-1][j-1];
			else	D[i][j] = max(D[i-1][j], D[i][j-1]);
		}

	return D[a.size()][b.size()];
}

int main() {
	vector<vector<char>> strings;

	string line;
	// little performance boost for iostream
	std::ios::sync_with_stdio(false);
	// parse the input
	while (getline(cin, line)) {
		if (line[0] == '#' || line.size() == 0) {
			cout << line << endl;
			continue;
		}

		// for some reason "\r\n" is not handled correctly
		if (!line.empty() && line[line.size() - 1] == '\r')
			line.erase(line.size() - 1);
		vector<char> data;
		copy(line.begin(), line.end(), back_inserter(data));
		strings.push_back(data);
	}

	size_t n = strings.size();

	for (size_t i = 0; i < n; i++) {
		for (size_t j = 0; j < n; j++) {
			float similarity = lcs(strings[i], strings[j]);
			similarity /= max(strings[i].size(), strings[j].size());
			cout << similarity;
			if (j != n-1)
				cout << ", ";
		}
		cout << endl;
	}
}
