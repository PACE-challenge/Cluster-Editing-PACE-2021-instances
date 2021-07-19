import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from tqdm import tqdm


for k, categories in enumerate([
        ['rec.sport.baseball', 'soc.religion.christian', 'rec.autos', 'talk.politics.mideast', 'misc.forsale'],
        ['rec.autos', 'comp.sys.mac.hardware', 'misc.forsale', 'talk.politics.mideast', 'sci.electronics'],
        ['talk.politics.mideast', 'rec.motorcycles', 'rec.sport.hockey', 'soc.religion.christian', 'comp.sys.mac.hardware'],
        ['misc.forsale', 'sci.space', 'comp.sys.ibm.pc.hardware', 'talk.politics.misc', 'rec.motorcycles'],
        ['rec.sport.hockey', 'soc.religion.christian', 'talk.politics.guns', 'rec.motorcycles', 'sci.space']
        ]):
    print("Generating dataset", k+1)


    print("Fetching data")
    newsgroups = fetch_20newsgroups(categories=categories, remove=('headers', 'footers', 'quotes'))
    vectorizer = TfidfVectorizer()
    print("Vectorizing data")
    data = vectorizer.fit_transform(newsgroups.data).toarray()
    pca = PCA(n_components=40)
    print("Computing PCA")
    X = pca.fit_transform(data)
    # make sure datapoints are in a nice order
    order = np.argsort(newsgroups.target)
    X = X[order]

    n = X.shape[0]

    S = np.zeros((n,n))

    print("Computing similarity matrix")
    for i in tqdm(range(n)):
        for j in range(n):
            S[i,j] = X[i].T @  X[j] / np.sqrt(X[i].T @ X[i]) / np.sqrt(X[j].T @ X[j])
    # values are in [-1, 1]
    S = (S + 1) / 2

    np.savetxt("data_"+str(k+1)+".csv", S, delimiter=', ', fmt='%.5f')
