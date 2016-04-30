import pygame
from pygame.locals import *
import sys
from city import City, Base
from missile import Missile
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

		while 1:
			#click tick
			self.clock.tick(60)

			#handle events
			self.handle_events()

			#tick updates
			self.ticks()

			#draw images
			self.draw_images()


	def draw_images(self):
		#black screen
		black = 0, 0, 0
		self.screen.fill(black)

		#draw cities
		for city in self.cities:
			city.draw()

		for base in self.bases:
			base.draw()

		for missile in self.missiles:
			missile.draw()

		for explosion in self.explosions:
			explosion.draw()

		for bomb in self.bombs:
			bomb.draw()

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
		while (i < len(self.bombs)):
			self.bombs[i].tick()

			#check if bomb is dead; if so, pop off of list
			if (self.bombs[i].da == 0):
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

				#if 1-9 pressed, set off bomb
				if event.key == pygame.K_1:
					bomb = Missile(pos[0], 0, self.bases[0].rect.centerx, self.size[1] - self.city_width, 1, "bomb", self)
					self.bombs.append(bomb)

				if event.key == pygame.K_2:
					bomb = Missile(pos[0], 0, self.cities[0].rect.centerx, self.size[1] - self.city_width, 3, "bomb", self)
					self.bombs.append(bomb)

				if event.key == pygame.K_3:
					bomb = Missile(pos[0], 0, self.cities[1].rect.centerx, self.size[1] - self.city_width, 3, "bomb", self)
					self.bombs.append(bomb)

				if event.key == pygame.K_4:
					bomb = Missile(pos[0], 0, self.cities[2].rect.centerx, self.size[1] - self.city_width, 3, "bomb",self)
					self.bombs.append(bomb)

				if event.key == pygame.K_5:
					bomb = Missile(pos[0], 0, self.bases[1].rect.centerx, self.size[1] - self.city_width, 3, "bomb",self)
					self.bombs.append(bomb)

				if event.key == pygame.K_6:
					bomb = Missile(pos[0], 0, self.cities[3].rect.centerx, self.size[1] - self.city_width, 3, "bomb",self)
					self.bombs.append(bomb)

				if event.key == pygame.K_7:
					bomb = Missile(pos[0], 0, self.cities[4].rect.centerx, self.size[1] - self.city_width, 3, "bomb",self)
					self.bombs.append(bomb)

				if event.key == pygame.K_8:
					bomb = Missile(pos[0], 0, self.cities[5].rect.centerx, self.size[1] - self.city_width, 3, "bomb",self)
					self.bombs.append(bomb)

				if event.key == pygame.K_9:
					bomb = Missile(pos[0], 0, self.bases[2].rect.centerx, self.size[1] - self.city_width, 3, "bomb",self)
					self.bombs.append(bomb)


				#fire missiles from bases with a, s, d. First make sure that there are enough missiles left in the base
				if event.key == pygame.K_a:
					if (self.bases[0].count > 0):
						self.bases[0].count = self.bases[0].count - 1
						missile = Missile(self.bases[0].rect.centerx, self.size[1] - self.city_width, pos[0], pos[1], 3, "missile", self)
						self.missiles.append(missile)
				
				if event.key == pygame.K_s:
					if (self.bases[1].count > 0):
						self.bases[1].count = self.bases[1].count - 1
						missile = Missile(self.bases[1].rect.centerx, self.size[1] - self.city_width, pos[0], pos[1], 3, "missile", self)
						self.missiles.append(missile)

				if event.key == pygame.K_d:
					if (self.bases[2].count > 0):
						self.bases[2].count = self.bases[2].count - 1
						missile = Missile(self.bases[2].rect.centerx, self.size[1] - self.city_width, pos[0], pos[1], 3, "missile", self)
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
