#!/bin/bash

cd ~/PAT/PAT-collecting-data/results


if [ -z "$1" ]
  then
    echo "usage: ./post-proc.sh q#"
	exit
fi

query_name=$1

mkdir -p ~/PAT/PAT-collecting-data/results/bb300-4node-$query_name
mkdir -p ~/PAT/PAT-collecting-data/results/bb300-4node-$query_name/pdf
mkdir -p ~/PAT/PAT-collecting-data/results/bb300-4node-$query_name/disk_stats
mkdir -p ~/PAT/PAT-collecting-data/results/bb300-4node-$query_name/perf
mkdir -p ~/PAT/PAT-collecting-data/results/bb300-4node-$query_name/cpu_stats


for test_name in bigbench300-$query_name-*4node*
do
	echo $test_name
	cd ~/PAT/PAT-post-processing
	if [[ ($test_name == *"HDD"*) || ($test_name == *"hdd"*) ]] ; then
		disk1="xvdd"
		#if [[ (($test_name == *"HDD"*) && ($test_name == *"SSD"*) || ($test_name == *"hdd"*) && ($test_name == *"ssd"*))  ]]; then
		if [[ ($test_name == *"SSD"*) || ($test_name == *"ssd"*)  ]]; then
			disk2="xvdc"
		else
			disk2="xvdd"
			#continue
		fi
	elif [[ ($test_name == *"SSD"*) || ($test_name == *"ssd"*) ]] ; then
		disk1=xvdc
		if [[ ($test_name == *"NVMe"*) || ($test_name == *"nvme"*)  ]]; then
			disk2="nvme"
		else
			disk2="xvdc"
			#continue
		fi
	else
		#continue
		disk1="nvme"
		disk2="nvme"
	fi

	echo "disk1: $disk1, disk2: $disk2"
	sed -i "96s/if \"[a-z 0-9]*\" in/if \"${disk1}\" in/" disk_module.py
	sed -i "103s/elif \"[a-z 0-9]*\" in/elif \"${disk2}\" in/" disk_module.py

	sed -i "55s/.*/\t<source>\/home\/ubuntu\/PAT\/PAT-collecting-data\/results\/${test_name}\/instruments<\/source>/" config.xml
	./pat-post-process.py
	cp ~/PAT/PAT-collecting-data/results/$test_name/instruments/PAT-Result.pdf ~/PAT/PAT-collecting-data/results/$test_name/instruments/PAT-$test_name-postproc.pdf
	cp ~/PAT/PAT-collecting-data/results/$test_name/instruments/disk_avg_stats.csv ~/PAT/PAT-collecting-data/results/$test_name/instruments/disk-avg-stats-$test_name.csv
	cp ~/PAT/PAT-collecting-data/results/$test_name/instruments/perf.csv ~/PAT/PAT-collecting-data/results/$test_name/instruments/perf-$test_name.csv
	cp ~/PAT/PAT-collecting-data/results/$test_name/instruments/PAT-Result.pdf ~/PAT/PAT-collecting-data/results/bb300-4node-$query_name/pdf/PAT-$test_name-postproc.pdf
	cp ~/PAT/PAT-collecting-data/results/$test_name/instruments/disk_avg_stats.csv ~/PAT/PAT-collecting-data/results/bb300-4node-$query_name/disk_stats/disk-avg-stats-$test_name.csv
	cp ~/PAT/PAT-collecting-data/results/$test_name/instruments/perf.csv ~/PAT/PAT-collecting-data/results/bb300-4node-$query_name/perf/perf-$test_name.csv
	cp ~/PAT/PAT-collecting-data/results/$test_name/instruments/cpu_stats.csv ~/PAT/PAT-collecting-data/results/bb300-4node-$query_name/cpu_stats/cpu-$test_name.csv

	#break
	cd ~/PAT/PAT-collecting-data/results
done

#cd ~/PAT/PAT-collecting-data
