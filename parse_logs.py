#!/usr/bin/env python

# First select each line that is relevant
# Create a data frame using pandas

myfile = open("/Users/admin/git/SD_Project/backend/myCode/ssh_honeypot.log",'r').read().split("\n")

connection_count = 0
for line in myfile:
	if "New connection" in line:
		print(line.split(" - "))
		connection_count += 1

print("Total number of connectons: " + str(connection_count))




