#Ryan Busk
#4/30/2016
import sys
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from client_gs import *

TYPE = None
PLAYER_1 = 40003
PLAYER_2 = 40008
#HOST = '127.0.0.1'
HOST = '10.176.31.106'

gs = Gamespace()

class Player(Protocol):
	def dataReceived(self,data):
		if data == 'Missiles' or data == 'Bombs':
			self.TYPE = data
			self.lc = LoopingCall(gs.ticks, self.TYPE)
			self.lc.start(1./60)
		elif data == "Turn Over":
			if self.TYPE == 'Missiles':
				self.TYPE = "Bombs"
			else:
				self.TYPE = "Missiles"
			gs.reset_turn()
		elif data == "Round Over":
			gs.reset_round()
		elif data == "Game Over":
			gs.game_over()
		else:
			data_queue.put(data)


	def connectionMade(self):
		command_queue.get().addCallback(self.callback)
		data_queue.get().addCallback(gs.callback)

	def connectionLost(self,reason):
		reactor.stop()

	def callback(self,data):
		self.transport.write(data)
		command_queue.get().addCallback(self.callback)


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
			reactor.connectTCP(HOST,PLAYER_2,ClientConnFactory())
			break
	print TYPE
	reactor.run()

