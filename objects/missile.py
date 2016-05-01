import pygame
from pygame.locals import *
from math import atan2, sin, cos

class Missile(pygame.sprite.Sprite):

	def __init__(self, sx, sy, fx, fy, v, source, gs=None):

		pygame.sprite.Sprite.__init__(self)
		self.TYPE = "Missile"
		self.gs = gs
		self.pos = sx, sy
		self.start = sx, sy
		self.fx = fx
		self.fy = fy
		self.da = 1
		self.source = source

		#calculate dx and dy
		angle = atan2(sy - fy, sx - fx)
		self.dx = -1 * v * cos(angle)
		self.dy = -1 * v * sin(angle)

	def tick(self):

		#update x and y positions
		x = self.pos[0] + self.dx
		y = self.pos[1] + self.dy

		self.pos = x, y

		#if missile has reached its destination, it should die
		if (self.pos[1] <= self.fy):
			self.da = 0

	def draw(self):
		pygame.draw.line(self.gs.screen, (0, 204, 204), self.start, self.pos)

class Bomb(Missile):

	def __init__(self, sx, sy, fx, fy, v, dest, gs=None):
		Missile.__init__(self, sx, sy, fx, fy, v, gs)

		self.dest = dest #destination (0-8) of bomb
		self.TYPE = "Bomb"

	def tick(self):

		#update x and y positions
		x = self.pos[0] + self.dx
		y = self.pos[1] + self.dy

		self.pos = x, y

		#if missile has reached its destination, it should die
		if (self.pos[1] >= self.fy):
			self.da = 0
	def draw(self):
		pygame.draw.line(self.gs.screen, (133, 255, 10), self.start, self.pos)
