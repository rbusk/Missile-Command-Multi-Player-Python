import pygame
from pygame.locals import *
import sys
from city import City, Base
from missile import Missile

class Gamespace(object):
	def main(self):

		#initialize
		pygame.init()
		self.size = width, height = 640, 480
		self.screen = pygame.display.set_mode(self.size)
		self.clock = pygame.time.Clock()

		self.initialize_cities_bases()

		#active bombs and active missiles (empty at first)
		self.missiles = []
		missile = Missile(0, 0, 400, 400, 3, self)
		self.missiles.append(missile)
		self.bombs = []

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

		pygame.display.flip()

	def ticks(self):

		# call ticks for each object

		i = 0
		while (i < len(self.missiles)):
			self.missiles[i].tick()

			#check if missile is dead; if so, pop off of list
			if (self.missiles[i].da == 0):
				del self.missiles[i]
			else:
				i = i+1

	def handle_events(self):

		for event in pygame.event.get():

			#quit game
			if event.type == QUIT:
				sys.exit()

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
