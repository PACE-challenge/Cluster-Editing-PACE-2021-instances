import numpy as np
import sys
import argparse
import os
import subprocess

np.set_printoptions( linewidth=10000000) 


def fix_inversion_frac(A, ind, inv_frac):
    d = len(A)
    max_inversions = np.ceil(inv_frac * (d*(d-1) / 2))

    text = ""
    for i in ind:
        text += str(i) + " ";
    text += "\n"
    text+= str(max_inversions) + "\n"

    output = subprocess.check_output(
        ["./fast_inversion/main", str(np.random.randint(100000))],
        input=text.encode()
    )

    ind2 = []
    for i in output.split():
        ind2.append(int(i))
    ind2 = np.array(ind2)
    return A[ind2].copy(), ind2
    



parser = argparse.ArgumentParser()
parser.add_argument("-n", type=int, help="total number of strings to generate", default=250)
parser.add_argument("-c", type=int, help="number of markov models or clusters used to generate the strings", default=10)
parser.add_argument("--variance", type=float, help="variance in cluster sizes in range (0, inf) (0 or inf not allowed), close to 0 - very random, close to inf or 100 - almost identical cluster sizes, in practice it's good to use values [1, 100]", default=8)
parser.add_argument("--global-string-blockiness", type=float, help="The closer to 1.0 the higher tendency for all tokens of the same type to be in a single block (in global referene)", default=0.5)
parser.add_argument("--inversion-global", type=float, help="Maximum fraction of inversions in the cluster reference string vs the global reference string", default=1.0)
parser.add_argument("--inversion-local", type=float, help="Maximum fraction of inversions in the datapoint reference string vs the cluster reference string", default=0.05)
parser.add_argument("--random-token-flip", type=float, help="The closter to 1.0 the more likely it is that a string from a cluster does not care which tokens are enabled/disabled in the cluster", default=0.2)
parser.add_argument("--tta-variance-global", type=float, help="Time to action are drawn from a normal distribution where the mean is fixed for a given token, but the variance is (this_arg) * mean", default=0.33)
parser.add_argument("--tta-variance-local", type=float, help="Time to action are drawn from a normal distribution where the mean is fixed for a given token, but the variance is (this_arg) * mean", default=0.11)
parser.add_argument("--seed", type=int, help="Set a custom (but) integer random seed", default=None)
parser.add_argument("--length-multiplier", type=int, help="Set this parameter higher if you want longer strings", default=2)
# statistics from the original paper
args = parser.parse_args()
args.d = 15
d = 15

if args.seed:
    np.random.seed(args.seed)

occurences = np.array([1841, 257, 225, 813, 752, 756, 32, 78, 72, 37, 86, 45, 20, 2, 6])
usage = np.array([100, 100, 100, 93, 92, 56, 13, 10, 9, 6, 5, 5, 5, 1, 1]) / 100
occurences = occurences / (usage * 620)
# occurance = average number of times a token appears
mdtta = np.array([278, 646, 437, 385, 178, 275, 894, 460, 234, 500, 52, 342, 900, 459, 162]) / 100

alphabet = [chr(i) for i in range(ord('0'), ord('9')+1)] + ['a', 'b', 'c', 'd', 'e']
assert(len(alphabet) == 15)

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

global_reference = []
goal_occ = np.ceil(args.length_multiplier * occurences).astype('int')
cur_occ = np.zeros_like(goal_occ)

# generate global reference with desired blockiness
while any(cur_occ < goal_occ):
    #ind = np.random.permute(d)
    ind = np.arange(d)
    for i in ind:
        goal = np.ceil(args.global_string_blockiness * goal_occ[i])
        goal = int(min(goal, goal_occ[i] - cur_occ[i]))
        for j in range(goal):
            global_reference.append(i)
            cur_occ[i] += 1

global_reference = np.array(global_reference, dtype=int)
#print("# Global reference: ", global_reference)

# generate clusters and datapoints within them
for cluster in range(args.c):
    # randomly permute global reference string while keeping the fraction of inversions in check
    shuf = np.random.permutation(len(global_reference))
    local_reference, shuf = fix_inversion_frac(global_reference, shuf, args.inversion_global)
    local_mdtta = np.random.normal(mdtta, mdtta*args.tta_variance_global)
    local_mdtta = np.clip(mdtta, 0.01, mdtta*10)
    

    # enable tokens according to the reference distribution usage
    enabled = [False] * len(global_reference)
    for i, token in enumerate(global_reference):
        if np.random.rand() < usage[token] and np.random.rand() < 0.5:
            enabled[i] = True

#    print("# Local reference in cluster", cluster, ":", local_reference)
#    print("# Enabled tokens: ", np.argwhere(enabled).flatten())

    # generate string from local reference
    n = cluster_sizes[cluster]
    for _ in range(n):
        shuf = np.random.permutation(len(global_reference))
        string, shuf = fix_inversion_frac(local_reference, shuf, args.inversion_local)
        string2 = []
    
        for i, token in enumerate(string):
            if enabled[shuf[i]]:
                if not np.random.rand() < args.random_token_flip * (1 - usage[token]):
                    string2.append(token)
            elif np.random.rand() < args.random_token_flip * usage[token]:
                    string2.append(token)

        for token in string2:
            print(alphabet[token], end='')
        print()
        for token in string2:
            r = np.random.normal(local_mdtta[token], local_mdtta[token] * args.tta_variance_local)
            r = np.clip(r, 0.01, np.inf)
            print("%.3f" % (r), end=' ')
        print()
                
