import numpy as np
import sys
import glob

instances = glob.glob("*.cm")

generated = 0
for instance in instances:
    f = open(instance)

    n = -1
    S = None
    for k, line in enumerate(f):
        words = line.split()
        if k == 0:
            n = int(words[0])
            S = np.zeros((n,n))
            continue
        if len(words) == 0:
            continue
        if k <= n:
            continue
        i = k - n - 1 

        for j in range(i+1, n):
            S[i,j] = float(words[j-(i+1)])

    # we only read the upper triangular half
    S = S + S.T
    # rescale to [0,1]
    S = S / np.max(np.abs(S)) / 2
    S = S + 0.5
    for i in range(n):
        S[i,i] = 1

    generated += 1
    np.savetxt("instance_"+str(generated)+".csv", S, delimiter=', ')
