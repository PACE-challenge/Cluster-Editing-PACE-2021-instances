#include <vector>
#include <algorithm>
#include <bits/stdc++.h>
#include <stdlib.h>
#include <time.h>
#include <string>
#include <cassert>

using namespace std;

///////////////////////////////////////////////////////////////////////////
// https://www.geeksforgeeks.org/counting-inversions/

int _mergeSort(int arr[], int temp[], 
		int left, int right);
int merge(int arr[], int temp[], int left, 
		int mid, int right);

/* This function sorts the 
   input array and returns the 
   number of inversions in the array */
int mergeSort(int arr[], int array_size)
{
	int temp[array_size];
	return _mergeSort(arr, temp, 0, array_size - 1);
}

/* An auxiliary recursive function 
   that sorts the input array and 
   returns the number of inversions in the array. */
int _mergeSort(int arr[], int temp[], 
		int left, int right)
{
	int mid, inv_count = 0;
	if (right > left) {
		/* Divide the array into two parts and 
		   call _mergeSortAndCountInv() 
		   for each of the parts */
		mid = (right + left) / 2;

		/* Inversion count will be sum of 
		   inversions in left-part, right-part 
		   and number of inversions in merging */
		inv_count += _mergeSort(arr, temp, 
				left, mid);
		inv_count += _mergeSort(arr, temp, 
				mid + 1, right);

		/*Merge the two parts*/
		inv_count += merge(arr, temp, left, 
				mid + 1, right);
	}
	return inv_count;
}

/* This funt merges two sorted arrays 
   and returns inversion count in the arrays.*/
int merge(int arr[], int temp[], int left,
		int mid, int right)
{
	int i, j, k;
	int inv_count = 0;

	i = left; /* i is index for left subarray*/
	j = mid; /* j is index for right subarray*/
	k = left; /* k is index for resultant merged subarray*/
	while ((i <= mid - 1) && (j <= right)) {
		if (arr[i] <= arr[j]) {
			temp[k++] = arr[i++];
		}
		else {
			temp[k++] = arr[j++];

			/* this is tricky -- see above 
			   explanation/diagram for merge()*/
			inv_count = inv_count + (mid - i);
		}
	}

	/* Copy the remaining elements of left subarray 
	   (if there are any) to temp*/
	while (i <= mid - 1)
		temp[k++] = arr[i++];

	/* Copy the remaining elements of right subarray 
	   (if there are any) to temp*/
	while (j <= right)
		temp[k++] = arr[j++];

	/*Copy back the merged elements to original array*/
	for (i = left; i <= right; i++)
		arr[i] = temp[i];

	return inv_count;
}

///////////////////////////////////////////////////////////////////////////

int count_inversions(vector<int> A) {
	int array[A.size()];
	for (size_t i = 0; i < A.size(); i++)
		array[i] = A[i];
	
	return mergeSort(array, A.size());
}


static vector<string> split_str(const string& str, const string& delim)
{
	vector<string> tokens;
	size_t prev = 0, pos = 0;
	do
	{
		pos = str.find(delim, prev);
		if (pos == string::npos) pos = str.length();
		string token = str.substr(prev, pos-prev);
		if (!token.empty()) tokens.push_back(token);
		prev = pos + delim.length();
	}
	while (pos < str.length() && prev < str.length());
	return tokens;
}

int main(int argc, char **argv) {
	vector<int> ind;

	int i = 0;
	int max_inversions = 0;
	string line;
	while (getline(cin, line)) {
		if (line[0] == '#' || line.size() == 0) {
			cout << line << endl;
			continue;
		}

		if (!line.empty() && line[line.size() - 1] == '\r')
			line.erase(line.size() - 1);

		auto words = split_str(line, " ");
		i++;
		if (i == 1) {
			for (string index: words) {
				ind.push_back(stoi(index));
			}
		}
		else if (i == 2) {
			max_inversions = stoi(words[0]);
		}
		else assert(false);
	}

	srand(atoi(argv[0]));

	int inversions = count_inversions(ind);
	int d = ind.size();

	while (inversions > max_inversions) {
		int j = rand() % d;
		if (ind[j] > j)
			swap(ind[j], ind[j+1]);
		if (ind[j] < j)
			swap(ind[j], ind[j-1]);
		inversions = count_inversions(ind);
	}
	
	for (int i: ind)
		cout << i << " ";
	cout << endl;
}
