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
        self.bg = py.image.load("src/Untitled design.png").convert()
        
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
        #scrolling / moving background image by 5 pixels every call
        self.scroll -=5
        
        #images required to fill the screen
        images = math.ceil(super().width / self.bg.get_width()) +1
        
        #blitting all the images necessary to fill the screen
        for i in range(0,images):
            self.window.blit(self.bg,(int(i*self.bg.get_width()+self.scroll)-10,0))
        
        
class Bird(Background):
    def __init__(self):
        super().__init__()
        #bird image
        self.bird_og = py.image.load("src/pngwing.com(1).png").convert_alpha()
        
        #bird co-ords
        self.bird_x = 400
        self.__bird_y = 0
        
        #scaling down bird image
        self.w = int(self.bird_og.get_width()*0.15)
        self.h = int(self.bird_og.get_height()*0.15)
        self.bird = py.transform.scale(self.bird_og,(self.w,self.h))
        
        #smooth motion
        self.gravity = 0.08
        self.velocity = 0
        
        
    @property
    def bird_y(self):
        return self.__bird_y
    
    @bird_y.setter
    def bird_y(self,val):
        #ensuring bird remains within window limits
        if self.__bird_y +self.h+50  >= self.height:
            self.__bird_y = self.height -self.h-50
            self.velocity =0
        elif self.__bird_y <0:
            self.__bird_y = 0
            self.velocity =0
        else:
            self.__bird_y = val
    
    
    def draw_bird (self):
        self.__bird_y = int(self.bird_y)
        print(self.bird_y)
        self.jump(False)
        self.window.blit(self.bird,(self.bird_x,self.bird_y))
        
        
    #constantly free falling bird using gravity for smoother transition
    def fall(self):
        self.velocity += self.gravity
        self.bird_y += self.velocity
    
    #FLAPPY bird.
    def jump(self,bool):
        if bool:
            self.velocity -= 5
            self.__bird_y += self.velocity
        else:
            self.fall()
            
            
            
#class object to run game
new_game = Bird()
 
       
while game:
    #getting events from pygame
    for event in py.event.get():
        
        #quit event
        if event.type == py.QUIT:
            game = False
            exit()
        if event.type == py.KEYDOWN:
            if event.key == py.K_SPACE:
                new_game.jump(True)
    
    #updating pygame display every Frame
    py.display.flip()
    
    new_game.draw_bg()
    new_game.draw_bird()
    #running game with defined FPS
    new_game.clock.tick(new_game.FPS)