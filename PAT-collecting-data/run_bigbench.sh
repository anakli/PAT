#!/bin/bash


# Run BigBench queries one by one

#for i in $(seq 1 30)
#for i in $(seq 5 30)
#for i in $(seq 3 4)
#for i in 8 14 16 21 26 28 29 3
for i in 3
do 

echo "cd /home/ubuntu/bigbench-spark2/Big-Data-Benchmark-for-Big-Bench; ./bin/bigBench runQuery -q $i -U -e spark_sql -s 1" > ~/PAT/PAT-collecting-data/launch_spark.sh
#~/PAT/PAT-collecting-data/run.sh bigbench-q$i-i3.xl-8node-SSD250GB-nvme-8exec-4cores-24GBmem
#~/PAT/PAT-collecting-data/run.sh bigbench-q$i-i3.xl-8node-SSD250GB-8exec-4cores-24GBmem
~/PAT/PAT-collecting-data/run.sh bigbench-q$i-i3.xl-8node-HDD500GB-8exec-4cores-24GBmem-rerun
#~/PAT/PAT-collecting-data/run.sh bigbench-q$i-i3.xl-8node-HDD500GB-SSD250GB-8exec-4cores-24GBmem

#~/PAT/PAT-collecting-data/run.sh bigbench-q$i-i3.4xl-8node-nvme-8exec-16cores-96GBmem

done
