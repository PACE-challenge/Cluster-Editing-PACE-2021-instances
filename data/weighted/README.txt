Folder containing weighted instances for Weighted Cluster Editing.

Instances are encoded as [0,1]-similarity matrices as .csv files.
(the .csv files may have comment lines beginning with #)

Subfolders which contain a setup.sh script are assumed to generate
the .csv files and will be automatically normalized to the full
[0,1] range of values (not strictly necessary but some heuristics
benefit from this) and the original .csv will be overwritten.
