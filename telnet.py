from twisted.internet import protocol, reactor, endpoints
import logging
import random
import signal

class Telnet(protocol.Protocol):

#code used for logging information about the attack
    logging.basicConfig(
        filename='telnet_honeypot.log',
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s', 
        datefmt='%m/%d/%Y %I:%M:%S %p')

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
            logging.info(self.transport.getPeer().host + " " + str(data))

    def connectionMade(self):
        self.transport.write(Telnet.PROMPT)

class TelnetFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Telnet()

print("Listening...")
endpoints.serverFromString(reactor, "tcp:8023").listen(TelnetFactory())
reactor.run()
