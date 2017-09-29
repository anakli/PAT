#!/bin/bash

cd ~/PAT/PAT-post-processing

#Afor i in {1..99}
#for i in {1..99}
for i in {1..13} 15 {17..22} {24..93} {96..99}
do
	./post-proc-tpcds300.sh q$i
done

