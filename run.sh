#!/bin/bash

OUTPUT_DIR=run01
REPORT_TIME=5
TIMEOUT=3m

flags=('--cpu 1'
       '--cpu 2'
       '--cpu 5'
       '--cpu 10'
       '--io 1'
       '--io 2'
       '--io 5'
       '--io 10'
       '--vm 1 --vm-bytes 80MB'
       '--vm 2 --vm-bytes 80MB'
       '--vm 5 --vm-bytes 80MB'
       '--vm 10 --vm-bytes 80MB'
       '--cpu 1 --io 10'
       '--cpu 2 --io 5'
       '--cpu 5 --io 2'
       '--cpu 10 --io 1'
       '--cpu 10 --io 10')

dir=('01-cpu1'
     '02-cpu2'
     '03-cpu5'
     '04-cpu10'
     '05-io1'
     '06-io2'
     '07-io5'
     '08-io10'
     '09-vm1'
     '10-vm2'
     '11-vm5'
     '12-vm10'
     '13-cpu1-io10'
     '14-cpu2-io5'
     '15-cpu5-io2'
     '16-cpu10-io1'
     '17-cpu10-io10')

run_all_tests()
{
  x=0;
  while [ $x != ${#flags[@]} ]
  do
    mkdir -p $OUTPUT_DIR/${dir[$x]}
    iostat -k -t $REPORT_TIME > $OUTPUT_DIR/${dir[$x]}/ioreport &
    vmstat -a -n -S k $REPORT_TIME > $OUTPUT_DIR/${dir[$x]}/vmreport &
    mpstat -P ALL $REPORT_TIME > $OUTPUT_DIR/${dir[$x]}/mpreport &
    ./stress ${flags[$x]} --timeout $TIMEOUT > $OUTPUT_DIR/${dir[$x]}/stressreport &&\
    killall iostat &&\
    killall vmstat &&\
    killall mpstat
    let "x = x + 1"
  done
}

run_all_tests

