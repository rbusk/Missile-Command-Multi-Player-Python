import sys
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue

PLAYER_1_PORT = 40003
PLAYER_2_PORT = 40008
global NUMBER_OF_PLAYERS
NUMBER_OF_PLAYERS = 0
round_over = 0
turn_over = 0
game_over = 0

p1_data_queue = DeferredQueue()
p2_data_queue = DeferredQueue()


#Player 1
class Player1Conn(Protocol):
	def __init__(self,addr):
		self.addr = addr

	def dataReceived(self,data):
		global round_over, turn_over, game_over
		if data == "Round Over":
			round_over += 1
			if round_over == 2:
				p1_data_queue.put("Round Over")
				p2_data_queue.put("Round Over")
				round_over = 0
		elif data == "Turn Over":
			turn_over += 1
			if turn_over == 2:
				p1_data_queue.put("Turn Over")
				p2_data_queue.put("Turn Over")
				turn_over = 0
		elif data == "Game Over":
			game_over += 1
			if game_over == 2:
				p1_data_queue.put("Game Over")
				p2_data_queue.put("Game Over")
				game_over = 0
		else:
			p1_data_queue.put(data)

	def connectionMade(self):
		p2_data_queue.get().addCallback(self.callback)
		print 'New connection from', self.addr
		global NUMBER_OF_PLAYERS
		print NUMBER_OF_PLAYERS
		if NUMBER_OF_PLAYERS == 0:
			NUMBER_OF_PLAYERS = 1
			self.transport.write("Missiles")
		elif NUMBER_OF_PLAYERS == 1:
			NUMBER_OF_PLAYERS = 2
			self.transport.write("Bombs")

	def connectionLost(self,reason):
		print 'Lost connection to', self.addr
		reactor.stop()

	def callback(self,data):
		self.transport.write(data)
		p2_data_queue.get().addCallback(self.callback)

class Player1ConnFactory(Factory):
	def __init__(self):
		pass

	def buildProtocol(self, addr):
		return Player1Conn(addr)

#Player 2
class Player2Conn(Protocol):
	def __init__(self,addr):
		self.addr = addr

	def dataReceived(self,data):
		global round_over,turn_over,game_over
		if data == "Round Over":
			round_over += 1
			if round_over == 2:
				print "hello"
				p1_data_queue.put("Round Over")
				p2_data_queue.put("Round Over")
				round_over = 0
		elif data == "Turn Over":
			turn_over += 1
			if turn_over == 2:
				p1_data_queue.put("Turn Over")
				p2_data_queue.put("Turn Over")
				turn_over = 0
		elif data == "Game Over":
			game_over += 1
			if game_over == 2:
				p1_data_queue.put("Game Over")
				p2_data_queue.put("Game Over")
				game_over = 0
		else:
			p2_data_queue.put(data)

	def connectionMade(self):
		p1_data_queue.get().addCallback(self.callback)
		print 'New connection from', self.addr
		global NUMBER_OF_PLAYERS
		print NUMBER_OF_PLAYERS
		if NUMBER_OF_PLAYERS == 0:
			NUMBER_OF_PLAYERS = 1
			self.transport.write("Missiles")
		elif NUMBER_OF_PLAYERS == 1:
			NUMBER_OF_PLAYERS = 2
			self.transport.write("Bombs")

	def connectionLost(self,reason):
		print 'Lost connection to', self.addr
		reactor.stop()

	def callback(self,data):
		self.transport.write(data)
		p1_data_queue.get().addCallback(self.callback)

class Player2ConnFactory(Factory):
	def __init__(self):
		pass

	def buildProtocol(self, addr):
		return Player2Conn(addr)

if __name__ == '__main__':
	reactor.listenTCP(PLAYER_1_PORT, Player1ConnFactory())
	reactor.listenTCP(PLAYER_2_PORT, Player2ConnFactory())
	reactor.run()

