#!/bin/bash

cd ~/PAT/PAT-post-processing

#Afor i in {1..99}
#for i in {1..99}
for i in 3 8 14 16 21 26 28 29
do
	./post-proc-bigbench300.sh q$i
done

