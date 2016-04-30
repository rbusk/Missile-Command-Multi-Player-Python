#Ryan Busk
#4/30/2016
import sys
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor

PLAYER = 0
TYPE = None
PLAYER_1 = 40003
PLAYER_2 = 40008
HOST = '127.0.0.1'

class Player(Protocol):
	def dataReceived(self,data):
		print data
		if data == 'Missiles' or data == 'Bombs':
			TYPE = data
			print TYPE


	def connectionMade(self):
		print 'Made connection'

	def connectionLost(self,reason):
		print 'Connection Lost'
		reactor.stop()

class ClientConnFactory(ClientFactory):
	def buildProtocol(self,addr):
		return Player()

if __name__ == '__main__':
	for args in sys.argv:
		if args == "1":
			PLAYER = 1
			reactor.connectTCP(HOST,PLAYER_1,ClientConnFactory())
			break
		if args == "2":
			PLAYER = 2
			reactor.connectTCP(HOST,PLAYER_1,ClientConnFactory())
			break
	reactor.run()

