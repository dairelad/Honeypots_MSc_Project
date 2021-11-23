#!/bin/bash
echo "Running..."
sudo pkill -F /usr/src/app/pid.pid
sudo python /usr/src/app/index.py &
echo $! > /usr/src/app/pid.pid