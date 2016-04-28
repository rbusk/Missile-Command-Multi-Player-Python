import pygame
from pygame.locals import *
import sys
from math import atan2, pi, degrees, sin, cos, sqrt

class Gamespace(object):
	def main(self):

		#initialize
		pygame.init()
		self.size = width, height = 640, 480
		self.screen = pygame.display.set_mode(self.size)
		self.clock = pygame.time.Clock()

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

		#self.screen.blit(self.earth.image, self.earth.rect)

		pygame.display.flip()

	def ticks(self):

		# call ticks for each object

		pass


			
		
	def handle_events(self):

		for event in pygame.event.get():

			#quit game
			if event.type == QUIT:
				sys.exit()
