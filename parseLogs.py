#!/usr/bin/env python
import pandas as pd
import numpy as np
import datetime
import geoip2.database
import os

#day = datetime.datetime.today().weekday()+1 # saves current day (monday=0 & sunday=6)+1
day = 4

#Create folders for seperate days
path = os.getcwd()
if not os.path.exists('csv/Aggregate'):
	os.mkdir('csv/Aggregate')
	os.mkdir('csv/Summary')

# Open log files
sshLog = open(f"/Users/admin/git/MSc_Project/SD_Project/ssh/Day{day}/sshD{day}.log",'r').read().split("\n")
telnetLog = open(f"/Users/admin/git/MSc_Project/SD_Project/telnet/Day{day}/telnetD{day}.log",'r').read().split("\n")
httpLog = open(f"/Users/admin/git/MSc_Project/SD_Project/http/Day{day}/httpD{day}.log",'r').read().split("\n")
httpsLog = open(f"/Users/admin/git/MSc_Project/SD_Project/https/Day{day}/httpsD{day}.log",'r').read().split("\n")

# Code used to find the location of an IP Address
ip_reader = geoip2.database.Reader(
		'/Users/admin/git/MSc_Project/SD_Project/GeoLite2-City_20211102/GeoLite2-City.mmdb')

# columns for the different tables
column1 = "timestamp"
column2 = "ip"
column3 = "url"
column4 = "commands"
column5 = "usernames"
column6 = "passwords"
column7 = 'country'
column8 = 'province'
column9 = 'city'
column10 = 'long'
column11 = 'lat'
column12 = '# connections'
column13 = '# credentials'
column14 = '# commands'
column15 = '# urls'

# Summary updates once a day
start = datetime.time(13, 50, 0)
end = datetime.time(15, 35, 0)
now = datetime.datetime.now()
hr = int(now.strftime("%H"))
min = int(now.strftime("%M"))
sec = int(now.strftime("%S"))
now = datetime.time(hr,min,sec)

def time_in_range(start, end, x):
	"""Return true if x is in the range [start, end]"""
	if start <= end:
		return start <= x <= end
	else:
		return start <= x or x <= end


def parseLogsToCsv(ssh, telnet, http, https):
		ssh.to_csv(f"/Users/admin/git/MSc_Project/SD_Project/csv/Day{day}/sshD{day}.csv", index=False) #index false to remove index or first column of data set
		telnet.to_csv(f"/Users/admin/git/MSc_Project/SD_Project/csv/Day{day}/telnetD{day}.csv", index=False)
		http.to_csv(f"/Users/admin/git/MSc_Project/SD_Project/csv/Day{day}/httpD{day}.csv", index=False)
		https.to_csv(f"/Users/admin/git/MSc_Project/SD_Project/csv/Day{day}/httpsD{day}.csv", index=False)


def parseSumsToCsv(ssh, telnet, http, https):
	if time_in_range(start,end,now):
		# if file does not exist write header
		if not os.path.isfile('/Users/admin/git/MSc_Project/SD_Project/csv/Summary/sshSum.csv'):
			ssh.to_csv('/Users/admin/git/MSc_Project/SD_Project/csv/Summary/sshSum.csv', index=False)
		else:  # else it exists so append without writing the header
			ssh.to_csv('/Users/admin/git/MSc_Project/SD_Project/csv/Summary/sshSum.csv', mode='a', header=False, index=False)
		if not os.path.isfile('/Users/admin/git/MSc_Project/SD_Project/csv/Summary/telnetSum.csv'):
			telnet.to_csv('/Users/admin/git/MSc_Project/SD_Project/csv/Summary/telnetSum.csv', index=False)
		else:
			telnet.to_csv('/Users/admin/git/MSc_Project/SD_Project/csv/Summary/telnetSum.csv', mode='a', header=False, index=False)
		if not os.path.isfile('/Users/admin/git/MSc_Project/SD_Project/csv/Summary/httpSum.csv'):
			http.to_csv('/Users/admin/git/MSc_Project/SD_Project/csv/Summary/httpSum.csv', index=False)
		else:
			http.to_csv('/Users/admin/git/MSc_Project/SD_Project/csv/Summary/httpSum.csv', mode='a', header=False, index=False)
		if not os.path.isfile('/Users/admin/git/MSc_Project/SD_Project/csv/Summary/httpsSum.csv'):
			https.to_csv('/Users/admin/git/MSc_Project/SD_Project/csv/Summary/httpsSum.csv', index=False)
		else:
			https.to_csv('/Users/admin/git/MSc_Project/SD_Project/csv/Summary/httpsSum.csv', mode='a', header=False, index=False)


def parseCsvToAgg(ssh, telnet, http, https):
	if time_in_range(start,end,now):
		# if file does not exist write header
		if not os.path.isfile('/Users/admin/git/MSc_Project/SD_Project/csv/Aggregate/sshAgg.csv'):
			ssh.to_csv('/Users/admin/git/MSc_Project/SD_Project/csv/Aggregate/sshAgg.csv', index=False)
		else:  # else it exists so append without writing the header
			ssh.to_csv('/Users/admin/git/MSc_Project/SD_Project/csv/Aggregate/sshAgg.csv', mode='a', header=False, index=False)
		if not os.path.isfile('/Users/admin/git/MSc_Project/SD_Project/csv/Aggregate/telnetAgg.csv'):
			telnet.to_csv('/Users/admin/git/MSc_Project/SD_Project/csv/Aggregate/telnetAgg.csv', index=False)
		else:
			telnet.to_csv('/Users/admin/git/MSc_Project/SD_Project/csv/Aggregate/telnetAgg.csv', mode='a', header=False, index=False)
		if not os.path.isfile('/Users/admin/git/MSc_Project/SD_Project/csv/Aggregate/httpAgg.csv'):
			http.to_csv('/Users/admin/git/MSc_Project/SD_Project/csv/Aggregate/httpAgg.csv', index=False)
		else:
			http.to_csv('/Users/admin/git/MSc_Project/SD_Project/csv/Aggregate/httpAgg.csv', mode='a', header=False, index=False)
		if not os.path.isfile('/Users/admin/git/MSc_Project/SD_Project/csv/Aggregate/httpsAgg.csv'):
			https.to_csv('/Users/admin/git/MSc_Project/SD_Project/csv/Aggregate/httpsAgg.csv', index=False)
		else:
			https.to_csv('/Users/admin/git/MSc_Project/SD_Project/csv/Aggregate/httpsAgg.csv', mode='a', header=False, index=False)


class Ssh():
	def __init__(self, sshLog, ip_reader):
		self.sshLog = sshLog
		self.ip_reader = ip_reader

	# lists
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
	ssh_sum1 = []
	ssh_sum2 = []
	ssh_sum3 = []
	ssh_sum4 = []

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
				self.ssh_timestamps.append(datetime.datetime.strptime(var[0], "%Y-%m-%d %H:%M:%S,%f"))
				# format ip address and add to list
				ip = var[-1].replace("New connection from: ", "")
				self.ssh_ips.append(ip)
				self.connection_count += 1

				# Append NaN to rest of values in row of table
				self.ssh_urls.append(np.nan)
				self.ssh_commands.append(np.nan)
				self.ssh_usernames.append(np.nan)
				self.ssh_passwords.append(np.nan)

				try:
					response = self.ip_reader.city(ip)
					self.ssh_countries.append(response.country.name)
					self.ssh_provinces.append(response.subdivisions.most_specific.name)
					self.ssh_cities.append(response.city.name)
					self.ssh_lats.append(response.location.latitude)
					self.ssh_longs.append(response.location.longitude)
				except Exception as e:
					print("Ip address not found in geoip2 db: " + ip)
					pass

			elif "New client credentials" in line:
				var = line.split(": user")
				var = var[-1].replace("name: ", "")
				var = var.replace("password: ", "")
				var = var.split(",")
				self.ssh_usernames.append(var[0])
				self.ssh_passwords.append(var[1].replace(" ", ""))
				self.credentials_count += 1
				#print(var[0] + ' ' + var[1])

				var = line.split(" - ")
				# Create datetime object and append to timestamp list
				self.ssh_timestamps.append(datetime.datetime.strptime(var[0], "%Y-%m-%d %H:%M:%S,%f"))
				# format ip address and add to list
				var = var[-1].split(":")
				ip = var[0].replace("New client credentials from ", "")
				self.ssh_ips.append(ip)

				# Append NaN to rest of values in row of table
				self.ssh_urls.append(np.nan)
				self.ssh_commands.append(np.nan)

				try:
					response = self.ip_reader.city(ip)
					self.ssh_countries.append(response.country.name)
					self.ssh_provinces.append(response.subdivisions.most_specific.name)
					self.ssh_cities.append(response.city.name)
					self.ssh_lats.append(response.location.latitude)
					self.ssh_longs.append(response.location.longitude)
				except Exception as e:
					print("Ip address not found in geoip2 db: " + ip)
					pass

			elif "URL detected" in line:
				var = line.split(": ")
				self.ssh_urls.append(var[-1])
				self.urls_count += 1

				var = line.split(" - ")
				# Create datetime object and append to timestamp list
				self.ssh_timestamps.append(datetime.datetime.strptime(var[0], "%Y-%m-%d %H:%M:%S,%f"))
				# format ip address and add to list
				var = var[-1].split(":")
				ip = var[0].replace("New URL detected from ", "")
				self.ssh_ips.append(ip)

				# Append NaN to rest of values in row of table
				self.ssh_usernames.append(np.nan)
				self.ssh_passwords.append(np.nan)
				self.ssh_commands.append(np.nan)

				try:
					response = self.ip_reader.city(ip)
					self.ssh_countries.append(response.country.name)
					self.ssh_provinces.append(response.subdivisions.most_specific.name)
					self.ssh_cities.append(response.city.name)
					self.ssh_lats.append(response.location.latitude)
					self.ssh_longs.append(response.location.longitude)
				except Exception as e:
					print("Ip address not found in geoip2 db: " + ip)
					pass

			elif "New command from" in line:
				var = line.split(": ")
				self.ssh_commands.append(var[-1])
				self.commands_count += 1

				var = line.split(" - ")
				# Create datetime object and append to timestamp list
				self.ssh_timestamps.append(datetime.datetime.strptime(var[0], "%Y-%m-%d %H:%M:%S,%f"))
				# format ip address and add to list
				var = var[-1].split(":")
				ip = var[0].replace("New command from ", "")
				self.ssh_ips.append(ip)

				# Append NaN to rest of values in row of table
				self.ssh_usernames.append(np.nan)
				self.ssh_passwords.append(np.nan)
				self.ssh_urls.append(np.nan)

				try:
					response = self.ip_reader.city(ip)
					self.ssh_countries.append(response.country.name)
					self.ssh_provinces.append(response.subdivisions.most_specific.name)
					self.ssh_cities.append(response.city.name)
					self.ssh_lats.append(response.location.latitude)
					self.ssh_longs.append(response.location.longitude)
				except Exception as e:
					print("Ip address not found in geoip2 db: " + ip)
					pass

		print("\nTotal number of connectons: " + str(self.connection_count) + "\n"
			  + "Total number of credentials tried: " + str(self.credentials_count) + "\n"
			  + "Total number of urls: " + str(self.urls_count) + "\n"
			  + "Total number of commands: " + str(self.commands_count) + "\n")

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
			column1: self.ssh_timestamps,
			column2: self.ssh_ips,
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

		self.ssh_sum1.append(self.connection_count)
		self.ssh_sum2.append(self.credentials_count)
		self.ssh_sum3.append(self.urls_count)
		self.ssh_sum4.append(self.commands_count)

		# Add data to dictionary
		sshSum_dict = {
			column12: self.ssh_sum1,
			column13: self.ssh_sum2,
			column14: self.ssh_sum3,
			column15: self.ssh_sum4
		}

		sshSum_table = pd.DataFrame(sshSum_dict)

		ssh_table = pd.DataFrame(ssh_dict)
		print(ssh_table)
		return ssh_table, sshSum_table

class Telnet():

	def __init__(self, telnetLog, ip_reader):
		self.telnetLog = telnetLog
		self.ip_reader = ip_reader

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
	telnet_sum1 = []
	telnet_sum2 = []
	telnet_sum3 = []

	connection_count = 0
	urls_count = 0
	commands_count = 0

	def parse(self):
		# Code for parsing sshLog to csv
		for line in self.telnetLog:
			if "New connection" in line:
				var = line.split(" - ")
				# Create datetime object and append to timestamp list
				self.telnet_timestamps.append(datetime.datetime.strptime(var[0], "%Y-%m-%d %H:%M:%S,%f"))
				# format ip address and add to list
				ip = var[-1].replace("New connection from: ", "")
				self.telnet_ips.append(ip)
				self.connection_count += 1

				try:
					response = ip_reader.city(ip)
					self.telnet_countries.append(response.country.name)
					self.telnet_provinces.append(response.subdivisions.most_specific.name)
					self.telnet_cities.append(response.city.name)
					self.telnet_lats.append(response.location.latitude)
					self.telnet_longs.append(response.location.longitude)
				except Exception as e:
					print("Ip address not found in geoip2 db: " + ip)
					pass

			elif "URL detected" in line:
				var = line.split(": ")
				self.telnet_urls.append(var[-1])
				self.urls_count += 1

				var = line.split(" - ")
				# Create datetime object and append to timestamp list
				self.telnet_timestamps.append(datetime.datetime.strptime(var[0], "%Y-%m-%d %H:%M:%S,%f"))
				# format ip address and add to list
				var = var[-1].split(":")
				ip = var[0].replace("New URL detected from ", "")
				self.telnet_ips.append(ip)

				# Append NaN to rest of values in row of table
				self.telnet_commands.append(np.nan)


				try:
					response = self.ip_reader.city(ip)
					self.telnet_countries.append(response.country.name)
					self.telnet_provinces.append(response.subdivisions.most_specific.name)
					self.telnet_cities.append(response.city.name)
					self.telnet_lats.append(response.location.latitude)
					self.telnet_longs.append(response.location.longitude)
				except Exception as e:
					print("Ip address not found in geoip2 db: " + ip)
					pass

			elif "New command from" in line:
				var = line.split(": ")
				self.telnet_commands.append(var[-1])
				self.commands_count += 1

				var = line.split(" - ")
				# Create datetime object and append to timestamp list
				self.telnet_timestamps.append(datetime.datetime.strptime(var[0], "%Y-%m-%d %H:%M:%S,%f"))
				# format ip address and add to list
				var = var[-1].split(":")
				ip = var[0].replace("New command from ", "")
				self.telnet_ips.append(ip)

				# Append NaN to rest of values in row of table
				self.telnet_urls.append(np.nan)

				try:
					response = self.ip_reader.city(ip)
					self.telnet_countries.append(response.country.name)
					self.telnet_provinces.append(response.subdivisions.most_specific.name)
					self.telnet_cities.append(response.city.name)
					self.telnet_longs.append(response.location.longitude)
					self.telnet_lats.append(response.location.latitude)
				except Exception as e:
					print("Ip address not found in geoip2 db: " + ip)
					pass

		print("\nTotal number of connectons: " + str(self.connection_count) + "\n"
			  + "Total number of urls: " + str(self.urls_count) + "\n"
			  + "Total number of commands: " + str(self.commands_count) + "\n")

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
			column1: self.telnet_timestamps,
			column2: self.telnet_ips,
			column3: self.telnet_urls,
			column4: self.telnet_commands,
			column7: self.telnet_countries,
			column8: self.telnet_provinces,
			column9: self.telnet_cities,
			column10: self.telnet_longs,
			column11: self.telnet_lats
		}

		self.telnet_sum1.append(self.connection_count)
		self.telnet_sum2.append(self.commands_count)
		self.telnet_sum3.append(self.urls_count)

		# Add data to dictionary
		telnetSum_dict = {
			column12: self.telnet_sum1,
			column14: self.telnet_sum2,
			column15: self.telnet_sum3,
		}

		telnetSum_table = pd.DataFrame(telnetSum_dict)

		telnet_table = pd.DataFrame(telnet_dict)
		print(telnet_table)
		return telnet_table , telnetSum_table

class Http_s():

	def __init__(self, httpLog, httpsLog, ip_reader):
		self.httpLog = httpLog
		self.httpsLog = httpsLog
		self.ip_reader = ip_reader

	# lists
	http_ips = []
	http_timestamps = []
	http_countries = []
	http_provinces = []
	http_cities = []
	http_longs = []
	http_lats = []
	http_sum = []

	https_ips = []
	https_timestamps = []
	https_countries = []
	https_provinces = []
	https_cities = []
	https_longs = []
	https_lats = []
	https_sum = []

	connection_count1 = 0
	connection_count2 = 0

	def parse(self):
		# Code for parsing httpLog to dataframe
		for line in self.httpLog:
			if "New connection" in line:
				var = line.split(" - ")
				# Create datetime object and append to timestamp list
				self.http_timestamps.append(datetime.datetime.strptime(var[0], "%Y-%m-%d %H:%M:%S,%f"))
				# format ip address and add to list
				ip = var[-1].replace("New connection from: ", "")
				self.http_ips.append(ip)
				self.connection_count1 += 1

				try:
					response = ip_reader.city(ip)
					self.http_countries.append(response.country.name)
					self.http_provinces.append(response.subdivisions.most_specific.name)
					self.http_cities.append(response.city.name)
					self.http_longs.append(response.location.longitude)
					self.http_lats.append(response.location.latitude)
				except Exception as e:
					print("Ip address not found in geoip2 db: " + ip)
					self.http_countries.append(np.nan)
					self.http_provinces.append(np.nan)
					self.http_cities.append(np.nan)
					self.http_longs.append(np.nan)
					self.http_lats.append(np.nan)
					pass

		# Code for parsing httpsLog to dataframe
		for line in self.httpsLog:
			if "New connection" in line:
				var = line.split(" - ")
				# Create datetime object and append to timestamp list
				self.https_timestamps.append(datetime.datetime.strptime(var[0], "%Y-%m-%d %H:%M:%S,%f"))
				# format ip address and add to list
				ip = var[-1].replace("New connection from: ", "")
				self.https_ips.append(ip)
				self.connection_count2 += 1

				try:
					response = ip_reader.city(ip)
					self.https_countries.append(response.country.name)
					self.https_provinces.append(response.subdivisions.most_specific.name)
					self.https_cities.append(response.city.name)
					self.https_longs.append(response.location.longitude)
					self.https_lats.append(response.location.latitude)
				except Exception as e:
					print("Ip address not found in geoip2 db: " + ip)
					self.https_countries.append(np.nan)
					self.https_provinces.append(np.nan)
					self.https_cities.append(np.nan)
					self.https_longs.append(np.nan)
					self.https_lats.append(np.nan)
					pass

		# Add data to dictionary
		http_dict = {
			column1: self.http_timestamps,
			column2: self.http_ips,
			column7: self.http_countries,
			column8: self.http_provinces,
			column9: self.http_cities,
			column10: self.http_longs,
			column11: self.http_lats
		}

		# Add data to dictionary
		https_dict = {
			column1: self.https_timestamps,
			column2: self.https_ips,
			column7: self.https_countries,
			column8: self.https_provinces,
			column9: self.https_cities,
			column10: self.https_longs,
			column11: self.https_lats
		}

		self.http_sum.append(self.connection_count1)
		self.https_sum.append(self.connection_count2)

		# Add data to dictionary
		httpSum_dict = {
			column12: self.http_sum,
		}

		# Add data to dictionary
		httpsSum_dict = {
			column12: self.https_sum,
		}

		httpSum_table = pd.DataFrame(httpSum_dict)
		httpsSum_table = pd.DataFrame(httpsSum_dict)

		http_table = pd.DataFrame(http_dict)
		print(http_table)
		https_table = pd.DataFrame(https_dict)
		print(https_table)

		return http_table, httpSum_table, https_table, httpsSum_table

if __name__ == "__main__":
	ssh_list = Ssh(sshLog, ip_reader).parse()
	telnet_list = Telnet(telnetLog, ip_reader).parse()
	http_s = Http_s(httpLog, httpsLog, ip_reader).parse()

	ssh_table = ssh_list[0]
	ssh_tableSum = ssh_list[1]

	telnet_table = telnet_list[0]
	telnet_tableSum = telnet_list[1]

	http_table = http_s[0]
	httpSum_table = http_s[1]
	https_table = http_s[2]
	httpsSum_table = http_s[3]

	parseLogsToCsv(ssh_table, telnet_table, http_table, https_table)

	parseSumsToCsv(ssh_tableSum, telnet_tableSum, httpSum_table, httpsSum_table)

	parseCsvToAgg(ssh_table, telnet_table, http_table, https_table)