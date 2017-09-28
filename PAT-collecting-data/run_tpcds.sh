#!/bin/bash




# Run BigBench queries one by one

#for i in $(seq 1 99)
#for i in $(seq 94 99)
for i in {1..13} 15 {17..22} {24..93} {96..99}
#for i in 1 8 14 16 21 26 28 29
do 

#echo "/home/ubuntu/crail-deployment/spark/bin/spark-submit -v --master yarn-client --num-executors 8 --executor-cores 16 --executor-memory 96G --driver-memory 48G --class com.ibm.crail.benchmarks.Main /home/ubuntu/crail-deployment/spark/apps/jars-ana/sql-benchmarks-1.0.jar -t q$i -i /tpcds1TBpq -a save,/tpcds10-output-q$i -of parquet" > ~/PAT/PAT-collecting-data/launch_spark.sh
echo "/home/ubuntu/crail-deployment/spark/bin/spark-submit -v --master yarn-client --num-executors 8 --executor-cores 16 --executor-memory 96G --driver-memory 48G --class com.ibm.crail.benchmarks.Main /home/ubuntu/crail-deployment/spark/apps/jars-ana/sql-benchmarks-1.0.jar -t q$i -i /tpcds300 -a save,/tpcds300-output-q$i -of parquet" > ~/PAT/PAT-collecting-data/launch_spark.sh
#echo "/home/ubuntu/crail-deployment/spark/bin/spark-submit -v --master yarn-client --num-executors 8 --executor-cores 4 --executor-memory 24G --driver-memory 48G --class com.ibm.crail.benchmarks.Main /home/ubuntu/crail-deployment/spark/apps/jars-ana/sql-benchmarks-1.0.jar -t q$i -i /tpcds1TBpq -a save,/tpcds10-output-q$i -of parquet" > ~/PAT/PAT-collecting-data/launch_spark.sh
#~/PAT/PAT-collecting-data/run.sh tpcds-q$i-i3.2xl-8node-SSD250GB-nvme-8exec-8cores-48GBmem
#~/PAT/PAT-collecting-data/run.sh tpcds-q$i-i3.2xl-8node-nvme-8exec-8cores-48GBmem
#~/PAT/PAT-collecting-data/run.sh tpcds-q$i-i3.2xl-8node-SSD250GB-8exec-8cores-48GBmem
#~/PAT/PAT-collecting-data/run.sh tpcds-q$i-i3.4xl-8node-SSD250GB-8exec-16cores-96GBmem
#~/PAT/PAT-collecting-data/run.sh tpcds-q$i-i3.4xl-8node-SSD250GB-8exec-16cores-96GBmem
#~/PAT/PAT-collecting-data/run.sh tpcds-q$i-i3.4xl-8node-SSD250GB-nvme-8exec-16cores-96GBmem
#~/PAT/PAT-collecting-data/run.sh tpcds-q$i-i3.xl-8node-nvme-8exec-4cores-24GBmem
#~/PAT/PAT-collecting-data/run.sh tpcds-q$i-i3.xl-8node-SSD250GB-nvme-8exec-4cores-24GBmem
#~/PAT/PAT-collecting-data/run.sh tpcds-q$i-i3.2xl-8node-nvme-8exec-8cores-48GBmem-rerun
#~/PAT/PAT-collecting-data/run.sh tpcds-q$i-i3.2xl-8node-SSD250GB-8exec-8cores-48GBmem
#~/PAT/PAT-collecting-data/run.sh tpcds-q$i-i3.2xl-8node-HDD500GB-SSD250GB-8exec-8cores-48GBmem
#~/PAT/PAT-collecting-data/run.sh tpcds-q$i-i3.2xl-8node-HDD500GB-8exec-8cores-48GBmem

#~/PAT/PAT-collecting-data/run.sh tpcds-q$i-r4.4xl-8node-SSD250GB-8exec-16cores-96GBmem
#~/PAT/PAT-collecting-data/run.sh tpcds-q$i-r4.4xl-8node-HDD500GB-SSD250GB-8exec-16cores-96GBmem-rerun2
#~/PAT/PAT-collecting-data/run.sh tpcds-q$i-r4.4xl-8node-HDD500GB-SSD250GB-8exec-4cores-96GBmem
#~/PAT/PAT-collecting-data/run.sh tpcds-q$i-r4.4xl-8node-HDD500GB-SSD250GB-8exec-1cores-96GBmem
#~/PAT/PAT-collecting-data/run.sh tpcds-q$i-r4.4xl-8node-HDD500GB-8exec-16cores-96GBmem-redo

~/PAT/PAT-collecting-data/run.sh tpcds300-q$i-i3.4xl-8node-nvme-8exec-16cores-96GBmem

done
