#/bin/bash

datasets=$(find . -maxdepth 2 -mindepth 2 -type d)

for dataset in $datasets
do
	setup="$dataset/setup.sh"
	
	if [[ -f "$setup" ]]; then
		echo "#########################################"
		echo "Running setup.sh in $dataset"
		pushd $dataset > /dev/null
		./setup.sh
		popd > /dev/null
	fi
done
