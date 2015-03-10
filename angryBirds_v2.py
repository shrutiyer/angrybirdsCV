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

class PyGameWindowView():
    """ A view of angry birds rendered in a Pygame window """
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
        
    # def draw(self):
    #     self.screen.fill(pygame.Color(0,0,0))
    #     for brick in self.model.bricks:
    #         pygame.draw.rect(self.screen, pygame.Color(brick.color[0],brick.color[1],brick.color[2]),pygame.Rect(brick.x,brick.y,brick.width,brick.height))
    #     pygame.draw.rect(self.screen, pygame.Color(self.model.paddle.color[0],self.model.paddle.color[1],self.model.paddle.color[2]),pygame.Rect(self.model.paddle.x,self.model.paddle.y,self.model.paddle.width,self.model.paddle.height))     
    #     pygame.display.update()

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
        self.view = PyGameWindowView(self.model,screen)
        self.controller = PygameKeyboardController(self.model)

        running = True

        while running:
            screen.fill((255, 64, 64))
            screen.blit(img,(0,0))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                   controller.handle_keyboard_event(event)

            model.update()
            view.draw()
            time.sleep(.001)
        
        pygame.quit()

if __name__ == "__main__":
    angry = AngryBirds()
    angry.run()