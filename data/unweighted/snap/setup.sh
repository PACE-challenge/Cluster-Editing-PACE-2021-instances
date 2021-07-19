#!/bin/bash

pushd snap-to-dimacs > /dev/null
make
popd > /dev/null

rm *.gz
rm *.txt
curl https://snap.stanford.edu/data/as20000102.txt.gz -O
curl https://snap.stanford.edu/data/p2p-Gnutella04.txt.gz -O 
curl https://snap.stanford.edu/data/p2p-Gnutella05.txt.gz -O 
curl https://snap.stanford.edu/data/p2p-Gnutella06.txt.gz -O 
curl https://snap.stanford.edu/data/p2p-Gnutella08.txt.gz -O 
curl https://snap.stanford.edu/data/p2p-Gnutella09.txt.gz -O 
curl https://snap.stanford.edu/data/p2p-Gnutella25.txt.gz -O 
curl https://snap.stanford.edu/data/ca-HepTh.txt.gz -O
curl https://snap.stanford.edu/data/bigdata/communities/com-youtube.ungraph.txt.gz -O
curl https://snap.stanford.edu/data/facebook_combined.txt.gz -O
curl https://snap.stanford.edu/data/twitter_combined.txt.gz -O
curl https://snap.stanford.edu/data/soc-Epinions1.txt.gz -O
curl https://snap.stanford.edu/data/soc-Slashdot0811.txt.gz -O
curl https://snap.stanford.edu/data/bigdata/communities/com-dblp.ungraph.txt.gz -O
curl https://snap.stanford.edu/data/soc-Slashdot0902.txt.gz -O
curl https://snap.stanford.edu/data/email-Eu-core.txt.gz -O
curl https://snap.stanford.edu/data/email-Enron.txt.gz -O
curl https://snap.stanford.edu/data/ca-AstroPh.txt.gz -O
curl https://snap.stanford.edu/data/ca-CondMat.txt.gz -O
curl https://snap.stanford.edu/data/ca-GrQc.txt.gz -O
curl https://snap.stanford.edu/data/ca-HepPh.txt.gz -O
curl https://snap.stanford.edu/data/roadNet-CA.txt.gz -O
curl https://snap.stanford.edu/data/roadNet-PA.txt.gz -O
curl https://snap.stanford.edu/data/roadNet-TX.txt.gz -O
curl https://snap.stanford.edu/data/bigdata/communities/com-amazon.ungraph.txt.gz -O
curl https://snap.stanford.edu/data/web-NotreDame.txt.gz -O
curl https://snap.stanford.edu/data/web-Stanford.txt.gz -O
curl https://snap.stanford.edu/data/amazon0302.txt.gz -O
curl https://snap.stanford.edu/data/amazon0312.txt.gz -O
curl https://snap.stanford.edu/data/amazon0505.txt.gz -O
curl https://snap.stanford.edu/data/amazon0601.txt.gz -O
curl https://snap.stanford.edu/data/soc-sign-epinions.txt.gz -O
curl https://snap.stanford.edu/data/soc-sign-Slashdot081106.txt.gz -O
curl https://snap.stanford.edu/data/soc-sign-Slashdot090216.txt.gz -O
curl https://snap.stanford.edu/data/soc-sign-Slashdot090221.txt.gz -O
curl https://snap.stanford.edu/data/loc-gowalla_edges.txt.gz -O
# curl https://snap.stanford.edu/data/as-skitter.txt.gz -O
# curl https://snap.stanford.edu/data/bigdata/communities/com-orkut.ungraph.txt.gz -O
# curl https://snap.stanford.edu/data/wiki-topcats.txt.gz -O
# curl https://snap.stanford.edu/data/bigdata/communities/com-lj.ungraph.txt.gz -O
# curl https://snap.stanford.edu/data/soc-LiveJournal1.txt.gz -O
# curl https://snap.stanford.edu/data/soc-pokec-relationships.txt.gz -O
# curl https://snap.stanford.edu/data/gplus_combined.txt.gz -O
# curl https://snap.stanford.edu/data/wiki-Talk.txt.gz -O
# curl https://snap.stanford.edu/data/web-BerkStan.txt.gz -O
# curl https://snap.stanford.edu/data/web-Google.txt.gz -O

for a in `ls -1 *.txt.gz`; 
do 
	gzip -df $a ; 
done

for a in `ls -1 *.txt`; do 
	newFile="${a%.txt}.gr"
	echo converting $a into $newFile
	cat $a | snap-to-dimacs/main > $newFile
	rm $a
	sed -i 's/e //g' $newFile
	sed -i 's/p/p cep/g' $newFile
# 	head $newFile
done
