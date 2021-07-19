import numpy as np
import matplotlib.pyplot as plt
import sys

def read_instance(filename):
    if filename.endswith(".csv"):
        return np.loadtxt(filename, delimiter=', ')
    assert(filename.endswith(".gr"))
    # adjacency matrix is the similaity matrix in this case
    S = None
    f = open(filename)
    p_read = False
    for line in f:
        words = line.split()
        if len(words) == 0 or words[0] == 'c':
            continue
        if words[0] == 'p':
            if p_read:
                continue
            p_read = True
            n = int(words[2])
            S = np.zeros((n,n))
        else:
            assert(len(words) == 2)
            i, j = int(words[0])-1, int(words[1])-1
            S[i,j] = 1
            S[j,i] = 1
    return S

S = read_instance(sys.argv[1])
plt.hist(S.flatten(), bins=np.linspace(0, 1, 200))
plt.title("Histogram of similarity values")
plt.xlabel("Similarity")
plt.ylabel("Frequency")
plt.savefig(sys.argv[1]+"_viz2.pdf", dpi=400)
plt.close()

n = len(S)
x = np.arange(n)

S[(x,x)] = 0.5
S = S - 0.5
m = np.quantile(np.abs(S), 0.99)
S = S / m / 2
S = S + 0.5
S[(x,x)] = 1 
#print(S)

plt.imshow(S, vmin=0, vmax=1, cmap='RdBu_r')
plt.colorbar()
plt.title("Similarity matrix")
plt.savefig(sys.argv[1]+"_viz1.pdf", dpi=400)
plt.close()
