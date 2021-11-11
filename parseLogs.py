#!/usr/bin/env python
import pandas as pd
import numpy as np
from datetime import datetime
import geoip2.database

day = datetime.today().weekday()+1 # saves current day (monday=0 & sunday=6)+1

# Add placeholder for days below
sshLog = open("/Users/admin/git/MSc_Project/SD_Project/ssh/Day1/sshD1.log",'r').read().split("\n")
telnetLog = open("/Users/admin/git/MSc_Project/SD_Project/telnet/Day1/telnetD1.log",'r').read().split("\n")
# httpLog = open("/Users/admin/git/MSc_Project/SD_Project/http/Day1/httpD1.log",'r').read().split("\n")
# httpsLog = open("/Users/admin/git/MSc_Project/SD_Project/https/Day1/httpsD1.log",'r').read().split("\n")

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

# def parseToCsv(ssh_table, telnet_table, http_table, https_table):
# 	ssh_table.to_csv(f"/ssh/Day{day}/sshD{day}.csv", index=False) #index false to remove index or first column of data set
# 	#ssh_table.to_csv(f"/telnet/Day{day}/telnetD{day}.csv", index=False)
# 	#ssh_table.to_csv(f"/http/Day{day}/httpD{day}.csv", index=False)
# 	#ssh_table.to_csv(f"/https/Day{day}/httpsD{day}.csv", index=False)


class Ssh():

	def __init__(self, sshLog):
		self.sshLog = sshLog

	# 11 lists
	ssh_ips = []
	ssh_timestamps = []
	ssh_urls = []
	ssh_commands = []
	ssh_usernames = []
	ssh_passwords = []
	ssh_countries = []
	ssh_provinces = []
	ssh_cities = []
	ssh_longs = []
	ssh_lats = []

	connection_count = 0
	credentials_count = 0
	urls_count = 0
	commands_count = 0

	def parse(self):
		# Code for parsing sshLog to csv
		for line in sshLog:
			if "New connection" in line:
				var = line.split(" - ")
				# Create datetime object and append to timestamp list
				self.ssh_timestamps.append(datetime.strptime(var[0], "%Y-%m-%d %H:%M:%S,%f"))
				# format ip address and add to list
				self.ssh_ips.append(var[-1].replace("New connection from: ", ""))
				self.connection_count += 1

			elif "new client credentials" in line:
				var = line.split("): ")
				var2 = var[-1].replace("username: ", "")
				var3 = var2.replace("password: ", "")
				var4 = var3.split(",")
				self.ssh_usernames.append(var4[0])
				self.ssh_passwords.append(var4[1].replace(" ", ""))
				self.credentials_count += 1

			elif "URL detected" in line:
				var = line.split(": ")
				self.ssh_urls.append(var[-1])
				self.urls_count += 1

			elif "client sent command via check_channel_exec_request" in line:
				var = line.split(": ")
				self.ssh_commands.append(var[-1])
				self.commands_count += 1

		print("\nTotal number of connectons: " + str(self.connection_count) + "\n"
			  + "Total number of credentials tried: " + str(self.credentials_count) + "\n"
			  + "Total number of urls: " + str(self.urls_count) + "\n"
			  + "Total number of commands: " + str(self.commands_count) + "\n")

		# Code used to find the location of an IP Address
		ip_reader = geoip2.database.Reader(
			'/Users/admin/git/MSc_Project/SD_Project/GeoLite2-City_20211102/GeoLite2-City.mmdb')

		for ip in self.ssh_ips:
			response = ip_reader.city(ip)
			self.ssh_countries.append(response.country.name)
			self.ssh_provinces.append(response.subdivisions.most_specific.name)
			self.ssh_cities.append(response.city.name)
			self.ssh_longs.append(response.location.latitude)
			self.ssh_lats.append(response.location.longitude)

		# Find max column size
		max_col = 0
		if max_col < len(self.ssh_ips):
			max_col = len(self.ssh_ips)
		if max_col < len(self.ssh_urls):
			max_col = len(self.ssh_urls)
		if max_col < len(self.ssh_commands):
			max_col = len(self.ssh_commands)
		if max_col < len(self.ssh_usernames):
			max_col = len(self.ssh_usernames)
		if max_col < len(self.ssh_passwords):
			max_col = len(self.ssh_passwords)

		# Difference between each column and max size
		dif_ips = max_col - len(self.ssh_ips)
		dif_urls = max_col - len(self.ssh_urls)
		dif_commands = max_col - len(self.ssh_commands)
		dif_credentials_u = max_col - len(self.ssh_usernames)
		dif_credentials_p = max_col - len(self.ssh_passwords)

		# Append none to each list to make size consistent
		for x in range(dif_ips):
			self.ssh_ips.append(np.nan)
			self.ssh_timestamps.append(np.nan)
			self.ssh_countries.append(np.nan)
			self.ssh_provinces.append(np.nan)
			self.ssh_cities.append(np.nan)
			self.ssh_longs.append(np.nan)
			self.ssh_lats.append(np.nan)
		for x in range(dif_urls):
			self.ssh_urls.append(np.nan)
		for x in range(dif_commands):
			self.ssh_commands.append(np.nan)
		for x in range(dif_credentials_u):
			self.ssh_usernames.append(np.nan)
		for x in range(dif_credentials_p):
			self.ssh_passwords.append(np.nan)

		print(len(self.ssh_ips))
		print(len(self.ssh_timestamps))
		print(len(self.ssh_countries))
		print(len(self.ssh_provinces))
		print(len(self.ssh_cities))
		print(len(self.ssh_longs))
		print(len(self.ssh_lats))
		print(len(self.ssh_urls))
		print(len(self.ssh_commands))
		print(len(self.ssh_usernames))
		print(len(self.ssh_passwords))

		# Add data to dictionary
		ssh_dict = {
			column1: self.ssh_ips,
			column2: self.ssh_timestamps,
			column3: self.ssh_urls,
			column4: self.ssh_commands,
			column5: self.ssh_usernames,
			column6: self.ssh_passwords,
			column7: self.ssh_countries,
			column8: self.ssh_provinces,
			column9: self.ssh_cities,
			column10: self.ssh_longs,
			column11: self.ssh_lats
		}

		ssh_table = pd.DataFrame(ssh_dict)
		print(ssh_table)


class Telnet():

	def __init__(self, telnetLog):
		self.telnetLog = telnetLog

	# 11 lists
	ssh_ips = []
	ssh_timestamps = []
	ssh_urls = []
	ssh_commands = []
	ssh_usernames = []
	ssh_passwords = []
	ssh_countries = []
	ssh_provinces = []
	ssh_cities = []
	ssh_longs = []
	ssh_lats = []

	connection_count = 0
	credentials_count = 0
	urls_count = 0
	commands_count = 0

	def parse(self):
		# Code for parsing sshLog to csv
		for line in self.telnetLog:
			if "New connection" in line:
				var = line.split(" - ")
				# Create datetime object and append to timestamp list
				self.ssh_timestamps.append(datetime.strptime(var[0], "%Y-%m-%d %H:%M:%S,%f"))
				# format ip address and add to list
				self.ssh_ips.append(var[-1].replace("New connection from: ", ""))
				self.connection_count += 1

			elif "new client credentials" in line:
				var = line.split("): ")
				var2 = var[-1].replace("username: ", "")
				var3 = var2.replace("password: ", "")
				var4 = var3.split(",")
				self.ssh_usernames.append(var4[0])
				self.ssh_passwords.append(var4[1].replace(" ", ""))
				self.credentials_count += 1

			elif "URL detected" in line:
				var = line.split(": ")
				self.ssh_urls.append(var[-1])
				self.urls_count += 1

			elif "client sent command via check_channel_exec_request" in line:
				var = line.split(": ")
				self.ssh_commands.append(var[-1])
				self.commands_count += 1

		print("\nTotal number of connectons: " + str(self.connection_count) + "\n"
			  + "Total number of credentials tried: " + str(self.credentials_count) + "\n"
			  + "Total number of urls: " + str(self.urls_count) + "\n"
			  + "Total number of commands: " + str(self.commands_count) + "\n")

		# Code used to find the location of an IP Address
		ip_reader = geoip2.database.Reader(
			'/Users/admin/git/MSc_Project/SD_Project/GeoLite2-City_20211102/GeoLite2-City.mmdb')

		for ip in self.ssh_ips:
			response = ip_reader.city(ip)
			self.ssh_countries.append(response.country.name)
			self.ssh_provinces.append(response.subdivisions.most_specific.name)
			self.ssh_cities.append(response.city.name)
			self.ssh_longs.append(response.location.latitude)
			self.ssh_lats.append(response.location.longitude)

		# Find max column size
		max_col = 0
		if max_col < len(self.ssh_ips):
			max_col = len(self.ssh_ips)
		if max_col < len(self.ssh_urls):
			max_col = len(self.ssh_urls)
		if max_col < len(self.ssh_commands):
			max_col = len(self.ssh_commands)
		if max_col < len(self.ssh_usernames):
			max_col = len(self.ssh_usernames)
		if max_col < len(self.ssh_passwords):
			max_col = len(self.ssh_passwords)

		# Difference between each column and max size
		dif_ips = max_col - len(self.ssh_ips)
		dif_urls = max_col - len(self.ssh_urls)
		dif_commands = max_col - len(self.ssh_commands)
		dif_credentials_u = max_col - len(self.ssh_usernames)
		dif_credentials_p = max_col - len(self.ssh_passwords)

		# Append none to each list to make size consistent
		for x in range(dif_ips):
			self.ssh_ips.append(np.nan)
			self.ssh_timestamps.append(np.nan)
			self.ssh_countries.append(np.nan)
			self.ssh_provinces.append(np.nan)
			self.ssh_cities.append(np.nan)
			self.ssh_longs.append(np.nan)
			self.ssh_lats.append(np.nan)
		for x in range(dif_urls):
			self.ssh_urls.append(np.nan)
		for x in range(dif_commands):
			self.ssh_commands.append(np.nan)
		for x in range(dif_credentials_u):
			self.ssh_usernames.append(np.nan)
		for x in range(dif_credentials_p):
			self.ssh_passwords.append(np.nan)

		print(len(self.ssh_ips))
		print(len(self.ssh_timestamps))
		print(len(self.ssh_countries))
		print(len(self.ssh_provinces))
		print(len(self.ssh_cities))
		print(len(self.ssh_longs))
		print(len(self.ssh_lats))
		print(len(self.ssh_urls))
		print(len(self.ssh_commands))
		print(len(self.ssh_usernames))
		print(len(self.ssh_passwords))

		# Add data to dictionary
		ssh_dict = {
			column1: self.ssh_ips,
			column2: self.ssh_timestamps,
			column3: self.ssh_urls,
			column4: self.ssh_commands,
			column5: self.ssh_usernames,
			column6: self.ssh_passwords,
			column7: self.ssh_countries,
			column8: self.ssh_provinces,
			column9: self.ssh_cities,
			column10: self.ssh_longs,
			column11: self.ssh_lats
		}

		ssh_table = pd.DataFrame(ssh_dict)
		print(ssh_table)


if __name__ == "__main__":
	# Ssh(sshLog).parse()
	Telnet(telnetLog).parse()
	# HTTP()
	# HTTPS()