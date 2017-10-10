#!/bin/bash


cd ~/PAT/PAT-collecting-data/results/
mkdir -p ~/PAT/PAT-collecting-data/results/SQLequijoin16Mrows-4node
mkdir -p ~/PAT/PAT-collecting-data/results/SQLequijoin16Mrows-4node/pdf
mkdir -p ~/PAT/PAT-collecting-data/results/SQLequijoin16Mrows-4node/disk_stats
mkdir -p ~/PAT/PAT-collecting-data/results/SQLequijoin16Mrows-4node/perf
mkdir -p ~/PAT/PAT-collecting-data/results/SQLequijoin16Mrows-4node/cpu_stats


#for test_name in bigbench-$query_name-*
for test_name in SQLequijoin16M*4node*
#for test_name in vanilla-spark-i3.xl-8node-HDD500GB-nvme-SQLequijoin16Mrows-4node-8exec-4cores-24GBexecmem
do
	echo $test_name
	cd ~/PAT/PAT-post-processing
	if [[ ($test_name == *"HDD"*) || ($test_name == *"hdd"*) || ($test_name == *"hhd"*)  ]] ; then
		disk1="xvdd"
		#if [[ (($test_name == *"HDD"*) && ($test_name == *"SSD"*) || ($test_name == *"hdd"*) && ($test_name == *"ssd"*))  ]]; then
		if [[ ($test_name == *"SSD"*) || ($test_name == *"ssd"*)  ]]; then
			disk2="xvdc"
		elif [[ ($test_name == *"NVMe"*) || ($test_name == *"nvme"*)  ]]; then
			disk2="nvme"
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

	#sed -i "55s/.*/\t<source>\/home\/ubuntu\/PAT\/PAT-collecting-data\/results\/${test_name}\/instruments<\/source>/" config.xml
	sed -i "55s/.*/\t<source>\/home\/ubuntu\/PAT\/PAT-collecting-data\/results\/${test_name}\/instruments<\/source>/" config.xml
	./pat-post-process.py
	cp ~/PAT/PAT-collecting-data/results/$test_name/instruments/PAT-Result.pdf /home/ubuntu/PAT/PAT-collecting-data/results/$test_name/instruments/PAT-$test_name-postproc.pdf
	cp ~/PAT/PAT-collecting-data/results/$test_name/instruments/disk_avg_stats.csv /home/ubuntu/PAT/PAT-collecting-data/results/$test_name/instruments/disk-avg-stats-$test_name.csv
	cp ~/PAT/PAT-collecting-data/results/$test_name/instruments/perf.csv ~/PAT/PAT-collecting-data/results/$test_name/instruments/perf-$test_name.csv
	cp ~/PAT/PAT-collecting-data/results/$test_name/instruments/PAT-Result.pdf /home/ubuntu/PAT/PAT-collecting-data/results/SQLequijoin16Mrows-4node/pdf/PAT-$test_name-postproc.pdf
	cp ~/PAT/PAT-collecting-data/results/$test_name/instruments/disk_avg_stats.csv /home/ubuntu/PAT/PAT-collecting-data/results/SQLequijoin16Mrows-4node/disk_stats/disk-avg-stats-$test_name.csv
	cp ~/PAT/PAT-collecting-data/results/$test_name/instruments/perf.csv ~/PAT/PAT-collecting-data/results/SQLequijoin16Mrows-4node/perf/perf-$test_name.csv
	cp ~/PAT/PAT-collecting-data/results/$test_name/instruments/cpu_stats.csv ~/PAT/PAT-collecting-data/results/SQLequijoin16Mrows-4node/cpu_stats/cpu-$test_name.csv

	#break
	cd ~/PAT/PAT-collecting-data/results
done



#cd ~/PAT/PAT-collecting-data
