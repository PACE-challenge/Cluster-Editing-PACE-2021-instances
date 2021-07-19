#!/bin/bash

if [ $# -lt 1 ]; then 
	echo "Usage ./generate.sh filename <arguments/--help>"
	exit
fi

file=$1

if [ "$file" = "--help" ]; then
	echo "This wrapper passes all but the first arguments to generate.py"
	python3 generate.py --help
	exit
fi

echo Writing $file.strings
python3 generate.py ${@:2} > $file.strings
echo Writing $file.csv
./compute_similarity/main < $file.strings > $file.csv
