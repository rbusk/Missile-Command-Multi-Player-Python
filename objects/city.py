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

	def draw(self):
		pygame.draw.rect(self.gs.screen, (255, 0 , 0), self.rect)

class Base(City):

	def __init__(self, x, y, h, w, count, gs=None):

		City.__init__(self, x, y, h, w, gs)
		self.count = count

	def draw(self):
		pygame.draw.rect(self.gs.screen, (0, 255, 0), self.rect)

		font = pygame.font.Font(None, 30)

		text = font.render(str(self.count), True, (0, 0, 255))
		text_pos = text.get_rect()
		text_pos.centerx = self.rect.centerx
		text_pos.centery = self.rect.centery
		self.gs.screen.blit(text, text_pos)
