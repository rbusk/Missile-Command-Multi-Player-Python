import pygame
from pygame.locals import *
from server_gamespace import *


import sys
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor

PLAYER_1_PORT = 40003
PLAYER_2_PORT = 40008
global NUMBER_OF_PLAYERS
NUMBER_OF_PLAYERS = 0


#Player 1
class Player1Conn(Protocol):
	def __init__(self,addr):
		self.addr = addr

	def dataReceived(self,data):
		print 'Received Data:', data

	def connectionMade(self):
		print 'New conenction from', self.addr
		global NUMBER_OF_PLAYERS
		print NUMBER_OF_PLAYERS
		if NUMBER_OF_PLAYERS == 0:
			NUMBER_OF_PLAYERS = 1
			self.transport.write("Missiles")
		elif NUMBER_OF_PLAYERS == 1:
			NUMBER_OF_PLAYERS = 2
			self.transport.write("Bombs")
			game = Gamespace()
			game.main()

	def connectionLost(self,reason):
		print 'Lost connection to', self.addr
		reactor.stop()

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
		print 'Received Data:', data

	def connectionMade(self):
		print 'New conenction from', self.addr
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

class Player2ConnFactory(Factory):
	def __init__(self):
		pass

	def buildProtocol(self, addr):
		return Player2Conn(addr)

if __name__ == '__main__':
	reactor.listenTCP(PLAYER_1_PORT, Player1ConnFactory())
	reactor.listenTCP(PLAYER_2_PORT, Player2ConnFactory())
	reactor.run()

