#! /usr/bin/env python

#import os, sys
import pygame
from pygame.locals import *
from helpers import *
import math
import time

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

points = 0
y_pos=400
x_pos=250
delta_t = 5
clock = pygame.time.Clock()
last_time = 0

class PyManMain:
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
            clock.tick(60)
            global last_time
            # print 'Last ',last_time
            # print 'Current ',pygame.time.get_ticks()/1000.0
            delta_t = (pygame.time.get_ticks()/1000.0 -last_time)
            last_time = delta_t
            #last_update_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == KEYDOWN:
                    if ((event.key == K_SPACE)
                    or (event.key == K_RIGHT)
                    or (event.key == K_LEFT)
                    or (event.key == K_DOWN)
                    or (event.key == K_UP)):
                        self.bird.move(event.key,delta_t)
            
            """Check for collision"""
            lstCols = pygame.sprite.spritecollide(self.bird, self.dart_sprites, True)
            global points
            points = points + 90*len(lstCols)

            self.bird_sprites.draw(self.screen)
            pygame.display.flip()

            """Do the Drawing"""               
            self.screen.blit(self.background, (0, 0))   
            if pygame.font:
                font = pygame.font.Font(None, 36)
                text = font.render("Score %s" % points, 1, (255, 0, 0))
                textpos = text.get_rect(centerx=self.background.get_width()/2)
                self.screen.blit(text, textpos)

            self.bird_sprites.draw(self.screen)
            self.dot_sprites.draw(self.screen)
            self.dart_sprites.draw(self.screen)
            #Physics().draw(self.screen)
            pygame.display.flip()
                    
    def LoadSprites(self):
        self.bird = Bird()
        self.bird_sprites = pygame.sprite.RenderPlain((self.bird))
        

        self.dart = Dart()
        self.dart_sprites = pygame.sprite.RenderPlain((self.dart))

        self.dot = Dot()
        self.dot_sprites = pygame.sprite.RenderPlain((self.dot))
           
class Bird(pygame.sprite.Sprite):
    """This is our bird that will move around the screen"""
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image, self.rect = load_image('angry_bird.png',-1)
        self.x_dist = 1
        self.y_dist = 1
        self.rect.center = (x_pos,y_pos)
        self.v_x = 0
        self.v_y = 0
        
    def move(self, key, delta_t):
        """Move yourself in one of the 4 directions according to key"""
        xMove = 0;
        yMove = 0;
        global x_pos
        global y_pos
        global last_time
        #rot_image,new_rect = load_image('angry_bird.png',-1)
        if (key == K_RIGHT):
            xMove = self.x_dist
            x_pos+=xMove
        elif (key == K_LEFT):
            xMove = -self.x_dist
            x_pos+=xMove
        elif (key == K_UP):
            yMove = -self.y_dist
            y_pos+=yMove
            """self.image = pygame.transform.rotate(rot_image,50)
            self.rect = self.image.get_rect(center=self.rect.center)"""
        elif (key == K_DOWN):
            yMove = self.y_dist
            y_pos+=yMove
            """self.image = pygame.transform.rotate(rot_image,-5)
            self.rect = self.image.get_rect(center=self.rect.center)"""
        elif (key == K_SPACE):
            #calculate velocity, etc
            dots = Dot()
            y_mag = dots.rect.center[1]-y_pos
            x_mag = dots.rect.center[0]-x_pos
            if x_mag == 0:
                x_mag = 0.001
            angle = -math.atan(float(y_mag)/x_mag)
            print 'Delta ',delta_t
            xMove += x_mag*delta_t 
            yMove += y_mag*delta_t-(5*delta_t**2)
            self.v_y += delta_t*50
            last_time = delta_t

        self.rect = self.rect.move(xMove,yMove)

class Physics:
    def __init__(self,rect=None):
        birdy = Bird()
        dots = Dot()
        pmm = PyManMain()
        pmm.MainLoop()
        pygame.draw.line(pmm.screen,[0,255,0],dots.rect.center,birdy.rect.center)

class Dart(pygame.sprite.Sprite):
    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self) 
        self.image, self.rect = load_image('eye.png',-1)
        self.rect.center = (750,400)
        
class Dot(pygame.sprite.Sprite):
     
    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self) 
        self.image, self.rect = load_image('Center.png',-1)
        self.rect.center = (250,400)

if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()