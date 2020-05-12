#! /bin/bash

date1=$(cut -d ',' -f1 /home/mid/atclient/watchdog.atclient)
seconds1=$(date --date "$date1" +%s)

#echo "Last STK heartbeat: ${seconds1} seconds"

seconds2=$(date +%s)

#echo "Current date      : ${seconds2} seconds"

delta=$((seconds2 - seconds1))

#echo "Age               : ${delta} seconds"

if [[ "$delta" -lt 86400 ]]; then 
    echo "${delta}"
else
    echo ">1 day"
fi