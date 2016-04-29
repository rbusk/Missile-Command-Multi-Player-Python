import pygame
from pygame.locals import *

class City(pygame.sprite.Sprite):

	def __init__(self, x, y, h, w, gs=None):

		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.x = x
		self.y = y
		self.h = h
		self.w = w
		self.da = 1

		self.rect = Rect(self.x, self.y, self.h, self.w)

	def tick(self):
		pass

class Base(City):

	def __init__(self, x, y, h, w, count, gs=None):

		City.__init__(self, x, y, h, w, gs)
		self.count = count
