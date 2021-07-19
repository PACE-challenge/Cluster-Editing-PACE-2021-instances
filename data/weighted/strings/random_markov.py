import numpy as np
import sys
import argparse


def count_inversions(a):
    n = a.size
    counts = np.arange(n) & -np.arange(n)  # The BIT
    ags = a.argsort(kind='mergesort')    
    return  BIT(ags,counts,n)

def BIT(ags,counts,n):
    res = 0        
    for x in ags :
        i = x
        while i:
            res += counts[i]
            i -= i & -i
        i = x+1
        while i < n:
            counts[i] -= 1
            i += i & -i
    return  res  


parser = argparse.ArgumentParser()
parser.add_argument("-n", type=int, help="total number of strings to generate", default=250)
parser.add_argument("-c", type=int, help="number of markov models or clusters used to generate the strings", default=10)
parser.add_argument("-d", type=int, help="number of alphabet characters to use in strings", default=26)
parser.add_argument("--alphabet-frac", type=float, help="minimum fraction of the d states that must be used in the markov chain", default=0.33)
parser.add_argument("--inversion-frac", type=float, help="Fraction of the at most (d choose 2) inversions in the permutation of the states will be allowed", default=0.1)
parser.add_argument("--variance", type=float, help="variance in cluster sizes in range (0, inf) (0 or inf not allowed), close to 0 - very random, close to inf or 100 - almost identical cluster sizes, in practice it's good to use values [1, 100]", default=100000)
parser.add_argument("--loops", type=int, help="number of loops in markov chain", default=1)
parser.add_argument("--loop-frac", type=float, help="fraction of the state array (in the middle) that is looped", default=1/3)
parser.add_argument("--edge-bias", type=float, help="a bias of 1 means all strings generated from a markov model will be almost the same, 0 means they will likely be quite different", default=1/3)
args = parser.parse_args()

args.c = min(args.c, args.n)
cluster_sizes = np.random.dirichlet(np.ones(args.c) * args.variance, 1)[0]
cluster_sizes = np.round(args.n * np.cumsum(cluster_sizes))
cluster_sizes[1:] = cluster_sizes[1:] - cluster_sizes[:-1]
cluster_sizes = cluster_sizes.astype(int)

print("# BEGIN_TRUE_CLUSTERS")
n = 0
for cluster in range(args.c):
    print('#', end=' ')
    for i in range(cluster_sizes[cluster]):
        print(i + n, end=' ')
    n += cluster_sizes[cluster]
    print()
print("# END_TRUE_CLUSTERS")

for cluster in range(args.c):
    n = cluster_sizes[cluster]
    # states in the markov chain
    # the markov chain starts in A[0] end in A[-1] = !

    A = [chr(i) for i in range(ord('A'), ord('A') + args.d)] + ['!']
    A = np.array(A)

    # permute states in between
    d = len(A)
    ind = np.arange(d)
    i = 0

    while i < (d-1) * args.alphabet_frac:
        np.random.shuffle(ind)
        i = np.argmax(A[ind] == '!')
    ind = ind[:i+1]
    assert A[ind[-1]] == '!'

    A = A[ind]
    d = len(A)
    
    ind_copy = np.argsort(ind)
    ind = np.argsort(ind)
    inversions = count_inversions(ind)
    # keep swapping elements to reduce inversions
    while inversions > args.inversion_frac * (d*(d-1) / 2):
        #print(ind)
        j = np.random.randint(d)
        if ind[j] > j:
            ind[j], ind[j+1] = ind[j+1], ind[j]
        if ind[j] < j:
            ind[j], ind[j-1] = ind[j-1], ind[j]
        inversions = count_inversions(ind)
        #print("Inversions =", inversions)
    #print(ind)
    A = A[ind[ind_copy]]
    #print("Inversions =", inversions)
    #print(ind)
    #print(A)

    A = list(A)

    m = len(A) / 2
    loop_start, loop_end = np.round([m - args.loop_frac/2, m + args.loop_frac/2]).astype(int)

    A = A[0: loop_start] + A[loop_start:loop_end] * args.loops + A[loop_end:]
    A = A + ['!'] * 10
    A = np.array(A)

    d = len(A)


    M = np.zeros((d, d))

    # generate random markov transition matrix
    M = np.zeros((d,d))

    for r, w in [(-1, 1-args.edge_bias), (0, 1-args.edge_bias), (1, 5), (2, 1-args.edge_bias)]:
        # create a "path" markov chain
        # by which a state jumps r states forward
        P = np.zeros((d,d))
        for i in range(d):
            if i + r >= 0 and i + r < d:
                P[i, i+r] = (args.edge_bias + np.random.rand() * (1 - args.edge_bias))

        # add this path to the markov chain
        M = M + P * w
        
    M[-1,-1] = 1
    for i in range(d):
        M[i] = M[i] / M[i].sum()

    # generate sequences from markov chain
    for _ in range(n):
        i = 0
        while A[i] != '!':
            print(A[i], end='')
            p = np.random.rand()
            s = 0
            j = 0
            while s + M[i,j] < p and j < d - 1:
                s += M[i,j]
                j += 1
            i = j
        print(A[i])
