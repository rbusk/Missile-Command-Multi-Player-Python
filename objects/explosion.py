import pygame
from pygame.locals import *
from math import atan2, sin, cos

class Explosion(pygame.sprite.Sprite):

	def __init__(self, x, y, dr, maxr, gs=None):

		pygame.sprite.Sprite.__init__(self)

		self.pos = x, y
		self.r = 1
		self.dr = dr
		self.maxr = maxr
		self.gs = gs
		self.da = 1

	def __getstate__(self):
		return {"pos": self.pos, "r": self.r, "dr": self.dr, "maxr": self.maxr, "da": self.da}

	def tick(self):

		#increase radius
		self.r = self.r + self.dr
		
		#if missile has reached max radius, it should be "dead"
		if (self.r > self.maxr):
			self.da = 0

	def draw(self):
		pygame.draw.circle(self.gs.screen, (204, 0, 0), self.pos, self.r)
