#!/bin/bash

pushd compute_similarity > /dev/null
make
popd > /dev/null

pushd fast_inversion > /dev/null
make
popd > /dev/null

mkdir -p ../../unweighted/action_seq_converted/

for n in 10 20 30 40 50 60 70 80 90 100 120 140 160 180 200 300 400 500
do
	for c in 2 3 5 8 10
	do
		./generate.sh "pace_actionseq_${n}_${c}" -n $n -c $c 
		./csv2pace.py < pace_actionseq_${n}_${c}.csv > ../../unweighted/action_seq_converted/pace_actionseq_${n}_${c}.gr
	done
done

for n in 100 120 140 160 180 200 300 400 500
do
	for c in 20
	do
		./generate.sh "pace_actionseq_${n}_${c}" -n $n -c $c 
		./csv2pace.py < pace_actionseq_${n}_${c}.csv > ../../unweighted/action_seq_converted/pace_actionseq_${n}_${c}.gr
	done
done

rm *.strings

