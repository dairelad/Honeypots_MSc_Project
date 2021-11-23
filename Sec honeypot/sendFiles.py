#!/usr/local/bin/env python
import paramiko

#key = open('/Users/admin/.ssh/MSc_project.pem').read()
key = '2591168o'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='34.240.31.21', username='ubuntu', password=key, port=22)
sftp_client=ssh.open_sftp()

print('Sending files..')
sftp_client.put('usr/src/app/csv/Aggregate/httpAgg.csv', '/home/ubuntu/frontend/csv/Aggregate/httpAgg.csv')
sftp_client.put('usr/src/app/csv/Aggregate/httpsAgg.csv', '/home/ubuntu/frontend/csv/Aggregate/httpsAgg.csv')
sftp_client.put('usr/src/app/csv/Aggregate/sshAgg.csv', '/home/ubuntu/frontend/csv/Aggregate/sshAgg.csv')
sftp_client.put('usr/src/app/csv/Aggregate/telnetAgg.csv', '/home/ubuntu/frontend/csv/Aggregate/telnetAgg.csv')
sftp_client.put('usr/src/app/csv/Summary/httpsSum.csv', '/home/ubuntu/frontend/csv/Summary/httpsSum.csv')
sftp_client.put('usr/src/app/csv/Summary/httpSum.csv', '/home/ubuntu/frontend/csv/Summary/httpSum.csv')
sftp_client.put('usr/src/app/csv/Summary/sshSum.csv', '/home/ubuntu/frontend/csv/Summary/sshSum.csv')
sftp_client.put('usr/src/app/csv/Summary/telnetSum.csv', '/home/ubuntu/frontend/csv/Summary/telnetSum.csv')

sftp_client.close()
ssh.close()
print('Files sent.')