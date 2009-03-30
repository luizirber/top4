#!/bin/bash

OUTPUT_DIR=run01
REPORT_TIME=1
TIMEOUT=30s

flags=('--cpu 1'
       '--cpu 2'
       '--cpu 5'
       '--cpu 10'
       '--hdd 1'
       '--hdd 2'
       '--hdd 5'
       '--hdd 10'
       '--vm 1 --vm-bytes 80MB'
       '--vm 2 --vm-bytes 80MB'
       '--vm 5 --vm-bytes 80MB'
       '--vm 10 --vm-bytes 80MB'
       '--cpu 1 --hdd 10'
       '--cpu 2 --hdd 5'
       '--cpu 5 --hdd 2'
       '--cpu 10 --hdd 1'
       '--cpu 10 --hdd 10')

dir=('01-cpu1'
     '02-cpu2'
     '03-cpu5'
     '04-cpu10'
     '05-hdd1'
     '06-hdd2'
     '07-hdd5'
     '08-hdd10'
     '09-vm1'
     '10-vm2'
     '11-vm5'
     '12-vm10'
     '13-cpu1-hdd10'
     '14-cpu2-hdd5'
     '15-cpu5-hdd2'
     '16-cpu10-hdd1'
     '17-cpu10-hdd10')

run_all_tests()
{
  x=0;
  while [ $x != ${#flags[@]} ]
  do
    mkdir -p $OUTPUT_DIR/${dir[$x]}
    iostat -k -t $REPORT_TIME > $OUTPUT_DIR/${dir[$x]}/ioreport &
    vmstat -a -n -S k $REPORT_TIME > $OUTPUT_DIR/${dir[$x]}/vmreport &
    pidstat -w -C stress $REPORT_TIME > $OUTPUT_DIR/${dir[$x]}/pidreport &
    mpstat -P ALL $REPORT_TIME > $OUTPUT_DIR/${dir[$x]}/mpreport &
    ./stress ${flags[$x]} --timeout $TIMEOUT > $OUTPUT_DIR/${dir[$x]}/stressreport &&\
    killall iostat &&\
    killall vmstat &&\
    killall pidstat &&\
    killall mpstat
    let "x = x + 1"
  done
}

run_all_tests

