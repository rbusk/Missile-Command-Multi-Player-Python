import pygame
from pygame.locals import *
from math import atan2, sin, cos

class Missile(pygame.sprite.Sprite):

	def __init__(self, sx, sy, fx, fy, v, gs=None):

		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.pos = sx, sy
		self.start = sx, sy
		self.fy = fy
		self.da = 1

		#calculate dx and dy
		angle = atan2(sy - fy, sx - fx)
		self.dx = abs(v * cos(angle))
		self.dy = abs(v * sin(angle))

	def tick(self):

		#update x and y positions
		x = self.pos[0] + self.dx
		y = self.pos[1] + self.dy

		self.pos = x, y

		#if missile has reached its destination, it should 
		if (self.pos[0] >= self.fy):
			self.da = 0
