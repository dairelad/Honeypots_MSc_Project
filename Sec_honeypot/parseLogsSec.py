#!/usr/local/bin/env python
import pandas as pd
import numpy as np
import datetime
import geoip2.database
import os
import sys

day = datetime.datetime.today().weekday()  # saves current day (monday=0 & sunday=6)

# Create folders for csv files
path = os.getcwd()
if not os.path.exists('csv/Aggregate'):
    os.mkdir('csv')
    os.mkdir('csv/Aggregate')
    os.mkdir('csv/Summary')

try:
    # Read honeypot log files
    sshLog = open("/usr/src/app/fail2ban.log", 'r').read().split("\n")
    telnetLog = open("/usr/src/app/telnet/telnetSec.log", 'r').read().split("\n")
    httpLog = open("/usr/src/app/http/httpSec.log", 'r').read().split("\n")
    httpsLog = open("/usr/src/app/https/httpsSec.log", 'r').read().split("\n")
except IOError:
    print('Could not open logs')
    sys.exit()

try:
    # Read in summary csvs so that the correct row (day) can be updated
    sshSumCsv = pd.read_csv("/usr/src/app/csv/Summary/sshSumSec.csv")
    telnetSumCsv = pd.read_csv("/usr/src/app/csv/Summary/telnetSumSec.csv")
    httpSumCsv = pd.read_csv("/usr/src/app/csv/Summary/httpSumSec.csv")
    httpsSumCsv = pd.read_csv("/usr/src/app/csv/Summary/httpsSumSec.csv")
except IOError:
    print('Could not open summaries')
    sys.exit()

try:
    # Read number of current lines in aggregate files so they can be updated
    sshAggCsv = pd.read_csv("/usr/src/app/csv/Aggregate/sshAggSec.csv")
    telnetAggCsv = pd.read_csv("/usr/src/app/csv/Aggregate/telnetAggSec.csv")
    httpAggCsv = pd.read_csv("/usr/src/app/csv/Aggregate/httpAggSec.csv")
    httpsAggCsv = pd.read_csv("/usr/src/app/csv/Aggregate/httpsAggSec.csv")
except IOError:
    print('Could not open aggregates')
    sys.exit()

# Code used to find the location of an IP Address
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
column16 = '# blocked'

def parseSumsToCsv(ssh, telnet, http, https):
    # if file does not exist write header
    if not os.path.isfile('/usr/src/app/csv/Summary/sshSumSec.csv'):
        ssh.to_csv('/usr/src/app/csv/Summary/sshSumSec.csv', index=False)
    else:  # else it exists so append without writing the header
        sshSumCsv.iloc[0, [0, 1]] = ssh.iloc[0, [0, 1]]
        sshSumCsv.to_csv('/usr/src/app/csv/Summary/sshSumSec.csv', index=False)
    if not os.path.isfile('/usr/src/app/csv/Summary/telnetSumSec.csv'):
        telnet.to_csv('/usr/src/app/csv/Summary/telnetSumSec.csv', index=False)
    else:
        telnetSumCsv.iloc[0, [0, 1, 2, 3]] = telnet.iloc[0, [0, 1, 2, 3]]
        telnetSumCsv.to_csv('/usr/src/app/csv/Summary/telnetSumSec.csv', index=False)
    if not os.path.isfile('/usr/src/app/csv/Summary/httpSumSec.csv'):
        http.to_csv('/usr/src/app/csv/Summary/httpSumSec.csv', index=False)
    else:
        httpSumCsv.iloc[0, [0, 1]] = http.iloc[0, [0, 1]]
        httpSumCsv.to_csv('/usr/src/app/csv/Summary/httpSumSec.csv', index=False)
    if not os.path.isfile('/usr/src/app/csv/Summary/httpsSumSec.csv'):
        https.to_csv('/usr/src/app/csv/Summary/httpsSumSec.csv', index=False)
    else:
        httpsSumCsv.iloc[0, [0, 1]] = https.iloc[0, [0, 1]]
        httpsSumCsv.to_csv('/usr/src/app/csv/Summary/httpsSumSec.csv', index=False)


def parseCsvToAgg(ssh, telnet, http, https):
    ssh_parsed = pd.concat([sshAggCsv, ssh])
    telnet_parsed = pd.concat([telnetAggCsv, telnet])
    http_parsed = pd.concat([httpAggCsv, http])
    https_parsed = pd.concat([httpsAggCsv, https])

    ssh_parsed['timestamp'] = ssh_parsed['timestamp'].astype(str).str.slice(0, 23)
    telnet_parsed['timestamp'] = telnet_parsed['timestamp'].astype(str).str.slice(0, 23)
    http_parsed['timestamp'] = http_parsed['timestamp'].astype(str).str.slice(0, 23)
    https_parsed['timestamp'] = https_parsed['timestamp'].astype(str).str.slice(0, 23)

    ssh_parsed = ssh_parsed.astype(str)
    telnet_parsed = telnet_parsed.astype(str)
    http_parsed = http_parsed.astype(str)
    https_parsed = https_parsed.astype(str)

    ssh_parsed = ssh_parsed.drop_duplicates(subset=None, keep="first", inplace=False)
    telnet_parsed = telnet_parsed.drop_duplicates(subset=None, keep="first", inplace=False)
    http_parsed = http_parsed.drop_duplicates(subset=None, keep="first", inplace=False)
    https_parsed = https_parsed.drop_duplicates(subset=None, keep="first", inplace=False)

    ssh_parsed['ip'].replace('', np.nan, inplace=True)
    telnet_parsed['ip'].replace('', np.nan, inplace=True)
    http_parsed['ip'].replace('', np.nan, inplace=True)
    https_parsed['ip'].replace('', np.nan, inplace=True)

    ssh_parsed.dropna(subset=['ip'], inplace=True)
    telnet_parsed.dropna(subset=['ip'], inplace=True)
    http_parsed.dropna(subset=['ip'], inplace=True)
    https_parsed.dropna(subset=['ip'], inplace=True)

    ssh_parsed = ssh_parsed.sort_values(by=['timestamp'], ascending=True)
    telnet_parsed = telnet_parsed.sort_values(by=['timestamp'], ascending=True)
    http_parsed = http_parsed.sort_values(by=['timestamp'], ascending=True)
    https_parsed = https_parsed.sort_values(by=['timestamp'], ascending=True)

    # if file does not exist write header
    if not os.path.isfile('/usr/src/app/csv/Aggregate/sshAggSec.csv'):
        ssh.to_csv('/usr/src/app/csv/Aggregate/sshAggSec.csv', index=False)
    else:  # else it exists so append without writing the header
        ssh_parsed.to_csv('/usr/src/app/csv/Aggregate/sshAggSec.csv', index=False)

    if not os.path.isfile('/usr/src/app/csv/Aggregate/telnetAggSec.csv'):
        telnet.to_csv('/usr/src/app/csv/Aggregate/telnetAggSec.csv', index=False)
    else:
        telnet_parsed.to_csv('/usr/src/app/csv/Aggregate/telnetAggSec.csv', index=False)

    if not os.path.isfile('/usr/src/app/csv/Aggregate/httpAggSec.csv'):
        http.to_csv('/usr/src/app/csv/Aggregate/httpAggSec.csv', index=False)
    else:
        http_parsed.to_csv('/usr/src/app/csv/Aggregate/httpAggSec.csv', index=False)

    if not os.path.isfile('/usr/src/app/csv/Aggregate/httpsAggSec.csv'):
        https.to_csv('/usr/src/app/csv/Aggregate/httpsAggSec.csv', index=False)
    else:
        https_parsed.to_csv('/usr/src/app/csv/Aggregate/httpsAggSec.csv', index=False)


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
    ssh_found = []
    ssh_ban = []

    found_count = 0
    ban_count = 0

    def parse(self):
        # Code for parsing sshLog to csv
        for line in sshLog:
            if "Found" in line:
                var = line.split(" [sshd] ")
                var2 = var[1].split(" - ")
                ip = var2[0].replace("Found ", "")
                ts = var2[1]
                try:
                    response = self.ip_reader.city(ip)
                    if response.country.name == 'United Kingdom':
                        self.ssh_ips.append(ip)
                        self.ssh_timestamps.append(ts)
                        self.found_count += 1
                        self.ssh_countries.append(response.country.name)
                        self.ssh_provinces.append(response.subdivisions.most_specific.name)
                        self.ssh_cities.append(response.city.name)
                        self.ssh_lats.append(response.location.latitude)
                        self.ssh_longs.append(response.location.longitude)
                except Exception as e:
                    pass

            elif "Ban" in line:
                var = line.split(" [sshd] ")
                ip = var[1].replace("Ban ", "")
                try:
                    response = self.ip_reader.city(ip)
                    if response.country.name == 'United Kingdom':
                        self.ban_count += 1
                        self.ssh_ips.append(ip)
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
        if max_col < len(self.ssh_timestamps):
            max_col = len(self.ssh_timestamps)
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
        dif_ts = max_col - len(self.ssh_timestamps)
        dif_urls = max_col - len(self.ssh_urls)
        dif_commands = max_col - len(self.ssh_commands)
        dif_credentials_u = max_col - len(self.ssh_usernames)
        dif_credentials_p = max_col - len(self.ssh_passwords)
        dif_geoip = max_col - len(self.ssh_cities)

        # Append none to each list to make size consistent
        for x in range(dif_ips):
            self.ssh_ips.append(np.nan)
        for x in range(dif_ts):
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
            column7: self.ssh_countries,
            column8: self.ssh_provinces,
            column9: self.ssh_cities,
            column10: self.ssh_longs,
            column11: self.ssh_lats
        }

        self.ssh_found.append(self.found_count)
        self.ssh_ban.append(self.ban_count)

        # Add data to dictionary
        sshSum_dict = {
            column12: self.ssh_found,
            column16: self.ssh_ban,
        }

        sshSum_table = pd.DataFrame(sshSum_dict)

        ssh_table = pd.DataFrame(ssh_dict)
        ssh_table.drop(ssh_table.loc[ssh_table['ip'] == ''].index,
                       inplace=True)  # remove any blank rows (hackers feeding in junk)
        ssh_table = ssh_table[:-1]  # remove last row (hackers feeding in junk)

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
    telnet_sumCon = []
    telnet_sumCom = []
    telnet_sumUrl = []
    telnet_blocked = []

    connection_count = 0
    blocked_count = 0
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

            elif "Connection blocked" in line:
                var = line.split(" - ")
                # Create datetime object and append to timestamp list
                self.telnet_timestamps.append(datetime.datetime.strptime(var[0], "%Y-%m-%d %H:%M:%S,%f"))
                # format ip address and add to list
                ip = var[-1].replace("Connection blocked from: ", "")
                self.telnet_ips.append(np.nan)
                self.blocked_count += 1
                self.telnet_countries.append(np.nan)
                self.telnet_provinces.append(np.nan)
                self.telnet_cities.append(np.nan)
                self.telnet_longs.append(np.nan)
                self.telnet_lats.append(np.nan)

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
                    pass

        # Find max column size
        max_col = 0
        if max_col < len(self.telnet_ips):
            max_col = len(self.telnet_ips)
        if max_col < len(self.telnet_timestamps):
            max_col = len(self.telnet_timestamps)
        if max_col < len(self.telnet_urls):
            max_col = len(self.telnet_urls)
        if max_col < len(self.telnet_commands):
            max_col = len(self.telnet_commands)

        # Difference between each column and max size
        dif_ips = max_col - len(self.telnet_ips)
        dif_ts = max_col - len(self.telnet_timestamps)
        dif_urls = max_col - len(self.telnet_urls)
        dif_commands = max_col - len(self.telnet_commands)
        dif_geoip = max_col - len(self.telnet_cities)

        # Append none to each list to make size consistent
        for x in range(dif_ips):
            self.telnet_ips.append(np.nan)
        for x in range(dif_ts):
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

        self.telnet_sumCon.append(self.connection_count)
        self.telnet_sumCom.append(self.commands_count)
        self.telnet_sumUrl.append(self.urls_count)
        self.telnet_blocked.append(self.blocked_count)

        # Add data to dictionary
        telnetSum_dict = {
            column12: self.telnet_sumCon,
            column14: self.telnet_sumCom,
            column15: self.telnet_sumUrl,
            column16: self.telnet_blocked,
        }

        telnetSum_table = pd.DataFrame(telnetSum_dict)

        telnet_table = pd.DataFrame(telnet_dict)
        return telnet_table, telnetSum_table


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
    http_blocked = []

    https_ips = []
    https_timestamps = []
    https_countries = []
    https_provinces = []
    https_cities = []
    https_longs = []
    https_lats = []
    https_sum = []
    https_blocked = []

    connection_count1 = 0
    blocked_count1 = 0
    connection_count2 = 0
    blocked_count2 = 0

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

            elif "Connection blocked" in line:
                var = line.split(" - ")
                # Create datetime object and append to timestamp list
                self.http_timestamps.append(datetime.datetime.strptime(var[0], "%Y-%m-%d %H:%M:%S,%f"))
                # format ip address and add to list
                ip = var[-1].replace("Connection blocked from: ", "")
                self.http_ips.append(np.nan)
                self.blocked_count1 += 1
                self.http_countries.append(np.nan)
                self.http_provinces.append(np.nan)
                self.http_cities.append(np.nan)
                self.http_longs.append(np.nan)
                self.http_lats.append(np.nan)

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

            elif "Connection blocked" in line:
                var = line.split(" - ")
                # Create datetime object and append to timestamp list
                self.http_timestamps.append(datetime.datetime.strptime(var[0], "%Y-%m-%d %H:%M:%S,%f"))
                # format ip address and add to list
                ip = var[-1].replace("Connection blocked from: ", "")
                self.http_ips.append(np.nan)
                self.blocked_count2 += 1
                self.http_countries.append(np.nan)
                self.http_provinces.append(np.nan)
                self.http_cities.append(np.nan)
                self.http_longs.append(np.nan)
                self.http_lats.append(np.nan)

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
        self.http_blocked.append(self.blocked_count1)
        self.https_blocked.append(self.blocked_count2)

        # Add data to dictionary
        httpSum_dict = {
            column12: self.http_sum,
            column16: self.http_blocked,
        }

        # Add data to dictionary
        httpsSum_dict = {
            column12: self.https_sum,
            column16: self.https_blocked
        }

        httpSum_table = pd.DataFrame(httpSum_dict)
        httpsSum_table = pd.DataFrame(httpsSum_dict)

        http_table = pd.DataFrame(http_dict)
        https_table = pd.DataFrame(https_dict)

        return http_table, httpSum_table, https_table, httpsSum_table


if __name__ == "__main__":
    print('Parsing logs..')
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

    # parseLogsToCsv(ssh_table, telnet_table, http_table, https_table)
    parseSumsToCsv(ssh_tableSum, telnet_tableSum, httpSum_table, httpsSum_table)
    parseCsvToAgg(ssh_table, telnet_table, http_table, https_table)
    print('Logs parsed.')