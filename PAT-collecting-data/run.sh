#!/bin/bash

# Run test and post-process data

#/home/ubuntu/crail-deployment/hadoop/bin/hadoop fs -rm -r /user/ubuntu/data/terasort_out_400g
/home/ubuntu/crail-deployment/hadoop/clear-slave-caches.sh

test_name=$1
./pat run $test_name

cd ~/PAT/PAT-post-processing
sed -i "55s/.*/\t<source>\/home\/ubuntu\/PAT\/PAT-collecting-data\/results\/${test_name}\/instruments<\/source>/" config.xml
./pat-post-process.py
cp /home/ubuntu/PAT/PAT-collecting-data/results/$test_name/instruments/PAT-Result.pdf /home/ubuntu/PAT/PAT-collecting-data/results/$test_name/instruments/PAT-$test_name.pdf
cd ~/PAT/PAT-collecting-data
