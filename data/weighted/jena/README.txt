Source: https://bio.informatik.uni-jena.de/data/
under "Cluster Editing evaluation data"

Only instances with at least 100 and at most 4999 vertices are created.
To change this update convert.py in the lines containing:
	if n < 100 or n > 5000

The dataset consists of positive and negative values. Using 0 as a threshold leads to very poor results.
The conversion script tries to guess a better threshold, but due to shape of the similarity distribution
this threshold is very difficult to estimate automatically.
