import numpy as np
import matplotlib.pyplot as plt
import sys
from sklearn.manifold import TSNE

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
plt.savefig(sys.argv[1][:-4]+"_viz2.pdf", dpi=400)
plt.close()

n = len(S)
x = np.arange(n)

# normalize instance
S[(x,x)] = 0.5 # stretch values to use full [0,1] range
S = S - 0.5
m = np.max(np.abs(S))
S = S / m / 2
S = S + 0.5
S[(x,x)] = 1 

# compute 2-d embedding
#print("computing tsne")
E = TSNE(n_components=2).fit_transform(S)
plt.scatter(E[:,0], E[:,1], c=x,cmap='jet')
plt.savefig(sys.argv[1][:-4]+"_viz5.pdf", dpi=400)
plt.close()
#print("done computing tsne")

# vizualise metric violations
M = np.zeros_like(S)
D = 1 - S
K = np.zeros_like(S)
for i in range(n):
    for j in range(n):
        K[i,j] = np.nan
        for k in range(n):
            if M[i,j] < D[i,j] - (D[i,k] + D[k,j]):
                M[i,j] = D[i,j] - (D[i,k] + D[k,j])
                K[i,j] = k
            


#plt.imshow(M, vmin=0, vmax=1, cmap='magma_r')
plt.imshow(M, cmap='magma_r')
plt.colorbar()
plt.title("Metric violation matrix (dark pixels = shorten distance)")
plt.savefig(sys.argv[1][:-4]+"_viz3.pdf", dpi=400)
plt.close()

plt.imshow(K, cmap='magma_r')
plt.colorbar()
plt.title("Which k was picked in metric violation matrix")
plt.savefig(sys.argv[1][:-4]+"_viz3k.pdf", dpi=400)
plt.close()

plt.imshow(K % 4, cmap='magma_r')
plt.colorbar()
plt.title("Which k mod 4 was picked in metric violation matrix")
plt.savefig(sys.argv[1][:-4]+"_viz3km4.pdf", dpi=400)
plt.close()

if True:
    # find closest metric matrix
    diff = 1
    SM = S.copy()
    while diff > 0.001:
        M = np.zeros_like(SM)
        DM = 1 - SM
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    M[i,j] = max(M[i,j], DM[i,j] - (DM[i,k] + DM[k,j]))
        SM = 1 - (DM - M)
        SM[(x,x)] = 0.5
        SM = SM - 0.5
        m = np.max(np.abs(SM))
        SM = SM / m / 2
        SM = SM + 0.5
        SM[(x,x)] = 1 
        diff = M.max()


    SM[(x,x)] = 0.5
    SM = SM - 0.5
    m = np.quantile(np.abs(SM), 0.99)
    SM = SM / m / 2
    SM = SM + 0.5
    SM[(x,x)] = 1 
    #print(S)

    
    #np.savetxt(sys.argv[1][:-4]+".metric", S, delimiter=', ')
    plt.imshow(SM, vmin=0, vmax=1, cmap='RdBu_r')
    plt.colorbar()
    plt.title("Closest \"metric\" matrix (constract enhanced)")
    plt.savefig(sys.argv[1][:-4]+"_viz6.pdf", dpi=400)
    plt.close()






# plot contract enhanced matrix

S[(x,x)] = 0.5
S = S - 0.5
m = np.quantile(np.abs(S), 0.99)
S = S / m / 2
S = S + 0.5
S[(x,x)] = 1 
#print(S)

plt.imshow(S, vmin=0, vmax=1, cmap='RdBu_r')
plt.colorbar()
plt.title("Similarity matrix (constract enhanced)")
plt.savefig(sys.argv[1][:-4]+"_viz1.pdf", dpi=400)
plt.close()

# print ""metric"" matrix
S=1-(D-M)

S[(x,x)] = 0.5
S = S - 0.5
S = S / m / 2
S = S + 0.5
S[(x,x)] = 1 

plt.imshow((S), vmin=0, vmax=1, cmap='RdBu_r')
plt.colorbar()
plt.title("Similarity matrix (1 round remetrification + constract enhancement)")
plt.savefig(sys.argv[1][:-4]+"_viz4.pdf", dpi=400)
plt.close()
