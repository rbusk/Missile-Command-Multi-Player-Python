import pygame
from pygame.locals import *
import sys

class City(pygame.sprite.Sprite):

	def __init__(self, x, y, h, w, da, gs=None):

		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.x = x
		self.y = y
		self.h = h
		self.w = w
		self.da = da

		self.rect = Rect(self.x, self.y, self.h, self.w)

	def tick(self):
		pass

class Base(City):

	def __init__(self, x, y, h, w, da, count, gs=None):

		City.__init__(self, x, y, h, w, da, gs)
		self.count = count
