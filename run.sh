#!/bin/bash
python3 sshHp.py &
echo ssh scrit started
python3 telnetHp.py &
echo telnet script started
python3 httpHp.py &
echo http script started
python3 httpsHp.py &
echo https script started
wait