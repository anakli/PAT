#!/bin/bash

cd ~/PAT/PAT-post-processing

FILE="tpcds-results-master1.csv"
touch $FILE

for i in {1..13} 15 {17..22} {24..99}
do
   #./post-proc-tpcds.sh q$i
   echo "processing tpds-q$i..."
   for disk_stat_name in ~/PAT/PAT-collecting-data/results/tpcds-q$i/disk_stats/disk-avg-stats-tpcds*
   do
      test_name=${disk_stat_name#*"disk-avg-stats-"}
      test_name=${test_name%".csv"}
      query_name=${test_name#*"tpcds-"}
      query_name=${query_name%"xl"*}
      query_name=${query_name%"-"*}

	  cpu_stat_name=${disk_stat_name%"disk_"*}"cpu_stats/cpu-"$test_name".csv" 

      echo $test_name
      if [[ ($disk_stat_name == *"HDD"*) || ($disk_stat_name == *"hdd"*) ]] ; then
      	disk1="hdd"
      	if [[ ($disk_stat_name == *"SSD"*) || ($disk_stat_name == *"ssd"*)  ]]; then
      		disk2="ssd"
      	else
      		disk2="hdd"
      	fi
      elif [[ ($disk_stat_name == *"SSD"*) || ($disk_stat_name == *"ssd"*) ]] ; then
      	disk1="ssd"
      	if [[ ($disk_stat_name == *"NVMe"*) || ($disk_stat_name == *"nvme"*)  ]]; then
      		disk2="nvme"
      	else
      		disk2="ssd"
      	fi
      else
      	disk1="nvme"
      	disk2="nvme"
      fi
      
      if [[ ($disk_stat_name == *"8xl"*) ]] ; then
      	num_cores=32
		ram=240
      elif [[ ($disk_stat_name == *"4xl"*) ]] ; then
      	num_cores=16
		ram=120
      elif [[ ($disk_stat_name == *"2xl"*) ]] ; then
      	num_cores=8
		ram=60
      elif [[ ($disk_stat_name == *"xl"*) ]] ; then
      	num_cores=4
		ram=30
      elif [[ ($disk_stat_name == *"xl"*) ]] ; then
      	num_cores=4
		ram=30
      elif [[ ($disk_stat_name == *"l-"*) ]] ; then
      	num_cores=2
		ram=15
      else
         num_cores=0
		 ram=0
      fi
      numeric_regex='^[0-9]+$'
	  # check if valid, otherwise skip this line
	  if ! [[ $num_cores =~ $numeric_regex ]] ; then
		  continue 
	  fi
	  #echo -n "$disk1, $disk2, $num_cores, $ram," >> $FILE
	  echo -n "$query_name, $num_cores, $ram, $disk1, $disk2, " >> $FILE
	  echo -n ", , , , , , , , , , , ," >> $FILE
	  if [ "$disk1" = "$disk2" ]; then
		  echo -n "0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0," >> $FILE
		  echo -n `cat $disk_stat_name` >> $FILE
		  echo -n "," >> $FILE
	  else
		  echo -n `cat $disk_stat_name` >> $FILE
		  echo -n ",0, 0, 0, 0, 0, 0," >> $FILE
	  fi 

	  echo -n `cat $cpu_stat_name` >> $FILE
	  echo -n "," >> $FILE

	  milisec=`cat ~/PAT/PAT-collecting-data/results/$test_name/jobhistory/stdout | grep "Execution time"  | awk '{ print $4 }'`
	  if ! [[ $milisec =~ $numeric_regex ]] ; then
		  echo -n "failed" >> $FILE
	  else
		  echo -n $(($milisec/1000)) >> $FILE
	  fi
	  echo ", $test_name" >> $FILE
   done
done

