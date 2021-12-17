#!/usr/local/bin/env python
import pandas as pd
import numpy as np
import datetime
import geoip2.database
import os
import sys

day = datetime.datetime.today().weekday() # saves current day (monday=0 & sunday=6)

#Create folders for csv files
path = os.getcwd()
if not os.path.exists('csv/Aggregate'):
	os.mkdir('csv')
	os.mkdir('csv/Aggregate')
	os.mkdir('csv/Summary')
	os.mkdir('csv/Day1')
	os.mkdir('csv/Day2')
	os.mkdir('csv/Day3')
	os.mkdir('csv/Day4')
	os.mkdir('csv/Day5')
	os.mkdir('csv/Day6')
	os.mkdir('csv/Day7')
	for x in range(7): # create csv files for containing daily data
		f = open(f"{path}/Day{x+1}/sshD{x+1}.csv", "x")
		f = open(f"{path}/Day{x+1}/telnetD{x+1}.csv", "x")
		f = open(f"{path}/Day{x+1}/httpD{x+1}.csv", "x")
		f = open(f"{path}/Day{x+1}/httpsD{x+1}.csv", "x")

try:
	# Read honeypot log files
	sshLog = open(f"/usr/src/app/Day{day+1}/sshD{day+1}.log",'r').read().split("\n")
	telnetLog = open(f"/usr/src/app/Day{day+1}/telnetD{day+1}.log",'r').read().split("\n")
	httpLog = open(f"/usr/src/app/Day{day+1}/httpD{day+1}.log",'r').read().split("\n")
	httpsLog = open(f"/usr/src/app/Day{day+1}/httpsD{day+1}.log",'r').read().split("\n")

	# Read in summary csvs so that the correct row (day) can be updated
	sshSumCsv = pd.read_csv("/usr/src/app/csv/Summary/sshSum.csv")
	telnetSumCsv = pd.read_csv("/usr/src/app/csv/Summary/telnetSum.csv")
	httpSumCsv = pd.read_csv("/usr/src/app/csv/Summary/httpSum.csv")
	httpsSumCsv = pd.read_csv("/usr/src/app/csv/Summary/httpsSum.csv")

	# Read number of current lines in aggregate files so they can be updated
	sshAggCsv = pd.read_csv("/usr/src/app/csv/Aggregate/sshAgg.csv")
	telnetAggCsv = pd.read_csv("/usr/src/app/csv/Aggregate/telnetAgg.csv")
	httpAggCsv = pd.read_csv("/usr/src/app/csv/Aggregate/httpAgg.csv")
	httpsAggCsv = pd.read_csv("/usr/src/app/csv/Aggregate/httpsAgg.csv")

except IOError:
	print('Could not open required files')
	sys.exit()

# load db for finding locations of IPs
ip_reader = geoip2.database.Reader(
		'/usr/src/app/GeoLite2-City_20211102/GeoLite2-City.mmdb')

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

# function logs daily data
# index false to remove index or first column of data set
def logsToCsv(ssh, telnet, http, https):
		ssh.to_csv(f"/usr/src/app/csv/Day{day+1}/sshD{day+1}.csv", index=False)
		telnet.to_csv(f"/usr/src/app/csv/Day{day+1}/telnetD{day+1}.csv", index=False)
		http.to_csv(f"/usr/src/app/csv/Day{day+1}/httpD{day+1}.csv", index=False)
		https.to_csv(f"/usr/src/app/csv/Day{day+1}/httpsD{day+1}.csv", index=False)


def sumToCsv(ssh, telnet, http, https):
	# if file does not exist write header
	if not os.path.isfile('/usr/src/app/csv/Summary/sshSum.csv'):
		ssh.to_csv('/usr/src/app/csv/Summary/sshSum.csv', index=False)
	else:  # else it exists so append without writing the header
		sshSumCsv.iloc[day,[0,1,2,3]] = ssh.iloc[0,[0,1,2,3]]
		sshSumCsv.to_csv('/usr/src/app/csv/Summary/sshSum.csv', index=False)
	if not os.path.isfile('/usr/src/app/csv/Summary/telnetSum.csv'):
		telnet.to_csv('/usr/src/app/csv/Summary/telnetSum.csv', index=False)
	else:
		telnetSumCsv.iloc[day, [0, 1, 2]] = telnet.iloc[0, [0, 1, 2]]
		telnetSumCsv.to_csv('/usr/src/app/csv/Summary/telnetSum.csv', index=False)
	if not os.path.isfile('/usr/src/app/csv/Summary/httpSum.csv'):
		http.to_csv('/usr/src/app/csv/Summary/httpSum.csv', index=False)
	else:
		httpSumCsv.iloc[day, [0]] = http.iloc[0, [0]]
		httpSumCsv.to_csv('/usr/src/app/csv/Summary/httpSum.csv', index=False)
	if not os.path.isfile('/usr/src/app/csv/Summary/httpsSum.csv'):
		https.to_csv('/usr/src/app/csv/Summary/httpsSum.csv', index=False)
	else:
		httpsSumCsv.iloc[day, [0]] = https.iloc[0, [0]]
		httpsSumCsv.to_csv('/usr/src/app/csv/Summary/httpsSum.csv', index=False)


def aggToCsv(ssh, telnet, http, https):
	# concatenate old data with new data
	ssh_parsed = pd.concat([sshAggCsv,ssh])
	telnet_parsed = pd.concat([telnetAggCsv, telnet])
	http_parsed = pd.concat([httpAggCsv, http])
	https_parsed = pd.concat([httpsAggCsv, https])
	# change timestamps from datetime object to strings so that duplicates can be removed
	ssh_parsed = ssh_parsed.astype(str)
	telnet_parsed = telnet_parsed.astype(str)
	http_parsed = http_parsed.astype(str)
	https_parsed = https_parsed.astype(str)
	# format timestamp column because changing to string added unnecessary 0's
	ssh_parsed['timestamp'] = ssh_parsed['timestamp'].str.slice(0,23)
	telnet_parsed['timestamp'] = telnet_parsed['timestamp'].str.slice(0, 23)
	http_parsed['timestamp'] = http_parsed['timestamp'].str.slice(0, 23)
	https_parsed['timestamp'] = https_parsed['timestamp'].str.slice(0, 23)
	# now that timestamps objects are string, duplicates are dropped
	ssh_parsed = ssh_parsed.drop_duplicates(subset = None, keep = "first", inplace = False)
	telnet_parsed = telnet_parsed.drop_duplicates(subset=None, keep="first", inplace=False)
	http_parsed = http_parsed.drop_duplicates(subset=None, keep="first", inplace=False)
	https_parsed = https_parsed.drop_duplicates(subset=None, keep="first", inplace=False)
	# replace empty values with NaN
	ssh_parsed['ip'].replace('', np.nan, inplace=True)
	telnet_parsed['ip'].replace('', np.nan, inplace=True)
	http_parsed['ip'].replace('', np.nan, inplace=True)
	https_parsed['ip'].replace('', np.nan, inplace=True)
	# drop rows which do not contain an ip address (caused if attacked enters some crazy input)
	ssh_parsed.dropna(subset=['ip'], inplace=True)
	telnet_parsed.dropna(subset=['ip'], inplace=True)
	http_parsed.dropna(subset=['ip'], inplace=True)
	https_parsed.dropna(subset=['ip'], inplace=True)
	# sort data
	ssh_parsed = ssh_parsed.sort_values(by=['timestamp'], ascending=True)
	telnet_parsed = telnet_parsed.sort_values(by=['timestamp'], ascending=True)
	http_parsed = http_parsed.sort_values(by=['timestamp'], ascending=True)
	https_parsed = https_parsed.sort_values(by=['timestamp'], ascending=True)

	# if file does not exist write header
	if not os.path.isfile('/usr/src/app/csv/Aggregate/sshAgg.csv'):
		ssh.to_csv('/usr/src/app/csv/Aggregate/sshAgg.csv', index=False)
	else:  # else it exists so append without writing the header
		ssh_parsed.to_csv('/usr/src/app/csv/Aggregate/sshAgg.csv', index=False)

	if not os.path.isfile('/usr/src/app/csv/Aggregate/telnetAgg.csv'):
		telnet.to_csv('/usr/src/app/csv/Aggregate/telnetAgg.csv', index=False)
	else:
		telnet_parsed.to_csv('/usr/src/app/csv/Aggregate/telnetAgg.csv', index=False)

	if not os.path.isfile('/usr/src/app/csv/Aggregate/httpAgg.csv'):
		http.to_csv('/usr/src/app/csv/Aggregate/httpAgg.csv', index=False)
	else:
		http_parsed.to_csv('/usr/src/app/csv/Aggregate/httpAgg.csv', index=False)

	if not os.path.isfile('/usr/src/app/csv/Aggregate/httpsAgg.csv'):
		https.to_csv('/usr/src/app/csv/Aggregate/httpsAgg.csv', index=False)
	else:
		https_parsed.to_csv('/usr/src/app/csv/Aggregate/httpsAgg.csv', index=False)


class Ssh():
	def __init__(self, sshLog, ip_reader):
		self.sshLog = sshLog
		self.ip_reader = ip_reader

	# lists
	ssh_ips = [], ssh_timestamps = [], ssh_urls = [], ssh_commands = [], ssh_usernames = [], ssh_passwords = []
	ssh_countries = [], ssh_provinces = [], ssh_cities = [], ssh_longs = [], ssh_lats = []
	ssh_sum1 = [], ssh_sum2 = [], ssh_sum3 = [], ssh_sum4 = []

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
					pass

			elif "New client credentials" in line:
				try:
					var = line.split(": user")
					var = var[-1].replace("name: ", "")
					var = var.replace("password: ", "")
					var = var.split(",")
					self.ssh_usernames.append(var[0])
					self.ssh_passwords.append(var[1].replace(" ", ""))
					self.credentials_count += 1

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
				except:
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
					self.ssh_passwords.append(np.nan)
					self.ssh_usernames.append(np.nan)

				try:
					response = self.ip_reader.city(ip)
					self.ssh_countries.append(response.country.name)
					self.ssh_provinces.append(response.subdivisions.most_specific.name)
					self.ssh_cities.append(response.city.name)
					self.ssh_lats.append(response.location.latitude)
					self.ssh_longs.append(response.location.longitude)
				except Exception as e:
					pass

			elif "URL detected" in line:
				try:
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
				except:
					pass

				try:
					response = self.ip_reader.city(ip)
					self.ssh_countries.append(response.country.name)
					self.ssh_provinces.append(response.subdivisions.most_specific.name)
					self.ssh_cities.append(response.city.name)
					self.ssh_lats.append(response.location.latitude)
					self.ssh_longs.append(response.location.longitude)
				except Exception as e:
					pass

			elif "New command from" in line:
				try:
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
				except:
					pass

				try:
					response = self.ip_reader.city(ip)
					self.ssh_countries.append(response.country.name)
					self.ssh_provinces.append(response.subdivisions.most_specific.name)
					self.ssh_cities.append(response.city.name)
					self.ssh_lats.append(response.location.latitude)
					self.ssh_longs.append(response.location.longitude)
				except Exception as e:
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
		ssh_table.drop(ssh_table.loc[ssh_table['ip']==''].index, inplace=True)#remove any blank rows (hackers feeding in junk)
		ssh_table =  ssh_table[:-1]# remove last row (hackers feeding in junk)

		return ssh_table, sshSum_table

class Telnet():

	def __init__(self, telnetLog, ip_reader):
		self.telnetLog = telnetLog
		self.ip_reader = ip_reader

	# lists
	telnet_ips = [], telnet_timestamps = [], telnet_urls = [], telnet_commands = []
	telnet_countries = [], telnet_provinces = [], telnet_cities = [], telnet_longs = [], telnet_lats = []
	telnet_sum1 = [], telnet_sum2 = [], telnet_sum3 = []

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
					pass

			elif "URL detected" in line:
				try:
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
				except:
					pass


				try:
					response = self.ip_reader.city(ip)
					self.telnet_countries.append(response.country.name)
					self.telnet_provinces.append(response.subdivisions.most_specific.name)
					self.telnet_cities.append(response.city.name)
					self.telnet_lats.append(response.location.latitude)
					self.telnet_longs.append(response.location.longitude)
				except Exception as e:
					pass

			elif "New command from" in line:
				try:
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
				except:
					pass

				try:
					response = self.ip_reader.city(ip)
					self.telnet_countries.append(response.country.name)
					self.telnet_provinces.append(response.subdivisions.most_specific.name)
					self.telnet_cities.append(response.city.name)
					self.telnet_longs.append(response.location.longitude)
					self.telnet_lats.append(response.location.latitude)
				except Exception as e:
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
		return telnet_table , telnetSum_table

class Http_s():

	def __init__(self, httpLog, httpsLog, ip_reader):
		self.httpLog = httpLog
		self.httpsLog = httpsLog
		self.ip_reader = ip_reader

	# lists
	http_ips = [], http_timestamps = []
	http_countries = [], http_provinces = [], http_cities = [], http_longs = [], http_lats = []
	http_sum = []

	https_ips = [], https_timestamps = []
	https_countries = [], https_provinces = [], https_cities = [], https_longs = [], https_lats = []
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
		https_table = pd.DataFrame(https_dict)

		return http_table, httpSum_table, https_table, httpsSum_table

if __name__ == "__main__":
	print('Parsing logs..')
	# parse logs for all honeypots
	ssh_list = Ssh(sshLog, ip_reader).parse()
	telnet_list = Telnet(telnetLog, ip_reader).parse()
	http_s = Http_s(httpLog, httpsLog, ip_reader).parse()

	# aggregate and summary of parsed data
	ssh_table = ssh_list[0]
	ssh_tableSum = ssh_list[1]
	telnet_table = telnet_list[0]
	telnet_tableSum = telnet_list[1]
	http_table = http_s[0]
	httpSum_table = http_s[1]
	https_table = http_s[2]
	httpsSum_table = http_s[3]

	# output the parsed data to csv
	logsToCsv(ssh_table, telnet_table, http_table, https_table)
	sumToCsv(ssh_tableSum, telnet_tableSum, httpSum_table, httpsSum_table)
	aggToCsv(ssh_table, telnet_table, http_table, https_table)
	print('Logs parsed.')