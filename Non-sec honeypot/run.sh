#!/bin/bash
python3 /usr/src/app/ssh/sshHp.py &
echo ssh scrit started
python3 /usr/src/app/telnet/telnetHp.py &
echo telnet script started
python3 /usr/src/app/http/httpHp.py &
echo http script started
python3 /usr/src/app/https/httpsHp.py &
echo https script started
cron
#tail -f /var/log/cron.log
echo cron has started
wait