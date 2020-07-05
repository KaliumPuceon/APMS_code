#! /bin/bash

echo "35" > /tmp/scale_reading.txt

socat 'pty,b115200,echo=0,link=/home/pi/testing/testTTY' 'exec:/home/pi/testing/data_generator.py,pty,b115200,echo=0'
