import pygame
from pygame.locals import *
import sys
from city import City, Base
from missile import Missile, Bomb
from explosion import Explosion
from math import sqrt

class Gamespace(object):
	def main(self):

		#initialize
		pygame.init()
		self.size = width, height = 640, 480
		self.screen = pygame.display.set_mode(self.size)
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
		winner = 0

		while not winner:
			#click tick
			self.clock.tick(60)

			#handle events
			self.handle_events()

			#tick updates
			self.ticks()

			#draw images
			self.draw_images()

			winner = self.check_winner()

		print "game over, player", winner, "wins"


	def draw_images(self):
		#black screen
		black = 0, 0, 0
		self.screen.fill(black)

		#draw cities
		for city in self.cities:
			#only draw if alive
			if city.da == 1:
				city.draw()

		for base in self.bases:
			base.draw()

		for missile in self.missiles:
			missile.draw()

		for explosion in self.explosions:
			explosion.draw()

		for bomb in self.bombs:
			bomb.draw()

		for explosion in self.bomb_explosions:
			explosion.draw()

		pygame.display.flip()

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

	def handle_events(self):

		for event in pygame.event.get():

			#quit game
			if event.type == QUIT:
				sys.exit()

			if event.type == KEYDOWN:

				pos = pygame.mouse.get_pos()

				#if player still has bombs to drop
				if (self.nbombs < self.maxbombs):

					#if 1-9 pressed, set off bomb
					if event.key == pygame.K_1:
						bomb = Bomb(pos[0], 0, self.bases[0].rect.centerx, self.size[1] - self.city_width, 3, 0, self)
						self.bombs.append(bomb)
						self.nbombs = self.nbombs + 1

					if event.key == pygame.K_2:
						bomb = Bomb(pos[0], 0, self.cities[0].rect.centerx, self.size[1] - self.city_width, 3, 1, self)
						self.bombs.append(bomb)
						self.nbombs = self.nbombs + 1

					if event.key == pygame.K_3:
						bomb = Bomb(pos[0], 0, self.cities[1].rect.centerx, self.size[1] - self.city_width, 3, 2, self)
						self.bombs.append(bomb)
						self.nbombs = self.nbombs + 1

					if event.key == pygame.K_4:
						bomb = Bomb(pos[0], 0, self.cities[2].rect.centerx, self.size[1] - self.city_width, 3, 3, self)
						self.bombs.append(bomb)
						self.nbombs = self.nbombs + 1

					if event.key == pygame.K_5:
						bomb = Bomb(pos[0], 0, self.bases[1].rect.centerx, self.size[1] - self.city_width, 3, 4, self)
						self.bombs.append(bomb)
						self.nbombs = self.nbombs + 1

					if event.key == pygame.K_6:
						bomb = Bomb(pos[0], 0, self.cities[3].rect.centerx, self.size[1] - self.city_width, 3, 5, self)
						self.bombs.append(bomb)
						self.nbombs = self.nbombs + 1

					if event.key == pygame.K_7:
						bomb = Bomb(pos[0], 0, self.cities[4].rect.centerx, self.size[1] - self.city_width, 3, 6, self)
						self.bombs.append(bomb)
						self.nbombs = self.nbombs + 1

					if event.key == pygame.K_8:
						bomb = Bomb(pos[0], 0, self.cities[5].rect.centerx, self.size[1] - self.city_width, 3, 7, self)
						self.bombs.append(bomb)
						self.nbombs = self.nbombs + 1

					if event.key == pygame.K_9:
						bomb = Bomb(pos[0], 0, self.bases[2].rect.centerx, self.size[1] - self.city_width, 3, 8, self)
						self.bombs.append(bomb)
						self.nbombs = self.nbombs + 1

				#fire missiles from bases with a, s, d. First make sure that there are enough missiles left in the base
				if event.key == pygame.K_a:
					if (self.bases[0].count > 0):
						self.bases[0].count = self.bases[0].count - 1
						missile = Missile(self.bases[0].rect.centerx, self.size[1] - self.city_width, pos[0], pos[1], 3, self)
						self.missiles.append(missile)
				
				if event.key == pygame.K_s:
					if (self.bases[1].count > 0):
						self.bases[1].count = self.bases[1].count - 1
						missile = Missile(self.bases[1].rect.centerx, self.size[1] - self.city_width, pos[0], pos[1], 3, self)
						self.missiles.append(missile)

				if event.key == pygame.K_d:
					if (self.bases[2].count > 0):
						self.bases[2].count = self.bases[2].count - 1
						missile = Missile(self.bases[2].rect.centerx, self.size[1] - self.city_width, pos[0], pos[1], 3, self)
						self.missiles.append(missile)

	def check_collisions(self):

		for explosion in self.explosions:
			i = 0
			while (i < len(self.bombs)):
				#calculate distance from missile to explosion
				dx = explosion.pos[0] - self.bombs[i].pos[0]
				dy = explosion.pos[1] - self.bombs[i].pos[1]

				d = sqrt(dx*dx + dy*dy)

				if (explosion.r > d):
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
			return 2

		#if player 2 has dropped all of his bombs and all of them have exploded, then player 1 wins
		elif (self.nbombs >= self.maxbombs and len(self.bomb_explosions) == 0 and len(self.bombs) == 0):
			return 1

		else:
			return 0
