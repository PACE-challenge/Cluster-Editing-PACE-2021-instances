import numpy as np
import sys

if len(sys.argv) < 2:
	print('usage: converter.py Matrix-File [threshold][n]   \n // default for threshold is 0.5; if n is given, then only the first n rows and columns are considered ')
	sys.exit(1)
        
S = np.loadtxt(sys.argv[1], delimiter=', ')

threshold = 0.5
n = len(S)
	
if len(sys.argv) > 2:
	threshold = float(sys.argv[2])

if len(sys.argv) > 3:
	n = min(n, int(sys.argv[3]))

# limit instance size
x = np.arange(n)
S = S[x,:][:,x]
# ignore diagonal elements 
S[(x,x)] = -1
#print(S)

A = (S > threshold) * 1
#print(A)
m = A.sum() // 2

# use PACE .gr format
print("p cep", n, m)

for i in range(n):
	for j in range(i+1,n):
		if A[i,j] == 1:
			print(i+1, j+1)
