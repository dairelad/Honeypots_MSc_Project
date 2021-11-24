#!/bin/bash
echo "Running..." >> /home/ubuntu/frontend/cron.log 2>&1
sudo pkill -F /home/ubuntu/frontend/pid.pid
sudo python3 /home/ubuntu/frontend/index.py &
echo $! > /home/ubuntu/frontend/pid.pid