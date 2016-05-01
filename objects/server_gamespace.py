import pygame
from pygame.locals import *
import sys
from city import City, Base
from missile import Missile, Bomb
from explosion import Explosion
from math import sqrt
from twisted.internet.defer import DeferredQueue
import cPickle as pickle

p1_data_queue = DeferredQueue()
p1_command_queue = DeferredQueue()
p2_data_queue = DeferredQueue()
p2_command_queue = DeferredQueue()

class Gamespace(object):

	def __init__(self, current_player):
		self.current_player = current_player

	def main(self):

		#initialize
		#pygame.init()
		self.size = width, height = 640, 480
		#self.screen = pygame.display.set_mode(self.size)
		self.clock = pygame.time.Clock()

		self.initialize_cities_bases()

		#active bombs missiles and explosions(empty at first)
		self.missiles = []
		self.bombs = []
		self.explosions = []
		self.bomb_explosions = []

		self.nbombs = 0 #keep track of how many bombs have been dropped
		self.maxbombs = 6 #max number of bombs that can be dropped

		#player 1 shoots missiles, player 2 drops bombs
		gameover = 0

		self.bomb_speed = 2
		self.missile_speed = 2

		self.player = 1 #1 or 2, depending on who is playing

		#points for players 1 and 2
		self.p1_points = 0
		self.p2_points = 0

		while not gameover:
			#click tick
			self.clock.tick(60)

			#tick updates
			self.ticks()

			gameover = self.check_winner()

		#calculate points for whoever is aiming missiles
		if self.player == 1:
			self.p1_points = self.p1_points + self.calculate_points()
		else:
			self.p2_points = self.p2_points + self.calculate_points()

		print "p1:", self.p1_points
		print "p2:", self.p2_points

	def ticks(self):

		# call ticks for each object
		i = 0
		while (i < len(self.missiles)):
			self.missiles[i].tick()

			#check if missile is dead; if so, create explosion and pop off of list
			if (self.missiles[i].da == 0):
				explosion = Explosion(self.missiles[i].fx, self.missiles[i].fy, 2, 50, self)
				self.explosions.append(explosion)
				del self.missiles[i]
			else:
				i = i+1

		i = 0
		while (i < len(self.explosions)):
			self.explosions[i].tick()

			#check if explosion is dead; if so, pop off of list
			if (self.explosions[i].da == 0):
				del self.explosions[i]
			else:
				i = i+1
		
		i = 0
		while (i < len(self.bomb_explosions)):
			self.bomb_explosions[i].tick()

			#check if explosion is dead; if so, pop off of list
			if (self.bomb_explosions[i].da == 0):
				del self.bomb_explosions[i]
			else:
				i = i+1

		i = 0
		while (i < len(self.bombs)):
			self.bombs[i].tick()

			#check if bomb is dead; if so, create explosion and pop off of list
			#also, make city or base "dead"
			if (self.bombs[i].da == 0):

				dest = self.bombs[i].dest #get destination 0-8 of bomb

				#if destination is a base, set count to 0
				if (dest % 4 == 0):
					self.bases[dest/4].count = 0

				#else if destination is a city, destroy it
				else:
					if (dest <= 3):
						self.cities[dest-1].da = 0
					else:
						self.cities[dest-2].da = 0

				explosion = Explosion(self.bombs[i].fx, self.bombs[i].fy, 2, 50, self)
				self.bomb_explosions.append(explosion)
				del self.bombs[i]
			else:
				i = i+1

		self.check_collisions()

	def check_collisions(self):

		for explosion in self.explosions:
			i = 0
			while (i < len(self.bombs)):
				#calculate distance from missile to explosion
				dx = explosion.pos[0] - self.bombs[i].pos[0]
				dy = explosion.pos[1] - self.bombs[i].pos[1]

				d = sqrt(dx*dx + dy*dy)

				#if bomb is within the explosion, add points and delete the bomb
				if (explosion.r > d):
					if (self.player == 1):
						self.p1_points = self.p1_points + 1
						print "adding a point for p1"
					else:
						self.p2_points = self.p2_points + 2
						print "adding a point for p2"
					del self.bombs[i]
				else:
					i = i+1


	def initialize_cities_bases(self):

		#initialize cities and bases list
		self.cities = []
		self.bases = []

		#calculate what width/height of each city/base should be
		width = (self.size[0] - 200) / 9

		#initialize and bases
		for i in range(0, 9):

			# if i is 0, 4, or 8, then create a base instead of a city
			if (i % 4 == 0):
				base = Base(20*(i+1) + i*width, self.size[1] - width,  width, width, 9, self)
				self.bases.append(base)
			else:
				city = City(20*(i+1) + i*width, self.size[1] - width,  width, width, self)
				self.cities.append(city)

		self.city_width = width

	def check_winner(self):

		#check cities -- if they are all dead, then player 2 wins
		ncities_dead = 0
		for city in self.cities:
			if city.da == 0:
				ncities_dead = ncities_dead + 1

		if ncities_dead == len(self.cities):
			return 1

		#if player 2 has dropped all of his bombs and all of them have exploded, then player 1 wins
		elif (self.nbombs >= self.maxbombs and len(self.bomb_explosions) == 0 and len(self.bombs) == 0):
			return 1

		else:
			return 0

	#calculate points for player aiming missiles
	def calculate_points(self):

		points = 0

		#points for each missile left
		for base in self.bases:
			points = points + base.count

		#points for each city left
		for city in self.cities:
			if city.da == 1:
				points = points + 1

		return points
