#!/bin/bash


cd ~/PAT/PAT-collecting-data/results/crailterasort400GB
mkdir -p /home/ubuntu/PAT/PAT-collecting-data/results/crailterasort400GB
mkdir -p /home/ubuntu/PAT/PAT-collecting-data/results/crailterasort400GB/pdf
mkdir -p /home/ubuntu/PAT/PAT-collecting-data/results/crailterasort400GB/disk_stats


#for test_name in bigbench-$query_name-*
#for test_name in vanilla*-crailterasort400GB*
for test_name in vanilla-spark-i3.xl-8node-HDD500GB-nvme-crailterasort400GB-8exec-4cores-24GBexecmem
do
	echo $test_name
	cd ~/PAT/PAT-post-processing
	if [[ ($test_name == *"HDD"*) || ($test_name == *"hdd"*) ]] ; then
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
	sed -i "97s/if \"[a-z 0-9]*\" in/if \"${disk1}\" in/" disk_module.py
	sed -i "105s/elif \"[a-z 0-9]*\" in/elif \"${disk2}\" in/" disk_module.py

	#sed -i "55s/.*/\t<source>\/home\/ubuntu\/PAT\/PAT-collecting-data\/results\/${test_name}\/instruments<\/source>/" config.xml
	sed -i "55s/.*/\t<source>\/home\/ubuntu\/PAT\/PAT-collecting-data\/results\/crailterasort400GB\/${query_name}\/${test_name}\/instruments<\/source>/" config.xml
	./pat-post-process.py
	cp /home/ubuntu/PAT/PAT-collecting-data/results/crailterasort400GB/$test_name/instruments/PAT-Result.pdf /home/ubuntu/PAT/PAT-collecting-data/results/crailterasort400GB/$test_name/instruments/PAT-$test_name-postproc.pdf
	cp /home/ubuntu/PAT/PAT-collecting-data/results/crailterasort400GB/$test_name/instruments/disk_avg_stats.csv /home/ubuntu/PAT/PAT-collecting-data/results/crailterasort400GB/$test_name/instruments/disk-avg-stats-$test_name.csv
	cp /home/ubuntu/PAT/PAT-collecting-data/results/crailterasort400GB/$test_name/instruments/PAT-Result.pdf /home/ubuntu/PAT/PAT-collecting-data/results/crailterasort400GB/$query_name/pdf/PAT-$test_name-postproc.pdf
	cp /home/ubuntu/PAT/PAT-collecting-data/results/crailterasort400GB/$test_name/instruments/disk_avg_stats.csv /home/ubuntu/PAT/PAT-collecting-data/results/crailterasort400GB/$query_name/disk_stats/disk-avg-stats-$test_name.csv

	#break
	cd ~/PAT/PAT-collecting-data/results/crailterasort400GB
done

#cd ~/PAT/PAT-collecting-data