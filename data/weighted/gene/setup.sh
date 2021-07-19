#!/bin/sh

wget -nc https://transclust.compbio.sdu.dk/downloads/clustering_example/sfld_brown_et_al_amidohydrolases_costmatrix_for_beh_with_threshold_100.cm
python3 convert.py

rm sfld_brown_et_al_amidohydrolases_costmatrix_for_beh_with_threshold_100.cm

find . -type f -name '*.csv' -exec python3 ../normalize.py {} \;

cd ../.. > /dev/null
./instance-convertion.sh ./weighted/gene
