#!/usr/local/bin/env python
import paramiko

key = '2591168o'
# connect to client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='52.208.69.153', username='ubuntu', password=key, port=22)
sftp_client=ssh.open_sftp()
# send data
print('Sending files..')
sftp_client.put('usr/src/app/csv/Aggregate/httpAggSec.csv', '/home/ubuntu/frontend/csv/Aggregate/httpAggSec.csv')
sftp_client.put('usr/src/app/csv/Aggregate/httpsAggSec.csv', '/home/ubuntu/frontend/csv/Aggregate/httpsAggSec.csv')
sftp_client.put('usr/src/app/csv/Aggregate/sshAggSec.csv', '/home/ubuntu/frontend/csv/Aggregate/sshAggSec.csv')
sftp_client.put('usr/src/app/csv/Aggregate/telnetAggSec.csv', '/home/ubuntu/frontend/csv/Aggregate/telnetAggSec.csv')
sftp_client.put('usr/src/app/csv/Summary/httpsSumSec.csv', '/home/ubuntu/frontend/csv/Summary/httpsSumSec.csv')
sftp_client.put('usr/src/app/csv/Summary/httpSumSec.csv', '/home/ubuntu/frontend/csv/Summary/httpSumSec.csv')
sftp_client.put('usr/src/app/csv/Summary/sshSumSec.csv', '/home/ubuntu/frontend/csv/Summary/sshSumSec.csv')
sftp_client.put('usr/src/app/csv/Summary/telnetSumSec.csv', '/home/ubuntu/frontend/csv/Summary/telnetSumSec.csv')
# close connection
sftp_client.close()
ssh.close()
print('Files sent.')