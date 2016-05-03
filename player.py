#Ryan Busk
#4/30/2016
import sys
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from objects.client_gs import *

TYPE = None #Bomb or Missile
PLAYER_1 = 40003 #port for player 1
PLAYER_2 = 40008 #port for player 2
HOST = '127.0.0.1'

gs = Gamespace() #initialize local gamespace

class Player(Protocol):
	def dataReceived(self,data):
		"""when data is received, parse data and send it to the right place"""
		if data == 'Missiles' or data == 'Bombs': #check if initial send is bomb or missile
			self.TYPE = data #set type
			gs.TYPE = self.TYPE #set type in gamespace
			self.lc = LoopingCall(gs.ticks) #start looping call
			self.lc.start(1./60) #set clock time
		elif data == "Turn Over": #if server says turn is over
			gs.reset_turn() #reset turn in gs
		elif data == "Round Over": #same with round
			gs.reset_round() #reset round
		elif data == "Game Over": #same wih game
			gs.game_over()
		else:
			data_queue.put(data) #send any other data to queue


	def connectionMade(self):
		"""when initial connection is made. add callback queue for both queues"""
		command_queue.get().addCallback(self.callback) #command queue
		data_queue.get().addCallback(gs.callback) #data queue

	def connectionLost(self,reason):
		"""stop reactor when connection is lost"""
		reactor.stop()

	def callback(self,data):
		"""callback to add to the queue"""
		self.transport.write(data)
		command_queue.get().addCallback(self.callback)


class ClientConnFactory(ClientFactory):
	def buildProtocol(self,addr):
		"""return player when factory is called"""
		return Player()

if __name__ == '__main__':
	"""run this to start game"""
	for args in sys.argv:
		if args == "1":
			#if first player, run this
			PLAYER = 1
			reactor.connectTCP(HOST,PLAYER_1,ClientConnFactory())
			break
		if args == "2":
			#if second player, run this
			PLAYER = 2
			reactor.connectTCP(HOST,PLAYER_2,ClientConnFactory())
			break
	#run reactor
	reactor.run()

