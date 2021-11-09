#!/usr/bin/env python
import pandas as pd
import numpy as np
from datetime import datetime
import geoip2.database

myfile = open("/Users/admin/git/SD_Project/frontend/myCode/SD_Project/ssh_honeypot.log",'r').read().split("\n")

# 11 columns
column1 = "ip"
column2 = "timestamp"
column3 = "url"
column4 = "commands"
column5 = "usernames"
column6 = "passwords"
column7 = 'country'
column8 = 'province'
column9 = 'city'
column10 = 'long'
column11 = 'lat'


# 11 lists
ips = []
timestamps = []
urls = []
commands = []
usernames = []
passwords = []
countries = []
provinces = []
cities = []
longs = []
lats = []

connection_count = 0
credentials_count = 0
urls_count = 0
commands_count = 0

for line in myfile:
	if "New connection" in line:
#		print(line)
		var = line.split(" - ")
		# Create datetime object and append to timestamp list
		timestamps.append(datetime.strptime(var[0],"%Y-%m-%d %H:%M:%S,%f"))
		# format ip address and add to list
		ips.append(var[-1].replace("New connection from: ",""))
		connection_count += 1

	elif "new client credentials" in line:
		var = line.split("): ")
		print(var)
		var2 = var[-1].replace("username: ", "")
		var3 = var2.replace("password: ", "")
		var4 = var3.split(",")
		usernames.append(var4[0])
		passwords.append(var4[1].replace(" ",""))
		credentials_count += 1

	elif "URL detected" in line:
#		print(line.split(": "))
		var = line.split(": ")
		urls.append(var[-1])
		urls_count += 1

	elif "client sent command via check_channel_exec_request" in line:
#		print(line)
		var = line.split(": ")
		commands.append(var[-1])
		commands_count += 1

print("\nTotal number of connectons: " + str(connection_count) + "\n"
	  + "Total number of credentials tried: " + str(credentials_count) + "\n"
	  + "Total number of urls: " + str(urls_count) + "\n"
	  + "Total number of commands: " + str(commands_count) + "\n")

# Code used to find the location of an IP Address
reader = geoip2.database.Reader('/Users/admin/git/SD_Project/frontend/myCode/SD_Project/GeoLite2-City_20211102/GeoLite2-City.mmdb')

for ip in ips:
	response = reader.city(ip)
	countries.append(response.country.name)
	provinces.append(response.subdivisions.most_specific.name)
	cities.append(response.city.name)
	longs.append(response.location.latitude)
	lats.append(response.location.longitude)

# Find max column size
max_col =  0
if max_col < len(ips):
	max_col = len(ips)
if max_col < len(urls):
	max_col = len(urls)
if max_col < len(commands):
	max_col = len(commands)
if max_col < len(usernames):
	max_col = len(usernames)
if max_col < len(passwords):
	max_col = len(passwords)

# Difference between each column and max size
dif_ips = max_col - len(ips)
dif_urls = max_col - len(urls)
dif_commands = max_col - len(commands)
dif_credentials_u = max_col - len(usernames)
dif_credentials_p = max_col - len(passwords)

# Append none to each list to make size consistent
for x in range(dif_ips):
	ips.append(np.nan)
for x in range(dif_urls):
	urls.append(np.nan)
for x in range(dif_commands):
	commands.append(np.nan)
for x in range(dif_credentials_u):
	usernames.append(np.nan)
for x in range(dif_credentials_p):
	passwords.append(np.nan)

# Add data to dictionary
dictionary = {
column1 : ips,
column2 : timestamps,
column3 : urls,
column4 : commands,
column5 : usernames,
column6 : passwords,
column7 : countries,
column8 : provinces,
column9 : cities,
column10 : longs,
column11 : lats
}

table = pd.DataFrame(dictionary)
print(table)

table.to_csv("ssh_log.csv", index=False) #index false to remove index or first column of data set
#print(df.groupby(['ip']).count())

