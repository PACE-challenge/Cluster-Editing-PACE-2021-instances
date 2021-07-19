import numpy as np
import pandas as pd

data = pd.read_csv('http://www1.icsi.berkeley.edu/wcs/data/cnum-maps/cnum-vhcm-lab-new.txt', sep='\t')
print(data)

X = np.array([data['L*'], data['a*'], data['b*']]).T

n = X.shape[0]

S = np.zeros((n,n))
for i in range(n):
    for j in range(n):
        d = X[i] - X[j]
        S[i,j] = np.exp(-0.001 * (d.T @ d))

np.savetxt("data.csv", S, delimiter=', ', fmt='%.6f')
