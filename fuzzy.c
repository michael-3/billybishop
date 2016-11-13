#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MIN(a,b) ((a) < (b) ? (a) : (b))

static const char* const CSV_FILENAME = "cities.csv";

int levenshtein(const char *s1, const char *s2) {
	int len1 = strlen(s1);
	int len2 = strlen(s2);

	const int rows = len1 + 1;
	const int cols = len2 + 1;
	int* matrix = (int*)malloc(rows * cols * sizeof(int));

	for (int i = 0; i < rows; i++) {
		matrix[i * cols] = i;
	}
	for (int j = 0; j < cols; j++) {
		matrix[j] = j;
	}

	for (int i = 1; i < rows; i++) {
		for (int j = 1; j < cols; j++) {
			int cost = s1[i-1] == s2[j-1] ? 0 : 1;
			int del = matrix[(i-1)*cols+j] + 1;
			int ins = matrix[i*cols+(j-1)] + 1;
			int sub = matrix[(i-1)*cols+(j-1)] + cost;
			matrix[i*cols+j] = MIN(del, MIN(ins, sub));

			if (i > 1 && j > 1 && s1[i-1] == s2[j-2] && s1[i-2] == s2[j-1]) {
				int current = matrix[i*cols+j];
				int trans = matrix[(i-2)*cols+(j-2)] + cost;
				matrix[i*cols+j] = MIN(current, trans);
			}
		}
	}

	printf("Dist for '%s' to '%s' is %d\n", s1, s2, matrix[rows*cols-1]);

	return matrix[rows * cols - 1];
}


int match(const char **strings, int slen, const char **cities, int clen) {
	int smallest = INT_MAX;
	int index = 0;
	for (int i = 0; i < slen; i++) {
		for (int j = 0; j < clen; j++) {
			int dist = levenshtein(strings[i], cities[j]);
			if (dist < smallest) {
				smallest = dist;
				index = j;
			}
		}
	}
	return index;
}
