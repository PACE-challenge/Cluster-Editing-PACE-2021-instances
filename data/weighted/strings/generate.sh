#!/bin/bash

if [ $# -lt 1 ]; then 
	echo "Usage ./generate.sh filename <arguments/--help>"
	exit
fi

file=$1

if [ "$file" = "--help" ]; then
	echo "This wrapper passes all but the first arguments to random_markov.py"
	python3 random_markov.py --help
	exit
fi

echo Writing $file.strings
python3 random_markov.py ${@:2} > $file.strings
echo Writing $file.csv
./compute_similarity/main < $file.strings > $file.csv
echo Visualizing $file.csv
python3 viz.py $file.csv
