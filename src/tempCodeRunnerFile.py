import pygame as py
import math 
import random as r

# variable responsible for running the game
game = True

class Assets:
    #basic and necessary assets of pygame
    
    def __init__(self):
        py.display.set_caption("Flappy Bird")
        self.__clock = py.time.Clock()
        self.__FPS = 60
        self.__WIDTH = 1500
        self.__HEIGHT = 600
        self._window()

    #py clock
    @property
    def clock(self):
        return self.__clock
    
    #FPS
    @property
    def FPS(self):
        return self.__FPS
    
    @FPS.setter
    def FPS(self,value):
        if value <= 60:
            self.__FPS = 60
        else:
            self.__FPS = value
    
    #window width
    @property
    def width(self):
        return self.__WIDTH

    @width.setter
    def width(self,value):
        if value <= 600:
            self.__WIDTH = 600
        else:
            self.width = value
    
    #window height
    @property
    def height(self):
        return self.__HEIGHT
    @height.setter
    def height(self,value):
        if value <= 60:
            self.__HEIGHT = 600
        else:
            self.__HEIGHT = value
    
    # window itself
    @property
    def window(self):
        return self.__window
    
    #initializing pygame window
    def _window(self):
        self.__window = py.display.set_mode((self.width,self.height))
        
        
class Background(Assets):
    #everything with game background. 
    
    def __init__(self):
        #initialziing basic assets
        super().__init__()
        
        #loading bg image
        self.bg = py.image.load("src/bg.png").convert()
        
        #bg image co-ords
        self.bg_x = 0
        
        #ensuring right to left movement of the bg image
        self.__scroll = 0 
        
        
    
    @property
    def scroll(self):
        return self.__scroll
    
    @scroll.setter
    def scroll(self,value):
        if abs(self.__scroll) >= self.bg.get_width():
            self.__scroll = 0
        else:
            self.__scroll= value
        
    #drawing the background
    def draw_bg(self):
        for i in range(0,3):
            print(self.scroll)
            super().window.blit(self.bg,(i*self.bg_x+self.scroll,0))
        
        
#class object to run game
new_game = Background()  
 
       
while game:
    #getting events from pygame
    for event in py.event.get():
        
        #quit event
        if event.type == py.QUIT:
            game = False
            exit()
    
    #updating pygame display every Frame
    py.display.flip()
    
    new_game.scroll -=5 
    new_game.draw_bg()
    #running game with defined FPS
    new_game.clock.tick(new_game.FPS)