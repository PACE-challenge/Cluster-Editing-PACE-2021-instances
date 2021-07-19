import numpy as np
import matplotlib.pyplot as plt
import sys

S = np.loadtxt(sys.argv[1], delimiter=', ')
comments = ""
csv = open(sys.argv[1])
for i, line in enumerate(csv):
    if line.startswith("#"):
        comments = comments + line
        continue
csv = open(sys.argv[1], "w")
print(comments[:-1], file=csv)

n = len(S)
x = np.arange(n)
S[(x,x)] = 0.5
S = S - 0.5
m = np.max(np.abs(S))
S = S / m / 2
S = S + 0.5
S[(x,x)] = 1 
#print(S)

csv = open(sys.argv[1], "a")
np.savetxt(csv, S, delimiter=', ')
