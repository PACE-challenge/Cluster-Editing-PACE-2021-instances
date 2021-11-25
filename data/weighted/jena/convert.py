import numpy as np
import sys
import glob

instances = glob.glob("biological/costmatrices_all_of_COG_score_10/*.cm")

for instance in instances:
    f = open(instance)

    n = -1
    S = None
    for k, line in enumerate(f):
        words = line.split()
        if k == 0:
            n = int(words[0])
            if n < 100 or n > 5000:
                break
            S = np.zeros((n,n))
            continue
        if len(words) == 0:
            continue
        if k <= n:
            continue
        i = k - n - 1 

        for j in range(i+1, n):
            S[i,j] = float(words[j-(i+1)])

    if n < 100 or n > 5000:
        continue

    # we only read the upper triangular half
    S = S + S.T
    # rescale to [0,1]
    S = S / np.max(np.abs(S)) / 2
    S = S + 0.5
    for i in range(n):
        S[i,i] = np.nan

    S = np.clip(S, 0, np.nanquantile(S, 0.98))
    S = S - np.nanquantile(S, 0.7)
    for i in range(n):
        S[i,i] = 0
    if np.max(np.abs(S)) != 0:
        S = S / np.max(np.abs(S)) / 2
    S = S + 0.5
    for i in range(n):
        S[i,i] = 1

    name = instance[instance.find("component_")+len("component_"):instance.rfind("_size")]
    np.savetxt("instance_"+str(name)+".csv", S, delimiter=', ')
