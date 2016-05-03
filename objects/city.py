#Mary Connolly
#classes for city and base

import pygame
from pygame.locals import *

class City(pygame.sprite.Sprite):
	"""class for city object"""

	def __init__(self, x, y, h, w, gs=None):
		"""initialization function for City. Sets variables passed into the constructor."""

		pygame.sprite.Sprite.__init__(self)

		self.gs = gs #gamespace
		self.x = x #x position of top left corner
		self.y = y #y position of top left corner
		self.h = h #height of city
		self.w = w #width of city
		self.da = 1 #dead or alive

		self.rect = Rect(self.x, self.y, self.h, self.w) #pygame rect

	def draw(self):
		"""Draw City to screen."""
		pygame.draw.rect(self.gs.screen, (0, 204, 204), self.rect)

class Base(City):
	"""class for Base object. Inherits from City."""

	def __init__(self, x, y, h, w, count, gs=None):
		"""initialization function for Base. Uses City's init function as well as sets self.count, as this is the one extra variable that Base has that City does not."""

		City.__init__(self, x, y, h, w, gs)
		self.count = count #number of missiles in city

	def draw(self):
		"""Draws the base to the screen as well as a number with the count (the number of missiles left.)"""
		pygame.draw.rect(self.gs.screen, (0, 0, 204), self.rect)

		#draw number of missiles left in base
		font = pygame.font.Font(None, 30)

		text = font.render(str(self.count), True, (0, 204, 204))
		text_pos = text.get_rect()
		text_pos.centerx = self.rect.centerx
		text_pos.centery = self.rect.centery
		self.gs.screen.blit(text, text_pos)
