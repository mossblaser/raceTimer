#!/usr/bin/python

import sys

import pygame
from pygame.locals import *

from race     import Race
from hardware import Hardware


class RaceTimer(object):
	
	
	LARGE_HEIGHT = 0.1
	SMALL_HEIGHT = 0.1
	
	BG_COLOUR = (0,0,0)
	TITLE_COLOUR = (255,255,255)
	
	CHECKER_BG_COLOUR = (30,30,30)
	CHECKER_FG_COLOUR = (200,200,200)
	
	@property
	def title_height(self):
		return int(RaceTimer.LARGE_HEIGHT * self.height)
	
	@property
	def text_height(self):
		return int(RaceTimer.SMALL_HEIGHT * self.height)
	
	
	def __init__(self, width, height):
		self.width  = width
		self.height = height
		
		pygame.display.set_mode((width, height))
		pygame.display.set_caption("Race Timer")
		
		self.screen = pygame.display.get_surface()
		
		# Setup fonts
		self.title_font = pygame.font.Font(pygame.font.match_font("Racer"), self.title_height)
		self.text_font = pygame.font.Font(None, self.text_height)
		
		# Strings
		self.title = self.title_font.render("RaceTimer", True, RaceTimer.TITLE_COLOUR)
		
		self.update()
	
	
	def update(self):
		# Clear the screen
		self.screen.fill(RaceTimer.BG_COLOUR)
		
		# Draw in the UI
		self.draw_title()
		
		# Display it
		pygame.display.flip()
	
	
	def draw_checkers(self, rect):
		pygame.draw.rect(self.screen, RaceTimer.CHECKER_BG_COLOUR, rect)
		
		height = int(rect.height * 0.8)
		gap = (rect.height - height) / 2
		
		fg = True
		
		x = rect.left
		while x < rect.right:
			if fg:
				c1,c2 = RaceTimer.CHECKER_FG_COLOUR, RaceTimer.CHECKER_BG_COLOUR
			else:
				c2,c1 = RaceTimer.CHECKER_FG_COLOUR, RaceTimer.CHECKER_BG_COLOUR
			fg = not fg
			
			pygame.draw.rect(self.screen, c1, Rect(x, rect.top + gap, height/2, height/2))
			pygame.draw.rect(self.screen, c2, Rect(x, rect.top + (height/2) + gap, height/2, height/2))
			x += height/2
	
	
	def draw_title(self):
		x = self.width / 2 - self.title.get_width() / 2
		y = self.title_height
		self.screen.blit(self.title, (x,y))
		
		gap = int(self.title_height * 0.1)
		self.draw_checkers(Rect(0,0,self.width,self.title_height-gap))
		self.draw_checkers(Rect(0,(self.title_height*2)+gap,self.width,self.title_height-gap))
	
	
	def on_event(self, event):
		pass


if __name__=="__main__":
	pygame.init()
	
	#h = Hardware("/dev/ttyUSB0")
	#r = Race([1,1])
	
	rt = RaceTimer(1024,768)
	
	while True:
		event = pygame.event.wait()
		if event.type == QUIT:
			sys.exit(0)
		else:
			rt.on_event(event)

