#! /usr/bin/env python

import os, sys
import pygame
from pygame.locals import *
from helpers import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class PyManMain():
    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self, width=1000,height=800):
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width = width
        self.height = height
        """Create the Screen"""
        self.screen = pygame.display.set_mode((self.width, self.height))
                                                          
    def MainLoop(self):
        """This is the Main Loop of the Game"""
        
        """Load All of our Sprites"""
        self.LoadSprites();
        """tell pygame to keep sending up keystrokes when they are
        held down"""
        pygame.key.set_repeat(1,1)
        
        """Create the background"""
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == KEYDOWN:
                    if ((event.key == K_RIGHT)
                    or (event.key == K_LEFT)
                    or (event.key == K_UP)
                    or (event.key == K_DOWN)):
                        self.bird.move(event.key)
                        
                self.bird_sprites.draw(self.screen)
                pygame.display.flip()

                """Do the Drawing"""               
                self.screen.blit(self.background, (0, 0))    
                self.bird_sprites.draw(self.screen)
                pygame.display.flip()
                    
    def LoadSprites(self):
        self.bird = Bird()
        self.bird_sprites = pygame.sprite.RenderPlain((self.bird))
            
        
class Bird(pygame.sprite.Sprite):
    """This is our bird that will move around the screen"""
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image, self.rect = load_image('angry_bird.png',-1)
        self.x_dist = 5
        self.y_dist = 5 
        
    def move(self, key):
        """Move yourself in one of the 4 directions according to key"""
        xMove = 0;
        yMove = 0;
        
        if (key == K_RIGHT):
            xMove = self.x_dist
        elif (key == K_LEFT):
            xMove = -self.x_dist
        elif (key == K_UP):
            yMove = -self.y_dist
        elif (key == K_DOWN):
            yMove = self.y_dist
        self.rect = self.rect.move(xMove,yMove)
        
if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()