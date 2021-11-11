#!/usr/bin/env python
import pandas as pd
import numpy as np
from datetime import datetime
import geoip2.database

day = datetime.today().weekday()+1 # saves current day (monday=0 & sunday=6)+1

# Open log files
sshLog = open(f"/Users/admin/git/MSc_Project/SD_Project/ssh/Day{day}/sshD{day}.log",'r').read().split("\n")
telnetLog = open(f"/Users/admin/git/MSc_Project/SD_Project/telnet/Day{day}/telnetD{day}.log",'r').read().split("\n")
httpLog = open(f"/Users/admin/git/MSc_Project/SD_Project/http/Day{day}/httpD{day}.log",'r').read().split("\n")
httpsLog = open(f"/Users/admin/git/MSc_Project/SD_Project/https/Day{day}/httpsD{day}.log",'r').read().split("\n")

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

def parseToCsv(table, hp):
	if hp == 'ssh':
		table.to_csv(f"/Users/admin/git/MSc_Project/SD_Project/csv/Day{day}/sshD{day}.csv", index=False) #index false to remove index or first column of data set
	elif hp == 'telnet':
		table.to_csv(f"/Users/admin/git/MSc_Project/SD_Project/csv/Day{day}/telnetD{day}.csv", index=False)
	elif hp == 'http':
		table.to_csv(f"/Users/admin/git/MSc_Project/SD_Project/csv/Day{day}/httpD{day}.csv", index=False)
	elif hp == 'https':
		table.to_csv(f"/Users/admin/git/MSc_Project/SD_Project/csv/Day{day}/httpsD{day}.csv", index=False)


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

			elif "New command from" in line:
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
			try:
				response = ip_reader.city(ip)
				self.ssh_countries.append(response.country.name)
				self.ssh_provinces.append(response.subdivisions.most_specific.name)
				self.ssh_cities.append(response.city.name)
				self.ssh_longs.append(response.location.latitude)
				self.ssh_lats.append(response.location.longitude)
			except Exception as e:
				print("Ip address not found in geoip2 db: " + ip)
				pass

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
		dif_geoip = max_col - len(self.ssh_cities)

		# Append none to each list to make size consistent
		for x in range(dif_ips):
			self.ssh_ips.append(np.nan)
			self.ssh_timestamps.append(np.nan)
		for x in range(dif_urls):
			self.ssh_urls.append(np.nan)
		for x in range(dif_commands):
			self.ssh_commands.append(np.nan)
		for x in range(dif_credentials_u):
			self.ssh_usernames.append(np.nan)
		for x in range(dif_credentials_p):
			self.ssh_passwords.append(np.nan)
		for x in range(dif_geoip):
			self.ssh_countries.append(np.nan)
			self.ssh_provinces.append(np.nan)
			self.ssh_cities.append(np.nan)
			self.ssh_longs.append(np.nan)
			self.ssh_lats.append(np.nan)

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
		return ssh_table

class Telnet():

	def __init__(self, telnetLog):
		self.telnetLog = telnetLog

	# lists
	telnet_ips = []
	telnet_timestamps = []
	telnet_urls = []
	telnet_commands = []
	telnet_countries = []
	telnet_provinces = []
	telnet_cities = []
	telnet_longs = []
	telnet_lats = []

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
				self.telnet_timestamps.append(datetime.strptime(var[0], "%Y-%m-%d %H:%M:%S,%f"))
				# format ip address and add to list
				self.telnet_ips.append(var[-1].replace("New connection from: ", ""))
				self.connection_count += 1

			elif "URL detected" in line:
				var = line.split(": ")
				self.telnet_urls.append(var[-1])
				self.urls_count += 1

			elif "New command from" in line:
				var = line.split(": ")
				self.telnet_commands.append(var[-1])
				self.commands_count += 1

		print("\nTotal number of connectons: " + str(self.connection_count) + "\n"
			  + "Total number of credentials tried: " + str(self.credentials_count) + "\n"
			  + "Total number of urls: " + str(self.urls_count) + "\n"
			  + "Total number of commands: " + str(self.commands_count) + "\n")

		# Code used to find the location of an IP Address
		ip_reader = geoip2.database.Reader(
			'/Users/admin/git/MSc_Project/SD_Project/GeoLite2-City_20211102/GeoLite2-City.mmdb')

		for ip in self.telnet_ips:
			try:
				response = ip_reader.city(ip)
				self.telnet_countries.append(response.country.name)
				self.telnet_provinces.append(response.subdivisions.most_specific.name)
				self.telnet_cities.append(response.city.name)
				self.telnet_longs.append(response.location.latitude)
				self.telnet_lats.append(response.location.longitude)
			except Exception as e:
				print("Ip address not found in geoip2 db: " + ip)
				pass

		# Find max column size
		max_col = 0
		if max_col < len(self.telnet_ips):
			max_col = len(self.telnet_ips)
		if max_col < len(self.telnet_urls):
			max_col = len(self.telnet_urls)
		if max_col < len(self.telnet_commands):
			max_col = len(self.telnet_commands)

		# Difference between each column and max size
		dif_ips = max_col - len(self.telnet_ips)
		dif_urls = max_col - len(self.telnet_urls)
		dif_commands = max_col - len(self.telnet_commands)
		dif_geoip = max_col - len(self.telnet_cities)

		# Append none to each list to make size consistent
		for x in range(dif_ips):
			self.telnet_ips.append(np.nan)
			self.telnet_timestamps.append(np.nan)
		for x in range(dif_urls):
			self.telnet_urls.append(np.nan)
		for x in range(dif_commands):
			self.telnet_commands.append(np.nan)
		for x in range(dif_geoip):
			self.telnet_countries.append(np.nan)
			self.telnet_provinces.append(np.nan)
			self.telnet_cities.append(np.nan)
			self.telnet_longs.append(np.nan)
			self.telnet_lats.append(np.nan)

		# Add data to dictionary
		telnet_dict = {
			column1: self.telnet_ips,
			column2: self.telnet_timestamps,
			column3: self.telnet_urls,
			column4: self.telnet_commands,
			column7: self.telnet_countries,
			column8: self.telnet_provinces,
			column9: self.telnet_cities,
			column10: self.telnet_longs,
			column11: self.telnet_lats
		}

		telnet_table = pd.DataFrame(telnet_dict)
		print(telnet_table)
		return telnet_table

class Http_s():

	def __init__(self, httpLog, httpsLog):
		self.httpLog = httpLog
		self.httpsLog = httpsLog

	# lists
	http_ips = []
	http_timestamps = []
	http_countries = []
	http_provinces = []
	http_cities = []
	http_longs = []
	http_lats = []

	https_ips = []
	https_timestamps = []
	https_countries = []
	https_provinces = []
	https_cities = []
	https_longs = []
	https_lats = []

	connection_count1 = 0
	connection_count2 = 0

	def parse(self):
		# Code for parsing httpLog to dataframe
		for line in self.httpLog:
			if "New connection" in line:
				var = line.split(" - ")
				# Create datetime object and append to timestamp list
				self.http_timestamps.append(datetime.strptime(var[0], "%Y-%m-%d %H:%M:%S,%f"))
				# format ip address and add to list
				self.http_ips.append(var[-1].replace("New connection from: ", ""))
				self.connection_count1 += 1

				# Code used to find the location of an IP Address
		ip_reader = geoip2.database.Reader(
			'/Users/admin/git/MSc_Project/SD_Project/GeoLite2-City_20211102/GeoLite2-City.mmdb')

		for ip in self.http_ips:
			try:
				response = ip_reader.city(ip)
				self.http_countries.append(response.country.name)
				self.http_provinces.append(response.subdivisions.most_specific.name)
				self.http_cities.append(response.city.name)
				self.http_longs.append(response.location.latitude)
				self.http_lats.append(response.location.longitude)
			except Exception as e:
				print("Ip address not found in geoip2 db: " + ip)
				pass

		# Code for parsing httpsLog to dataframe
		for line in self.httpsLog:
			if "New connection" in line:
				var = line.split(" - ")
				# Create datetime object and append to timestamp list
				self.https_timestamps.append(datetime.strptime(var[0], "%Y-%m-%d %H:%M:%S,%f"))
				# format ip address and add to list
				self.https_ips.append(var[-1].replace("New connection from: ", ""))
				self.connection_count2 += 1

		for ip in self.https_ips:
			try:
				response = ip_reader.city(ip)
				self.https_countries.append(response.country.name)
				self.https_provinces.append(response.subdivisions.most_specific.name)
				self.https_cities.append(response.city.name)
				self.https_longs.append(response.location.latitude)
				self.https_lats.append(response.location.longitude)
			except Exception as e:
				print("Ip address not found in geoip2 db: " + ip)
				pass

		# Add data to dictionary
		http_dict = {
			column1: self.http_ips,
			column2: self.http_timestamps,
			column7: self.http_countries,
			column8: self.http_provinces,
			column9: self.http_cities,
			column10: self.http_longs,
			column11: self.http_lats
		}

		# Add data to dictionary
		https_dict = {
			column1: self.https_ips,
			column2: self.https_timestamps,
			column7: self.https_countries,
			column8: self.https_provinces,
			column9: self.https_cities,
			column10: self.https_longs,
			column11: self.https_lats
		}

		http_table = pd.DataFrame(http_dict)
		print(http_table)
		https_table = pd.DataFrame(https_dict)
		print(https_table)

		return http_table, https_table


if __name__ == "__main__":
	ssh_table = Ssh(sshLog).parse()
	telnet_table = Telnet(telnetLog).parse()
	http_s = Http_s(httpLog, httpsLog).parse()

	http_table = http_s[0]
	https_table = http_s[1]

	parseToCsv(ssh_table, 'ssh')
	parseToCsv(telnet_table, 'telnet')
	parseToCsv(http_table, 'http')
	parseToCsv(https_table,'https')

# Code to append one csv to another

	# with open('original.csv', 'r') as f1:
	# 	original = f1.read()
	#
	# with open('all.csv', 'a') as f2:
	# 	f2.write('\n')
	# 	f2.write(original)