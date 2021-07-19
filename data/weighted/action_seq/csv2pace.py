#!/usr/bin/env python3
import math

# Convert CSV files to Pace format

THRESHOLD=0.35
N=1000

data = []
line = input()

while line is not None:
    if line[0] == '#':
        line = input()
        continue
    row = [math.floor((float(x.strip())-THRESHOLD)*N) for x in line.strip().split(',')]
    data.append(row)
    try:
        line = input()
    except EOFError:
        line = None

n = len(data)
for i in range(n):
    assert(len(data[i]) == n)

# now remember the pairs that are positive
edges = set()
for i in range(n):
    for j in range(i+1, n):
        if data[i][j] > 0:
            edges.add((i+1, j+1))

print("p cep", n, len(edges))
for e in edges:
    print(e[0], e[1])
