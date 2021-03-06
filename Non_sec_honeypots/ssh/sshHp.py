#!/usr/bin/env python
import argparse
import threading
import socket
import sys
import os
import traceback
import re
import logging
import paramiko
from datetime import datetime
from binascii import hexlify
from paramiko.py3compat import b, u, decodebytes

HOST_KEY = paramiko.RSAKey(filename='server.key')
SSH_BANNER = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"

# code for recognising client key presses
UP_KEY = '\x1b[A'.encode()
DOWN_KEY = '\x1b[B'.encode()
RIGHT_KEY = '\x1b[C'.encode()
LEFT_KEY = '\x1b[D'.encode()
BACK_KEY = '\x7f'.encode()

#Create folders for seperate days
path = os.getcwd()
if not os.path.exists('Day1'):
    for i in range(7):
        os.mkdir(f'Day{i+1}')

# logger method for logging to correct day
def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)

# create correct folder hierarchy
logger_set = {}
NUM_DAYS_IN_WEEK = 7
for i in range(NUM_DAYS_IN_WEEK):
    day_name = f"Day{str(i+1)}"
    setup_logger(day_name, f'{path}/{day_name}/sshD{str(i+1)}.log')
    logger_set[str(i+1)] = logging.getLogger(day_name)

# code detects any URLs input by the client
def detect_url(command, client_ip):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    result = re.findall(regex, command)
    if result:
        for ar in result:
            for url in ar:
                if url != '':
                    day = datetime.today().weekday() + 1  # saves current day (monday=0 & sunday=6)+1
                    logger_set[str(day)].info('New URL detected from {}: {}'.format(client_ip, url))

    ip_regex = r"([0-9]+(?:\.[0-9]+){3}\/\S*)"
    ip_result = re.findall(ip_regex, command)
    if ip_result:
        for ip_url in ip_result:
            if ip_url != '':
                day = datetime.today().weekday() + 1  # saves current day (monday=0 & sunday=6)+1
                logger_set[str(day)].info('New IP-based URL detected from {}: {}'.format(client_ip, ip_url))

#code handles basic/common terminal commands and gives appropriate reponses
def handle_cmd(cmd, chan, ip):

    detect_url(cmd, ip)
    response = ""

    if cmd.startswith("ls"):
        response = "users.txt"
    elif cmd.startswith("pwd"):
        response = "/home/root"
    elif cmd.startswith("cat /proc/cpuinfo | grep name | wc -l"):
        response = "2"
    elif cmd.startswith("uname -a"):
        response = "Linux server 4.15.0-147-generic #151-Ubuntu SMP Fri Jun 18 19:21:19 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux"
    elif cmd.startswith("cat /proc/cpuinfo | grep name | head -n 1 | awk '{print $4,$5,$6,$7,$8,$9;}'"):
        response = "Intel(R) Xeon(R) CPU E5-2680 v3 @"
    elif cmd.startswith("free -m | grep Mem | awk '{print $2 ,$3, $4, $5, $6, $7}'"):
        response = "7976 5167 199 1 2609 2519"
    elif cmd.startswith("ls -lh $(which ls)"):
        response = "-rwxr-xr-x 1 root root 131K Jan 18  2018 /bin/ls"
    elif cmd.startswith("crontab -l "):
        response = "no crontab for root"

    if response != '':
        response = response + "\r\n"
    chan.send(response)

#class accepts any credentials and logs every username, password and ip address
class BasicSshHoneypot(paramiko.ServerInterface):
    client_ip = None
    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

    def get_allowed_auths(self, username):
        return "publickey,password"

    def check_auth_publickey(self, username, key):
        fingerprint = u(hexlify(key.get_fingerprint()))
        return paramiko.AUTH_PARTIALLY_SUCCESSFUL        

    def check_auth_password(self, username, password):
        # Accept all passwords as valid by default
        day = datetime.today().weekday() + 1  # saves current day (monday=0 & sunday=6)+1
        logger_set[str(day)].info('New client credentials from {}: username: {}, password: {}'.format(
                    self.client_ip, username, password))
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_exec_request(self, channel, command):
        command_text = str(command.decode("utf-8"))
        handle_cmd(command_text, channel, self.client_ip)
        day = datetime.today().weekday() + 1  # saves current day (monday=0 & sunday=6)+1
        logger_set[str(day)].info('New command from {}: {}'.format(self.client_ip, command))
        return True

#SSH banner sent to client after connection and logs important client data
def handle_connection(client, addr):
    client_ip = addr[0]
    day = datetime.today().weekday() + 1  # saves current day (monday=0 & sunday=6)+1
    logger_set[str(day)].info('New connection from: {}'.format(client_ip))
    print('New connection from: {}'.format(client_ip))

    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(HOST_KEY)
        transport.local_version = SSH_BANNER # Change banner to appear more convincing
        server = BasicSshHoneypot(client_ip)

        try:
            transport.start_server(server=server)
            transport.banner_timeout = 200

        except paramiko.SSHException:
            print('*** SSH negotiation failed.')
            raise Exception("SSH negotiation failed")

        # wait for auth
        chan = transport.accept(10)
        if chan is None:
            print('*** No channel (from '+client_ip+').')
            raise Exception("No channel")
        
        chan.settimeout(10)

        server.event.wait(10)
        if not server.event.is_set():
            raise Exception("No shell request")
     
        try:
            chan.send("Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-128-generic x86_64)\r\n\r\n")
            run = True
            while run:
                chan.send("$ ")
                command = ""
                while not command.endswith("\r"):
                    transport = chan.recv(1024)
                    print(client_ip+"- received:",transport)
                    # Echo input to psuedo-simulate a basic terminal
                    if(
                        transport != UP_KEY
                        and transport != DOWN_KEY
                        and transport != LEFT_KEY
                        and transport != RIGHT_KEY
                        and transport != BACK_KEY
                    ):
                        chan.send(transport)
                        command += transport.decode("utf-8")
                
                chan.send("\r\n")
                command = command.rstrip()
                day = datetime.today().weekday() + 1  # saves current day (monday=0 & sunday=6)+1
                logger_set[str(day)].info('New command from {}: {}'.format(client_ip, command))

                if command == "exit":
                    run = False

                else:
                    handle_cmd(command, chan, client_ip)

        except Exception as err:
            print('!!! Exception: {}: {}'.format(err.__class__, err))
            try:
                transport.close()
            except Exception:
                pass

        chan.close()

    except Exception as err:
        print('!!! Exception: {}: {}'.format(err.__class__, err))
        try:
            transport.close()
        except Exception:
            pass


#code opens a port and binds it to the application
def start_server(port, bind):
    """Init and run the ssh server"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((bind, port))
    except Exception as err:
        print('*** Bind failed: {}'.format(err))
        traceback.print_exc()
        sys.exit(1)

    threads = []
    while True:
        try:
            sock.listen(100)
            print('[*] SSH honeypot is listening for connection on port {} ...'.format(port))
            client, addr = sock.accept()
        except Exception as err:
            print('*** Listen/accept failed: {}'.format(err))
            traceback.print_exc()

        # creates a new thread for each connection to the honeypot
        new_thread = threading.Thread(target=handle_connection, args=(client, addr))
        new_thread.start()
        threads.append(new_thread)
        for thread in threads:
            thread.join()

#code used to pass in parameters when invoking python script
if __name__ == "__main__":
    start_server(2222, "")