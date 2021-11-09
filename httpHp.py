import logging as log
import socket
import atexit

# Local IP/Port for the honeypot to listen on (TCP)
LHOST = '0.0.0.0'
LPORT = 8080 # non admin http port

#code used for logging information about the attack
log.basicConfig(
    filename='http_honeypot.log',
    level=log.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')

# Socket timeout in seconds
TIMEOUT = 0.00001

# Banner information
Banner = "HTTP/1.1 403 Forbidden" \
         "Date: Mon, 08 Nov 2021 18:59:22 GMT" \
         "Server: Apache" \
         "Content-Length: 264" \
         "Content-Type: text/html; charset=iso-8859-1"

def main():
    print ('[*] HTTP honeypot listening for connection on ' + LHOST + ':' + str(LPORT))
    atexit.register(exit_handler)

    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((LHOST, LPORT))
    listener.listen(5)
    count = 0
    while True:
        try:
            (connection, address) = listener.accept()
            log.info('Honeypot connection from ' + address[0] + ':' + str(address[1]))
            listener.settimeout(TIMEOUT)
            print ('[*] Honeypot connection from ' + address[0] + ':' + str(address[1]) + ' on port ' + str(LPORT))
            count = 0
        except socket.timeout as e:
            if(count < 1):
                print(e)
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