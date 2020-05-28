#! /bin/bash

if [ -e /var/log/watchdog.atclient ]
then
    date1=$(cut -d ',' -f1 /var/log/watchdog.atclient)
else
    echo "n/a"
    exit 1
fi

date1=$(cut -d ',' -f1 /var/log/watchdog.atclient)
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