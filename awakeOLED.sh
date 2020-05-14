#!/bin/bash
if ! (ps -ef | grep -q "[m]id.py") ; then (python /home/mid/oled-i2c/mid.py 30 &) ; else echo "already running..." ; fi
