#Mary Connolly

import pygame
from pygame.locals import *
from math import atan2, sin, cos

class Explosion(pygame.sprite.Sprite):
	"""Explosion class."""

	def __init__(self, x, y, dr, maxr, gs=None):
		"""Initialization function for Explosion. Sets member variables."""

		pygame.sprite.Sprite.__init__(self)

		self.pos = x, y #position of center
		self.r = 1 #radius
		self.dr = dr #change in radius
		self.maxr = maxr #max radius
		self.gs = gs #gamespace
		self.da = 1 #dead or alive

	def tick(self):
		"""Tick function for explosion. Increases the radius of the explosion by self.dr. If radius has reached max radius, da is set to dead."""

		#increase radius
		self.r = self.r + self.dr
		
		#if missile has reached max radius, it should be "dead"
		if (self.r > self.maxr):
			self.da = 0

	def draw(self):
		"""Draw Explosion to screen."""
		pygame.draw.circle(self.gs.screen, (204, 0, 0), self.pos, self.r)
