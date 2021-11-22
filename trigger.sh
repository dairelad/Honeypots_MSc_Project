#!/bin/bash
cd /PYTHON_SCRIPT_ABSOLUTE_PATH/
echo 'test complete' >> /usr/src/app/test.txt
#/usr/local/bin/python3 parseLogs.py
python3 /usr/src/app/parseLogs.py >> /usr/src/app/test.txt
echo 'logs parsed' >> /usr/src/app/test.txt
#/usr/local/bin/python3 sendFiles.py
python3 /usr/src/app/sendFiles.py >> /usr/src/app/test.txt
echo 'files sent' >> /usr/src/app/test.txt
wait