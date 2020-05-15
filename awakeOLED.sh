#!/bin/bash
if ! (ps -ef | grep -q "[m]id.py") ; then (python /home/mid/oled-i2c/mid.py 600 &) ; else echo "OLED is already on..." ; fi