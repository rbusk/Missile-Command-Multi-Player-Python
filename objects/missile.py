#Mary Connolly

import pygame
from pygame.locals import *
from math import atan2, sin, cos

class Missile(pygame.sprite.Sprite):
	"""class for shooting missiles"""
	def __init__(self, sx, sy, fx, fy, v, source, gs=None):
		"""Initialization function for Missile sets member variables."""

		pygame.sprite.Sprite.__init__(self)
		self.TYPE = "Missile"
		self.gs = gs #gamespace
		self.pos = sx, sy #current position of missile
		self.start = sx, sy #start position of missile
		self.fx = fx #final x position
		self.fy = fy #final y position
		self.da = 1 #dead or alive
		self.source = source #0-2, referring to which base the missile was shot from

		#calculate dx and dy
		angle = atan2(sy - fy, sx - fx)
		self.dx = -1 * v * cos(angle)
		self.dy = -1 * v * sin(angle)

	def tick(self):
		"""Tick function for Missile updates position and sets da to 0 if the missile has reached its destination."""

		#update x and y positions
		x = self.pos[0] + self.dx
		y = self.pos[1] + self.dy

		self.pos = x, y

		#if missile has reached its destination, it should die
		if (self.pos[1] <= self.fy):
			self.da = 0

	def draw(self):
		"""Draw Missile to screen."""
		pygame.draw.line(self.gs.screen, (0, 204, 204), self.start, self.pos)

class Bomb(Missile):
	"""Bomb class that inherites from missile"""

	def __init__(self, sx, sy, fx, fy, v, dest, gs=None):
		"""Init function for Bomb. Uses Missile's init function and also sets self.dest, the destination of the bomb."""

		Missile.__init__(self, sx, sy, fx, fy, v, gs)

		self.dest = dest #destination (0-8) of bomb
		self.TYPE = "Bomb"

	def tick(self):
		"""Tick function. Updates position and sets to dead if destination has been reached."""

		#update x and y positions
		x = self.pos[0] + self.dx
		y = self.pos[1] + self.dy

		self.pos = x, y

		#if missile has reached its destination, it should die
		if (self.pos[1] >= self.fy):
			self.da = 0

	def draw(self):
		"""Draw Bomb to screen."""
		pygame.draw.line(self.gs.screen, (133, 255, 10), self.start, self.pos)
