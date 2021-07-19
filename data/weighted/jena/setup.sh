#!/bin/sh

wget -nc https://bio.informatik.uni-jena.de/wp/wp-content/uploads/2012/09/biological_bielefeld.zip
echo "unzipping archive"
unzip biological_bielefeld.zip > /dev/null

echo "converting instances"
python3 convert.py

rm -r biological/
rm biological_bielefeld.zip


find . -type f -name '*.csv' -exec python3 ../normalize.py {} \;

cd ../.. > /dev/null
./instance-convertion.sh ./weighted/jena
