#!/bin/sh

python3 generate.py

find . -type f -name '*.csv' -exec python3 ../normalize.py {} \;

cd ../.. > /dev/null
./instance-convertion.sh ./weighted/newsgroups
