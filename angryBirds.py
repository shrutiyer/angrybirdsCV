"""
An interactive AngryBirds game make with PyGame

@authors: Shruti Iyer and Kiki Chandra
"""

#! /usr/bin/env python

import sys
import pygame
from pygame.locals import *
from helpers import *
import random
from math import floor

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

last_time = 0
delta_t = 0
level = 0

class PyBirdMain:
    """The Main PyBird Class - This class handles the main 
    initialization and creating of the Game. It sets the screen size and includes the main loop of the game"""
    
    def __init__(self):

        #Initialize PyGame
        pygame.init()

        #Set the window Size
        self.width = 1000
        self.height = 800

        #Create the Screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.bird = Bird()
        self.points = 0
                           
    def MainLoop(self):
        """This is the Main Loop of the game. It load all of our sprites
        """
        self.LoadSprites();

        #tell pygame to keep sending up keystrokes when they are held down
        pygame.key.set_repeat(1,1)
        
        #Create the background
        self.background = pygame.image.load('background.png').convert()
        running = True
        while running:
            global last_time,delta_t
            delta_t = (pygame.time.get_ticks()/1000.0 -last_time)
            last_time = delta_t
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    running = False
                    break
                elif event.type == KEYDOWN: 
                    if self.bird.in_flight(): #Makes sure that once in flight, it doesn't accept inputs
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

            #Check for collision"""
            lstCols = pygame.sprite.spritecollide(self.bird, self.dart_sprites, False)
            self.points = self.points + 90*len(lstCols)
            if self.points >= 270:
                break

            #Checks for collisions and then updates the dart
            self.dart.move_dart()
            if lstCols:
                global level
                level+=1
                self.bird.lose_life = False
                self.dart.update()

            #Displays the fonts like score and lives remaining
            if pygame.font:
                font = pygame.font.Font(None, 54)
                text = font.render("Lives: %s" % self.bird.currentLives, 1, (255, 0, 0))
                textpos = text.get_rect(centerx=100,centery=40)
                self.screen.blit(text, textpos)
                text = font.render("Score: %s" % self.points, 1, (255, 0, 0))
                textpos = text.get_rect(centerx=890,centery=40)
                self.screen.blit(text, textpos)
            #Draws the sprites to the screen
            self.bird_sprites.draw(self.screen)
            self.dot_sprites.draw(self.screen)
            self.dart_sprites.draw(self.screen)
            pygame.display.flip()
            self.screen.blit(self.background, [0,0])

        pygame.quit()

    def LoadSprites(self):
        #Loads all the sprites (Bird, Dart and Dot)
        self.bird = Bird()
        self.bird_sprites = pygame.sprite.RenderPlain((self.bird))
        
        self.dart = Dart()
        self.dart_sprites = pygame.sprite.RenderPlain((self.dart))

        self.dot = Dot()
        self.dot_sprites = pygame.sprite.RenderPlain((self.dot))
           
class Bird(pygame.sprite.Sprite):
    """This is our bird that will move around the screen.
    attributes:
                x_pos, y_pos = initial position which also get updates
                x_dist, y_dist = Determines how fast the sprite moves when you press the arrow keys
                v_x, v_y = Velocities
                x_mag, y_mag = The distance between the bird and the blue dot (origin of sorts) 
                xMove, yMove = Updates the x_pos and y_pos
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.x_pos = 250
        self.y_pos = 400
        self.image, self.rect = load_image('angry_bird.png',-1) #Uses a helper function to load the image
        self.x_dist = 4
        self.y_dist = 4
        self.rect.center = (self.x_pos,self.y_pos)
        self.v_x = 0
        self.v_y = 0
        self.x_mag = 0
        self.y_mag = 0
        self.yMove = 0
        self.xMove = 0
        self.currentLives = 5 #Sets the number of lives to 5
        self.lose_life = True

    def move(self, key):
        """Tells what action should take place according to keyboard inputs.
        For various keystrokes, xMove updates the x_pos and y_pos"""
        
        global last_time
        if (key == K_RIGHT):
            self.xMove = self.x_dist
            self.x_pos=self.xMove
        elif (key == K_LEFT):
            self.xMove = -self.x_dist
            self.x_pos+=self.xMove
        elif (key == K_UP):
            self.yMove = -self.y_dist
            self.y_pos+=self.yMove
        elif (key == K_DOWN):
            self.yMove = self.y_dist
            self.y_pos+=self.yMove
        self.rect = self.rect.move(self.xMove,self.yMove)

    def launch(self):
        #calculate velocity, etc
        dots = Dot()
        self.y_mag = dots.rect.center[1]-self.y_pos
        self.x_mag = dots.rect.center[0]-self.x_pos
        if self.x_mag == 0:
            self.x_mag = 0.001
        self.xMove += self.x_mag 
        self.yMove += self.y_mag 
        self.v_x = self.x_mag*0.065
        self.v_y = self.y_mag*0.065
        self.rect = self.rect.move(self.xMove,self.yMove)
                
    def in_flight(self):
        return self.v_y != 0 #Defines what in_flight is in terms of velocity

    def reset(self):
        """This function resets the rect (bird) every time it goes out of the screen 
        and reduces a life.
        """
        self.rect.center = (250,400)
        self.v_x = 0
        self.v_y = 0
        self.x_pos = 250
        self.y_pos = 400
        if self.lose_life:
            self.currentLives-=1
            if self.currentLives == 0:
                pygame.quit()
        self.lose_life = True

    def update(self):
        """This function constantly updates the rectangle and also xMove and yMove.
        There are also boundary conditions on the dart rectangle to make sure it 
        always stays in the screen
        """
        self.xMove = self.v_x
        self.yMove = self.v_y
        self.rect = self.rect.move(self.xMove,self.yMove)
        if (self.rect.centerx > 1000) or (self.rect.centerx < 0) or (self.rect.centery > 800) or (self.rect.centery < 0):
            self.reset()
        if self.in_flight():
            self.v_y += 0.2
        pygame.time.delay(10)

class Dart(pygame.sprite.Sprite):
    """The red rectangle which is the dart in the game.
    We are using a png image as a sprite
    """    
    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self) 
        self.image, self.rect = load_image('eye.png',-1)
        self.rect.center = (800,400)
        self.delta = 1

    def update(self):
        self.rect.center = (750,200)

    def move_dart(self):
        """This function, depending on the level the player is on, changes the 
        way the red rectangle moves.
        delta is a variable that changes the x and y, hence changing the direction too
        There are also boundry conditions on the rectangle to make sure it remains inside 
        the screen
        """
        global level
        if level == 0:
            self.rect.centerx+=self.delta
            if self.rect.centerx >= 1000: 
               self.delta = -1
            elif self.rect.centerx < 500:
               self.delta = 1
        elif level == 1:
            self.rect.centery+=self.delta
            if self.rect.centery <= 150: 
               self.delta = 2
            elif self.rect.centery > 650:
               self.delta = -2
        elif level == 2:
            self.rect.centerx+=self.delta #To make changes in both x and y direction
            self.rect.centery+=self.delta
            if self.rect.centerx < 100 or self.rect.centery <= 100: 
                self.delta = random.randint(1,10) #adds random speeds to the motion
            elif self.rect.centerx >= 900 or self.rect.centery > 700:
                self.delta = -random.randint(1,10)
        
class Dot(pygame.sprite.Sprite):
    #The blue dot that acts like the origin in the game
    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self) 
        self.image, self.rect = load_image('Center.png',-1)
        self.rect.center = (250,400)

if __name__ == "__main__":
    MainWindow = PyBirdMain()
    MainWindow.MainLoop()

