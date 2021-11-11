import logging as log
import socket
import atexit
from datetime import datetime
import os

# Local IP/Port for the honeypot to listen on (TCP)
LHOST = '0.0.0.0'
LPORT = 8443 # non admin https port

day = datetime.today().weekday()+1 # saves current day (monday=0 & sunday=6)+1

#Create folders for seperate days
path = os.getcwd()
if not os.path.exists('Day1'):
    for i in range(7):
        os.mkdir(f'Day{i+1}')

#code used for logging information about the attack
log.basicConfig(
    filename=f'{path}/Day{day}/httpsD{day}.log',
    level=log.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',)

# Socket timeout in seconds
TIMEOUT = 0.00001

# Banner information
BANNER = "HTTP/1.1 403 Forbidden \n" \
         "Date: Fri, 09 Nov 2021 12:00:47 GMT\n" \
         "Server: Apache\n" \
         "Content-Length: 199\n" \
         "Content-Type: text/html; charset=iso-8859-1\n"

def main():
    print ('[*] HTTPS honeypot listening for connection on ' + LHOST + ':' + str(LPORT))
    atexit.register(exit_handler)

    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((LHOST, LPORT))
    listener.listen(5)
    count = 0
    while True:
        try:
            (connection, address) = listener.accept()
            log.info('New connection from: ' + address[0])
            listener.settimeout(TIMEOUT)
            print ('[*] Honeypot connection from ' + address[0] + ':' + str(address[1]) + ' on port ' + str(LPORT))
            count = 0
            connection.send(BANNER.encode())
        except socket.timeout as e:
            if(count < 1):
                print(e)
                connection.close()
                count += 1

def exit_handler():
    print ('\n[*] HTTPS honeypot is shutting down!')
    listener.close()

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass