#!/bin/bash

cd ~/PAT/PAT-post-processing

#Afor i in {1..99}
#for i in {1..99}
for i in {1..13} 15 {17..22} {24..99}
do
	./post-proc-tpcds.sh q$i
done

