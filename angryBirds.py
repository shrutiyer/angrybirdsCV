#! /usr/bin/env python

#import os, sys
import pygame
from pygame.locals import *
from helpers import *
import math
import time
import random

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

points = 0
origin_x = 250
origin_y = 400
last_time = 0
height = 800
width = 1000
delta_t = 0
level = 0

class PyManMain:
    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self):
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        global height,width
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
        self.background = pygame.image.load('background.png').convert()
        # self.image, self.rect = load_image('background.png',-1)
        # self.background = pygame.Surface(self.screen.get_size())
        # self.background = self.background.convert()
        #self.background.fill((0,0,0))
        running = True
        while running:
            #clock.tick(60)
            global last_time,delta_t
            # print 'Last ',last_time
            # print 'Current ',pygame.time.get_ticks()/1000.0
            delta_t = (pygame.time.get_ticks()/1000.0 -last_time)
            last_time = delta_t
            #last_update_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    running = False
                    break
                elif event.type == KEYDOWN:
                    if self.bird.in_flight():
                        break
                    if ((event.key == K_SPACE)
                    or (event.key == K_RIGHT)
                    or (event.key == K_LEFT)
                    or (event.key == K_DOWN)
                    or (event.key == K_UP)):
                        self.bird.move(event.key)
                elif event.type == KEYUP:
                    if event.key == K_SPACE:
                        self.bird.launch()
            self.bird.update()

            """Check for collision"""
            lstCols = pygame.sprite.spritecollide(self.bird, self.dart_sprites, False)
            global points
            points = points + 90*len(lstCols)

            self.dart.move_dart()
            if lstCols:
                global level
                level+=1
                self.dart.update()

            """Do the Drawing"""               
            if pygame.font:
                font = pygame.font.Font(None, 36)
                text = font.render("Score %s" % points, 1, (255, 0, 0))
                textpos = text.get_rect(centerx=self.background.get_width()/2.0)
                self.screen.blit(text, textpos)

            self.bird_sprites.draw(self.screen)
            self.dot_sprites.draw(self.screen)
            self.dart_sprites.draw(self.screen)
            pygame.display.flip()
            self.screen.blit(self.background, [0,0])

        sys.QUIT()

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
        self.x_pos = 250
        self.y_pos = 400
        self.image, self.rect = load_image('angry_bird.png',-1)
        self.x_dist = 4
        self.y_dist = 4
        self.rect.center = (self.x_pos,self.y_pos)
        self.v_x = 0
        self.v_y = 0
        self.x_mag = 0
        self.y_mag = 0
        self.yMove = 0
        self.xMove = 0
        self.i = 0

    def move(self, key):
        """Move yourself in one of the 4 directions according to key"""
        self.i += 1
        #print "inside move "+ str(self.i)
        global last_time
        moveonce = True
        #rot_image,new_rect = load_image('angry_bird.png',-1)
        if (key == K_RIGHT):
            self.xMove = self.x_dist
            self.x_pos=self.xMove
        elif (key == K_LEFT):
            self.xMove = -self.x_dist
            self.x_pos+=self.xMove
        elif (key == K_UP):
            self.yMove = -self.y_dist
            self.y_pos+=self.yMove
            """self.image = pygame.transform.rotate(rot_image,50)
            self.rect = self.image.get_rect(center=self.rect.center)"""
        elif (key == K_DOWN):
            self.yMove = self.y_dist
            self.y_pos+=self.yMove
            """self.image = pygame.transform.rotate(rot_image,-5)
            self.rect = self.image.get_rect(center=self.rect.center)"""
        print "xpos and ypos ", self.x_pos, " ", self.y_pos
        # elif (key == K_SPACE):
        #     if moveonce:
        #         print 'x_mag is', self.x_mag, 'y_mag is', self.y_mag, 'self.yMove is', self.yMove, 'self.xMove is', self.xMove, 'v_y is', self.v_y, 'v_x is', self.v_x
            
        #         #calculate velocity, etc
        #         dots = Dot()
        #         self.y_mag = dots.rect.center[1]-self.y_pos
        #         self.x_mag = dots.rect.center[0]-self.x_pos
        #         if self.x_mag == 0:
        #             self.x_mag = 0.001
        #         #angle = -math.atan(float(y_mag)/x_mag)
        #         global delta_t,last_time
        #         self.xMove += self.x_mag*delta_t 
        #         self.yMove += self.y_mag*delta_t-(5*delta_t**2)
        #         #self.v_y -= delta_t*50\
        #         self.v_x = self.x_mag*0.05
        #         self.v_y = self.y_mag*0.05
        #         #print "LAUNCHING!"
        #         moveonce = False
        #         print 'x_mag is', self.x_mag, 'y_mag is', self.y_mag, 'self.yMove is', self.yMove, 'self.xMove is', self.xMove, 'v_y is', self.v_y, 'v_x is', self.v_x
        #     last_time = delta_t
            
        self.rect = self.rect.move(self.xMove,self.yMove)
        #print self.rect.center

    def launch(self):
        #calculate velocity, etc
        dots = Dot()
        self.y_mag = dots.rect.center[1]-self.y_pos
        self.x_mag = dots.rect.center[0]-self.x_pos
        if self.x_mag == 0:
            self.x_mag = 0.001
        #angle = -math.atan(float(y_mag)/x_mag)
        #global delta_t,last_time
        self.xMove += self.x_mag #*delta_t 
        self.yMove += self.y_mag #*delta_t-(5*delta_t**2)
        #self.v_y -= delta_t*50\
        self.v_x = self.x_mag*0.075
        self.v_y = self.y_mag*0.075
        #print "LAUNCHING!"
        self.rect = self.rect.move(self.xMove,self.yMove)
                
    def in_flight(self):
        return self.v_y != 0

    def reset(self):
        global origin_x,origin_y
        self.rect.center = (origin_x,origin_y)
        self.v_x = 0
        self.v_y = 0
        #self.xMove = 0
        # self.yMove = 0
        # self.y_mag = 0
        # self.x_mag = 0
        self.x_pos = 250
        self.y_pos = 400

    def update(self):
        self.xMove = self.v_x
        self.yMove = self.v_y
        self.rect = self.rect.move(self.xMove,self.yMove)
        global height,width
        if (self.rect.centerx > width) or (self.rect.centerx < 0) or (self.rect.centery > height) or (self.rect.centery < 0):
            print "inside reset"
            self.reset()
        if self.in_flight():
            self.v_y += 0.2
        pygame.time.delay(10)

class Dart(pygame.sprite.Sprite):
    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self) 
        self.image, self.rect = load_image('eye.png',-1)
        self.rect.center = (800,400)
        self.delta = 1

    def update(self):
        self.rect.center = (750,height/5)

    def move_dart(self):
        global level
        if level == 0:
            self.rect.centerx+=self.delta
            if self.rect.centerx >= width: 
               self.delta = -1
            elif self.rect.centerx < width/2:
               self.delta = 1
        elif level == 1:
            self.rect.centery+=self.delta
            if self.rect.centery <= height/5: 
               self.delta = 2
            elif self.rect.centery > (4*height)/5:
               self.delta = -2
        elif level == 2:
            rand_xy = random.choice[self.rect.centerx, self.rect.centery]
            rand_xy+=self.delta
            if rand_xy <= height/5: 
                self.delta = randint(1,5)
            elif rand_xy > (4*height)/5:
                self.delta = -randint(1,5)
        
class Dot(pygame.sprite.Sprite):     
    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self) 
        self.image, self.rect = load_image('Center.png',-1)
        self.rect.center = (250,400)

if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()

