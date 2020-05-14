#!/bin/bash
ps -ef | grep "[m]id.py" | awk '{print "kill -9", $2}' | sh ; python /home/mid/oled-i2c/poweroff.py ; /sbin/poweroff
