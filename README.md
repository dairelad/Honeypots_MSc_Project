# MSc in Software Development Project at the University of Glasgow 2021

- The project code is made up of
  - 8 honeypots (mimic the SSH, Telnet, HTTP and HTTPs services, 4 secure and 4 non-secure)
  - parsing scripts
  - shell scripts for running inside Docker
  - front-end dashboard developed in Python

- Four honeypots are not secure (1 SSH, 1 Telnet, 1 HTTP, 1 HTTPS) and accept incomming connections from anywhere.

- Three honeypots (1 Telnet, 1 HTTP, 1 HTTPS) use geo-ip blocking to stop connections from outside of the UK.
- One final SSH honeypot is configured using fail2ban (blocks IP after X number of failed logins). A parser is used on the fail2ban logs at /var/log/fail2ban.log and updates the dashboard appropriately, there is no code for this honeypot in the files as the rate-limited tool is configured on the server itself.

- The two honeypot folders contain code that should be run on separate cloud instances using Docker.

- The honeypots send parsed data to the dashboard using SFTP every 10 minutes.

- When running this project firewall rules should be edited appropriately to ensure that the honeypots and dashboard can be seen from the web.
