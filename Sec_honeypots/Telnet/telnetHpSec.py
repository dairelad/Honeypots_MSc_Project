from datetime import datetime
from twisted.internet import protocol, reactor, endpoints
import logging
import random
import os
import re
import geoip2.database

#get folder path
path = os.getcwd()

#code used for logging information about the attack
logging.basicConfig(
    filename=f'{path}/telnet/telnetSec.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',)

def detect_url(command, client_ip):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    result = re.findall(regex, command)
    if result:
        for ar in result:
            for url in ar:
                if url != '':
                    logging.info('New URL detected from {}: {}'.format(client_ip, url))

    ip_regex = r"([0-9]+(?:\.[0-9]+){3}\/\S*)"
    ip_result = re.findall(ip_regex, command)
    if ip_result:
        for ip_url in ip_result:
            if ip_url != '':
                logging.info('New IP-based URL detected from {}: {}'.format(client_ip, ip_url))

class Telnet(protocol.Protocol):
    # Code used to find the location of an IP Address
    ip_reader = geoip2.database.Reader(
        '/usr/src/app/GeoLite2-City_20211102/GeoLite2-City.mmdb')

    PROMPT = ("/ # ").encode('utf-8')
    def dataReceived(self, data):
        data = data.strip()

        if data == "id".encode('utf-8'):
            self.transport.write(("uid=0(root) gid=0(root) groups=0(root)\n").encode('utf-8')) #highlighted because of type mismatch (looking for a bytes-like object is required, not 'str')
        elif data == "uname".encode('utf-8'):
            self.transport.write(("Linux f001 3.13.3-7-high-octane-fueled #3000-LPG SMPx4 Fri Jun 31 25:24:23 UTC 2200 x86_64 x64_86 x13_37 GNU/Linux\n").encode('utf-8'))
        elif data == "^]".encode('ASCII'):
            self.transport.loseConnection()
        else:
            if random.randrange(0, 2) == 0 and data != "":
                self.transport.write(("bash: " +  str(data) + ": command not found\n").encode('utf-8'))

        self.transport.write(Telnet.PROMPT)

        if data != "":
            print("[*] Telnet command received")
            logging.info("New command from " + self.transport.getPeer().host + ": " + str(data))
            detect_url(data.decode(), self.transport.getPeer().host)

    def connectionMade(self):
        try:
            response = self.ip_reader.city(str(self.transport.getPeer().host))
            if response.country.name != 'United Kingdom':
                self.transport.loseConnection()
                logging.info("Connection blocked from: " + self.transport.getPeer().host)
            else:
                self.transport.write(Telnet.PROMPT)
                logging.info("New connection from: " + self.transport.getPeer().host)
                reactor.callLater(20, self.transport.loseConnection)  # 20 second timeout on server
        except Exception as e:
            print('Cannot find location')
            self.transport.loseConnection()


class TelnetFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Telnet()

print("[*] Telnet honeypot is listening on port 8023...")
endpoints.serverFromString(reactor, "tcp:8023").listen(TelnetFactory())
reactor.run()

if __name__ == '__main__':
    try:
        Telnet()
    except KeyboardInterrupt:
        pass