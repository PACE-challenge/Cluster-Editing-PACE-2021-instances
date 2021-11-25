# Software prerequisites:
 * Required: g++, python3

## Python packages
 * Required python3 packages: numpy, matplotlib
 * Optional python3 packages (creating some datasets may fail without these): sklearn, pandas, tqdm
  
  python libraries can be installed as root using

    `pip3 install <packages>`
  or as a user

    `pip3 install --user <packages>`

# Usage
  The datasets can be downloaded and converted using the following command:

    `cd data && ./setup.sh`
  
  This creates all weighted and unweighted graphs from various data sources. 
  The datasets are stored in the data/ folder in different subfolders. Weighted instances are similarity matrices stored as csv files. Unweighted instances are stored as .gr files as edge lists in the dimacs format used by PACE. 
  The setup script additionally applies a normalization of the similarity values to use the [0,1] range of values. 
  Lines starting with # in the weighted graphs are comments.

  Visualization:

    `cd data && ./viz_all.sh`

  This creates a pdf rendering of the instances in the same location as the instance files.

# Dataset sources


- http://www.icsi.berkeley.edu/wcs/data.html

- https://scikit-learn.org/0.19/datasets/twenty_newsgroups.html
   
- https://transclust.compbio.sdu.dk/online_service/web.php  
  References:  
    [1] Tobias Wittkop, Dorothea Emig, Sita Lange, Sven Rahmann, Mario Albrecht, John H Morris, Sebastian Böcker, Jens Stoye, and Jan Baumbach. Partitioning biological data with transitivity clustering. Nature methods, 7(6):419–420, 2010. 

- https://bio.informatik.uni-jena.de/data/  
    References:  
    [2] Sven Rahmann, Tobias Wittkop, Jan Baumbach, Marcel Martin, Anke Truss, and Sebastian Böcker. Exact and Heuristic Algorithms for Weighted Cluster Editing. Proc. of Computational Systems Bioinformatics (CSB 2007), volume 6, pages 391—401, 2007.  
    [3] Sebastian Böcker, Sebastian Briesemeister, Quang Bao Anh Bui, and Anke Truss. A fixed-parameter approach for Weighted Cluster Editing. Proc. of Asia-Pacific Bioinformatics Conference (APBC 2008), volume 5, pages 211—220 of Series on Advances in Bioinformatics and Computational Biology, Imperial College Press, 2008.
   
- http://snap.stanford.edu/data/index.html  
    References:  
    [4] J. Leskovec and A. Krevl. SNAP Datasets: Stanford Large Network Dataset Collection. http://snap.stanford.edu/data. June 2014


# Solvers

See the [PACE 2021](https://doi.org/10.4230/LIPIcs.IPEC.2021.26) report for a list of known solvers with public repository as well as the ranking. 
