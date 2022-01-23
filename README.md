# SD_Project
MSC in Software Development Project at the University of Glasgow 2021. 
GUID: 2591168o

The project code comprises of 7 honeypots, parsing scripts, shell scripts for running inside Docker and a front-end dashboard programmed in Python. 4 honeypots are non-secure and accept incomming connections from anywhere whereas 3 use geo-ip blocking to stop connections from outside of the UK. The honeypots mimic the SSH, Telnet, HTTP and HTTPs services. A final honeypot is configured using fail2ban, but the only code relating to this is the parser of the fail2ban logs at /var/log/fail2ban.log.

The two honeypot folders contain code that should be run on separate machines using Docker. The honeypots send parsed data to the dashboard using SFTP every 10 minutes. Dashboard IP address must be correct in sendFiles.py. Firewall rules should be edited appropriately to ensure that the honeypots and dashboard can be seen from the web.
