#! /bin/bash

# generates graphs from a square weight matrix 
# Either goes through all csv files whose path matches the following pattern ./weighted/*/*.csv


if [ -z "$1" ]; then
	folderWithData="weighted"
	datasets=$(find $folderWithData -maxdepth 1 -mindepth 1 -type d)
else
	datasets=$1													# ... or give the data sets as parameter to the script
fi



# the script converts with threshold-values starting from minThres and increasing by thresStep until maxThres is smaller than the current threshold-value
minThres=0.1							# minimum threshold for an edge
maxThres=0.9							# minimum threshold for an edge
thresStep=0.1							# increase in thresholds between instances

for dataset in $datasets
do
	if [ -d $dataset ]; then
		echo "##############################################################################################################"
		echo "##############################################################################################################"
		echo "##############################################################################################################"
		echo "Runnig dataset $dataset"
		targetDirectory="unweighted/$(basename $dataset)_converted"			# directory where to put to convert
		files=$(ls $dataset/*.csv)
		for fileName in $files
		do
			mkdir -p $targetDirectory
			./converter/convert-vary-thresholds $fileName $targetDirectory $minThres $maxThres $thresStep
		done
	else
		echo "$dataset does not exist"
	fi
done
