"""
Angry Birds"""

import pygame
from pygame.locals import *
import math
img = pygame.image.load('data/images/background.png')

class AngryModel():
    """ Represents the game state of our bird """
    def __init__(self, width, height):
        """ Initialize the flappy model """
        self.width = width
        self.height = height
        self.bird = Bird(width/8.0, height/2.0) #the position of the bird initially
        #self.background = Background(width, height)
        #self.dart = Dart()

    def update(self):
        self.bird.update()

class DrawableSurface():
    """ A class that wraps a pygame.Surface and a pygame.Rect """

    def __init__(self, surface, rect):
        """ Initialize the drawable surface """
        self.surface = surface
        self.rect = rect

    def get_surface(self):
        """ Get the surface """
        return self.surface

    def get_rect(self):
        """ Get the rect """
        return self.rect

class Bird():
    """This is our bird that will move around the screen"""
    def __init__(self,pos_x,pos_y):
        """ Initialize a Flappy bird at the specified position
            pos_x, pos_y """
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.v_x = 0
        self.v_y = 0
        self.image = pygame.image.load('data/images/angry_bird.png')
        self.image.set_colorkey((255,255,255))

    def update(self):
        """ update the flappy bird's position """
        self.pos_x += self.v_x
        self.pos_y += self.v_y
        #self.v_y += delta_t*100 # this is gravity in pixels / s^2

class PyGameWindowView():
    """ A view of angry birds rendered in a Pygame window """
    def __init__(self,model,width,height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.screen_boundaries = pygame.Rect(0 ,0, width, height)
        self.model = model
        
    def draw(self):
        self.screen.fill(pygame.Color(50,0,0))
        pygame.display.update()

class PyGameKeyboardController():
    """ Handles keyboard input for angrybirds"""
    def __init__(self,model):
        self.model = model
    
    def handle_keyboard_event(self,event):
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            self.model.bird.vx += -0.5
        if event.key == pygame.K_RIGHT:
            self.model.bird.vx += 0.5
        if event.key == pygame.K_UP:
            self.model.bird.vy += -0.5
        if event.key == pygame.K_DOWN:
            self.model.bird.vy += 0.5

class AngryBirds():
    """The main class of Angry Birds"""
    def __init__(self):
        """ Initialize the flappy bird game.  Use FlappyBird.run to
            start the game """
        size = (1280,846)
        screen = pygame.display.set_mode(size)
        self.model = AngryModel(1280,846)
        self.view = PyGameWindowView(self.model,1280,846)
        self.controller = PyGameKeyboardController(self.model)

    def run(self):
        frame_count = 0
        self.view.draw()
        for event in pygame.event.get():
            # if event.type == QUIT:
            #     running = False
            if event.type == KEYDOWN:
                self.controller.handle_keyboard_event()
        self.model.update()       

if __name__ == "__main__":
    angry = AngryBirds()
    angry.run()