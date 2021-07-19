#!/bin/bash

pushd compute_similarity > /dev/null
make
popd > /dev/null

for strings in *.strings ; do
	file=$(basename $strings .strings)
	echo $file
	./compute_similarity/main < $file.strings > $file.csv
done

cd ../.. > /dev/null
./instance-convertion.sh ./weighted/strings
