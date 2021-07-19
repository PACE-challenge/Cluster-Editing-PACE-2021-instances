#include <iostream>
#include <sstream>
#include <cassert>
#include <vector>
#include <cmath>
#include <algorithm>

using namespace std;


pair<vector<size_t>, vector<size_t>> lcs(vector<char> &a, vector<char> &b) {
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

	// backtrack to find indicies in the two strings that build the LCS
	vector<size_t> la;
	vector<size_t> lb;

	size_t i = a.size();
	size_t j = b.size();

	while (D[i][j] > 0) {
		int k = 0;
		if (a[i-1] != b[j-1]) {
			int d = 0;
			k = 1;
			if (D[i-1][j] > d)
				d = D[i-1][j];
			if (D[i][j-1] > d)
				k = 2;
		}

		if (k == 0) {
			la.push_back(i-1);
			lb.push_back(j-1);
			i--;
			j--;
		}
		if (k == 1)
			i--;
		if (k == 2)
			j--;
	}

	reverse(la.begin(), la.end());
	reverse(lb.begin(), lb.end());

	assert(D[a.size()][b.size()] == la.size());
	for (size_t i = 0; i < la.size(); i++)
		assert(a[la[i]] == b[lb[i]]);

	return make_pair(la, lb);
}

float similiarity(vector<char> &a, vector<char> &b, vector<float> &ta, vector<float> &tb) {
	auto pair = lcs(a, b);
	auto la = pair.first;
	auto lb = pair.second;
	
	if (la.size() == 0)
		return 0;

	float sim = 0;
	for (size_t i = 0; i < la.size(); i++) {
		sim += min(ta[la[i]], tb[lb[i]]) / max(ta[la[i]], tb[lb[i]]);
	}
	sim /= la.size();


	float timea = 0;
	float timeb = 0;
	float Timea = 0;
	float Timeb = 0;
	for (size_t i = 0; i < la.size(); i++) {
		timea += ta[la[i]];
		timeb += tb[lb[i]];
	}
	for (float t: ta)
		Timea += t;
	for (float t: tb)
		Timeb += t;

	float imp = sqrt(timea * timeb / (Timea * Timeb));

	return sim * imp;
}

int main() {
	vector<vector<char>> strings;
	vector<vector<float>> times;

	string line;
	// little performance boost for iostream
	std::ios::sync_with_stdio(false);
	// parse the input
	int i = 0;
	while (getline(cin, line)) {
		if (line[0] == '#' || line.size() == 0) {
			cout << line << endl;
			continue;
		}

		// for some reason "\r\n" is not handled correctly
		if (!line.empty() && line[line.size() - 1] == '\r')
			line.erase(line.size() - 1);
		if (i == 0) {
			vector<char> data;
			copy(line.begin(), line.end(), back_inserter(data));
			strings.push_back(data);
		}
		else {
			std::istringstream iss(line);
			vector<float> time;
			float t;
			while (iss >> t) {
				time.push_back(t);
			}
			times.push_back(time);
		}

		i++;
		i = i % 2;
	}

	size_t n = strings.size();

	for (size_t i = 0; i < n; i++) {
		for (size_t j = 0; j < n; j++) {
			float sim1 = similiarity(strings[i], strings[j], times[i], times[j]);
			float sim2 = similiarity(strings[j], strings[i], times[j], times[i]);
			cout << max(sim1, sim2);
			if (j != n-1)
				cout << ", ";
		}
		cout << endl;
	}
}
