import logging as log
import socket
import atexit
import os
import geoip2.database

# Code used to find the location of an IP Address
ip_reader = geoip2.database.Reader(
    '/usr/src/app/GeoLite2-City_20211102/GeoLite2-City.mmdb')

# Local IP/Port for the honeypot to listen on (TCP)
LHOST = '0.0.0.0'
LPORT = 8080 # non admin http port

#Create folders for seperate days
path = os.getcwd()

# Socket timeout in seconds
TIMEOUT = 0.00001

# Banner information
BANNER = "HTTP/1.1 403 Forbidden" \
         "Date: Mon, 09 Nov 2021 18:59:22 GMT" \
         "Server: Apache" \
         "Content-Length: 264" \
         "Content-Type: text/html; charset=iso-8859-1"

def main():
    # code used for logging information about the attack
    log.basicConfig(
        filename=f'{path}/http/httpSec.log',
        level=log.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', )

    print ('[*] HTTP honeypot listening for connection on ' + LHOST + ':' + str(LPORT))
    atexit.register(exit_handler)

    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((LHOST, LPORT))
    listener.listen(5)
    count = 0
    while True:
        try:
            (connection, address) = listener.accept()
            try:
                response = ip_reader.city(address[0])
                if response.country.name != 'United Kingdom':
                    connection.close()
                    log.info("Connection blocked from: " + address[0])
                else:
                    log.info('New connection from: ' + address[0])
                    listener.settimeout(TIMEOUT)
                    print(
                        '[*] Honeypot connection from ' + address[0] + ':' + str(address[1]) + ' on port ' + str(LPORT))
                    connection.send(BANNER.encode())
                    count = 0
            except Exception as e:
                print('Cannot find location')
                log.info("Connection blocked from: " + address[0])
                connection.close()
        except socket.timeout as e:
            if(count < 1):
                print("Connection closed by host.")
                connection.close()
                count += 1

def exit_handler():
    print ('\n[*] HTTP honeypot is shutting down!')
    listener.close()

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass