#!/bin/bash

read -p "Some files contained in the datasets may be permanentely deleted. Continue? [y/n] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
fi

datasets=$(find . -maxdepth 2 -mindepth 2 -type d)

read -p "Delete .csv and .gr's in folders with setup script? [y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
	for dataset in $datasets
	do
		setup="$dataset/setup.sh"
		
		if [[ -f "$setup" ]]; then
			find $dataset -type f -name '*.csv' -delete
			find $dataset -type f -name '*.gr' -delete
		fi
	done
fi

read -p "Delete .gr instances converted from .csv's? [y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
	for dataset in $datasets
	do
		if [[ $dataset == *_converted ]]; then
			find $dataset -type f -name '*.gr' -delete
		fi
	done
fi

read -p "Delete pdf files? [y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
	for dataset in $datasets
	do
		find $dataset -type f -name '*.pdf' -delete
	done
fi
