#!/bin/bash

cd ~/PAT/PAT-collecting-data/results


if [ -z "$1" ]
  then
    echo "usage: ./post-proc.sh q#"
	exit
fi

query_name=$1

mkdir -p /home/anakli/PAT/PAT-collecting-data/results/tpcds-$query_name
mkdir -p /home/anakli/PAT/PAT-collecting-data/results/tpcds-$query_name/pdf
mkdir -p /home/anakli/PAT/PAT-collecting-data/results/tpcds-$query_name/disk_stats


for test_name in tpcds-$query_name-*
do
	echo $test_name
	cd ~/PAT/PAT-post-processing
	if [[ ($test_name == *"HDD"*) || ($test_name == *"hdd"*) ]] ; then
		disk1="xvdd"
		if [[ ($test_name == *"SSD"*) || ($test_name == *"ssd"*)  ]]; then
			disk2="xvdc"
		else
			disk2="xvdd"
		fi
	elif [[ ($test_name == *"SSD"*) || ($test_name == *"ssd"*) ]] ; then
		disk1=xvdc
		if [[ ($test_name == *"NVMe"*) || ($test_name == *"nvme"*)  ]]; then
			disk2="nvme"
		else
			disk2="xvdc"
		fi
	else
		disk1="nvme"
		disk2="nvme"
	fi

	echo "disk1: $disk1, disk2: $disk2"
	sed -i "96s/if \"[a-z 0-9]*\" in/if \"${disk1}\" in/" disk_module.py
	sed -i "103s/elif \"[a-z 0-9]*\" in/elif \"${disk2}\" in/" disk_module.py

	sed -i "55s/.*/\t<source>\/home\/anakli\/PAT\/PAT-collecting-data\/results\/${test_name}\/instruments<\/source>/" config.xml
	./pat-post-process.py
	cp /home/anakli/PAT/PAT-collecting-data/results/$test_name/instruments/PAT-Result.pdf /home/anakli/PAT/PAT-collecting-data/results/$test_name/instruments/PAT-$test_name-postproc.pdf
	cp /home/anakli/PAT/PAT-collecting-data/results/$test_name/instruments/disk_avg_stats.csv /home/anakli/PAT/PAT-collecting-data/results/$test_name/instruments/disk-avg-stats-$test_name.csv
	cp /home/anakli/PAT/PAT-collecting-data/results/$test_name/instruments/PAT-Result.pdf /home/anakli/PAT/PAT-collecting-data/results/tpcds-$query-name/pdf/PAT-$test_name-postproc.pdf
	cp /home/anakli/PAT/PAT-collecting-data/results/$test_name/instruments/disk_avg_stats.csv /home/anakli/PAT/PAT-collecting-data/results/tpcds-$query_name/disk_stats/disk-avg-stats-$test_name.csv

	#break
	cd ~/PAT/PAT-collecting-data/results
done

#cd ~/PAT/PAT-collecting-data
