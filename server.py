import sys
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue

PLAYER_1_PORT = 40003
PLAYER_2_PORT = 40008
global NUMBER_OF_PLAYERS
NUMBER_OF_PLAYERS = 0
#flags to check if round is over for both players
round_over = 0
turn_over = 0
game_over = 0

p1_data_queue = DeferredQueue() #server queue from player 1 to player 2
p2_data_queue = DeferredQueue() #server queue from player 2 to player 1


#Player 1
class Player1Conn(Protocol):
	def __init__(self,addr):
		self.addr = addr

	def dataReceived(self,data):
		"""parse data received from client"""
		global round_over, turn_over, game_over #global variables to share between players
		if data == "Round Over":
			"""only sends round over if both players complete round"""
			round_over += 1
			if round_over == 2:
				p1_data_queue.put("Round Over")
				p2_data_queue.put("Round Over")
				round_over = 0
		elif data == "Turn Over":
			"""only sends turn over if both players complete turn"""
			turn_over += 1
			if turn_over == 2:
				p1_data_queue.put("Turn Over")
				p2_data_queue.put("Turn Over")
				turn_over = 0
		elif data == "Game Over":
			"""only sends game over if both players complete game"""
			game_over += 1
			if game_over == 2:
				p1_data_queue.put("Game Over")
				p2_data_queue.put("Game Over")
				game_over = 0
		else:
			"""puts all other data in player 1 queue"""
			p1_data_queue.put(data)

	def connectionMade(self):
		"""on ititial connection send data"""
		p2_data_queue.get().addCallback(self.callback)
		print 'New connection from', self.addr
		global NUMBER_OF_PLAYERS
		"""if first player send missiles, else bombs"""
		if NUMBER_OF_PLAYERS == 0:
			NUMBER_OF_PLAYERS = 1
			self.transport.write("Missiles")
		elif NUMBER_OF_PLAYERS == 1:
			NUMBER_OF_PLAYERS = 2
			self.transport.write("Bombs")

	def connectionLost(self,reason):
		"""if connection is lost, stop reactor"""
		print 'Lost connection to', self.addr
		reactor.stop()

	def callback(self,data):
		"""callback for p1"""
		self.transport.write(data)
		p2_data_queue.get().addCallback(self.callback)

class Player1ConnFactory(Factory):
	def __init__(self):
		pass

	def buildProtocol(self, addr):
		"""build plarer 1 connection"""
		return Player1Conn(addr)

#Player 2
class Player2Conn(Protocol):
	def __init__(self,addr):
		self.addr = addr

	def dataReceived(self,data):
		global round_over,turn_over,game_over
		if data == "Round Over":
			"""only sends round over if both players complete round"""
			round_over += 1
			if round_over == 2:
				print "hello"
				p1_data_queue.put("Round Over")
				p2_data_queue.put("Round Over")
				round_over = 0
		elif data == "Turn Over":
			"""only sends turn over if both players complete turn"""
			turn_over += 1
			if turn_over == 2:
				p1_data_queue.put("Turn Over")
				p2_data_queue.put("Turn Over")
				turn_over = 0
		elif data == "Game Over":
			"""only sends game over if both players complete game"""
			game_over += 1
			if game_over == 2:
				p1_data_queue.put("Game Over")
				p2_data_queue.put("Game Over")
				game_over = 0
		else:
			"""adds other data to queue"""
			p2_data_queue.put(data)

	def connectionMade(self):
		"""when connection is made, act like player one did"""
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
		"""stop rreactor if connection is lost"""
		print 'Lost connection to', self.addr
		reactor.stop()

	def callback(self,data):
		"""player 2 callback"""
		self.transport.write(data)
		p1_data_queue.get().addCallback(self.callback)

class Player2ConnFactory(Factory):
	def __init__(self):
		pass

	def buildProtocol(self, addr):
		return Player2Conn(addr)

if __name__ == '__main__':
	"""listen on ports for clients and run reactor"""
	reactor.listenTCP(PLAYER_1_PORT, Player1ConnFactory())
	reactor.listenTCP(PLAYER_2_PORT, Player2ConnFactory())
	reactor.run()

