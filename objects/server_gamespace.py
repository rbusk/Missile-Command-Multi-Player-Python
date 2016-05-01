import pygame
from pygame.locals import *
import sys
from city import City, Base
from missile import Missile, Bomb
from explosion import Explosion
from math import sqrt
from twisted.internet.defer import DeferredQueue
import cPickle as pickle

PLAYER = 0

p1_data_queue = DeferredQueue()
p1_command_queue = DeferredQueue()
p2_data_queue = DeferredQueue()
p2_command_queue = DeferredQueue()

class Gamespace(object):

	def __init__(self, current_player=0):
		self.TYPE = None
		self.current_player = current_player
		#initialize
		self.size = width, height = 640, 480

		self.initialize_cities_bases()

		#active bombs missiles and explosions(empty at first)
		self.missiles = []
		self.bombs = []
		self.explosions = []
		self.bomb_explosions = []

		self.nbombs = 0 #keep track of how many bombs have been dropped
		self.maxbombs = 6 #max number of bombs that can be dropped

		#player 1 shoots missiles, player 2 drops bombs
		self.gameover = 0

		self.bomb_speed = 2
		self.missile_speed = 2

		self.player = 1 #1 or 2, depending on who is playing

		#points for players 1 and 2
		self.p1_points = 0
		self.p2_points = 0

	def main(self):


		#click tick

		#handle events

		#tick updates
		self.ticks()

		#draw images

		self.gameover = self.check_winner()

		#calculate points for whoever is aiming missiles
		if self.player == 1:
			self.p1_points = self.p1_points + self.calculate_points()
		else:
			self.p2_points = self.p2_points + self.calculate_points()

		print "p1:", self.p1_points
		print "p2:", self.p2_points



	def ticks(self,TYPE):
		self.TYPE = TYPE

		self.handle_events()
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

	def handle_events(self):
		print self.TYPE

		for event in pygame.event.get():

			#quit game
			if event.type == QUIT:
				sys.exit()

			if event.type == KEYDOWN:

				pos = pygame.mouse.get_pos()

				if self.TYPE == "Bombs":

					#if player still has bombs to drop
					if (self.nbombs < self.maxbombs):

						#if 1-9 pressed, set off bomb
						if event.key == pygame.K_1:
							bomb = Bomb(pos[0], 0, self.bases[0].rect.centerx, self.size[1] - self.city_width, self.bomb_speed, 0, self)
							self.bombs.append(bomb)
							self.nbombs = self.nbombs + 1

						if event.key == pygame.K_2:
							bomb = Bomb(pos[0], 0, self.cities[0].rect.centerx, self.size[1] - self.city_width, self.bomb_speed, 1, self)
							self.bombs.append(bomb)
							self.nbombs = self.nbombs + 1

						if event.key == pygame.K_3:
							bomb = Bomb(pos[0], 0, self.cities[1].rect.centerx, self.size[1] - self.city_width, self.bomb_speed, 2, self)
							self.bombs.append(bomb)
							self.nbombs = self.nbombs + 1

						if event.key == pygame.K_4:
							bomb = Bomb(pos[0], 0, self.cities[2].rect.centerx, self.size[1] - self.city_width, self.bomb_speed, 3, self)
							self.bombs.append(bomb)
							self.nbombs = self.nbombs + 1

						if event.key == pygame.K_5:
							bomb = Bomb(pos[0], 0, self.bases[1].rect.centerx, self.size[1] - self.city_width, self.bomb_speed, 4, self)
							self.bombs.append(bomb)
							self.nbombs = self.nbombs + 1

						if event.key == pygame.K_6:
							bomb = Bomb(pos[0], 0, self.cities[3].rect.centerx, self.size[1] - self.city_width, self.bomb_speed, 5, self)
							self.bombs.append(bomb)
							self.nbombs = self.nbombs + 1

						if event.key == pygame.K_7:
							bomb = Bomb(pos[0], 0, self.cities[4].rect.centerx, self.size[1] - self.city_width, self.bomb_speed, 6, self)
							self.bombs.append(bomb)
							self.nbombs = self.nbombs + 1

						if event.key == pygame.K_8:
							bomb = Bomb(pos[0], 0, self.cities[5].rect.centerx, self.size[1] - self.city_width, self.bomb_speed, 7, self)
							self.bombs.append(bomb)
							self.nbombs = self.nbombs + 1

						if event.key == pygame.K_9:
							bomb = Bomb(pos[0], 0, self.bases[2].rect.centerx, self.size[1] - self.city_width, self.bomb_speed, 8, self)
							self.bombs.append(bomb)
							self.nbombs = self.nbombs + 1

				if self.TYPE == "Missiles":
					#fire missiles from bases with a, s, d. First make sure that there are enough missiles left in the base
					if event.key == pygame.K_a:
						if (self.bases[0].count > 0):
							self.bases[0].count = self.bases[0].count - 1
							missile = Missile(self.bases[0].rect.centerx, self.size[1] - self.city_width, pos[0], pos[1], self.missile_speed, self)
							self.missiles.append(missile)
					
					if event.key == pygame.K_s:
						if (self.bases[1].count > 0):
							self.bases[1].count = self.bases[1].count - 1
							missile = Missile(self.bases[1].rect.centerx, self.size[1] - self.city_width, pos[0], pos[1], self.missile_speed, self)
							self.missiles.append(missile)

					if event.key == pygame.K_d:
						if (self.bases[2].count > 0):
							self.bases[2].count = self.bases[2].count - 1
							missile = Missile(self.bases[2].rect.centerx, self.size[1] - self.city_width, pos[0], pos[1], self.missile_speed, self)
							self.missiles.append(missile)

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
