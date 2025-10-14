import pygame as py
import math 
import random as r
import sys

# variable responsible for running the game
game = True

class Assets:
    #basic and necessary assets of pygame
    
    #initializing dimensions of the window. 
    __WIDTH = 1500
    __HEIGHT = 600
    
    #initializing window
    _window = py.display.set_mode((__WIDTH,__HEIGHT))

    def __init__(self):
        py.display.set_caption("Flappy Bird")
        self.__clock = py.time.Clock()
        self.__FPS = 60
        
        

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
        return Assets.__WIDTH

    @width.setter
    def width(self,value):
        if value <= 600:
            Assets.__WIDTH = 600
        else:
            Assets.width = value
    
    #window height
    @property
    def height(self):
        return Assets.__HEIGHT
    @height.setter
    def height(self,value):
        if value <= 60:
            Assets.__HEIGHT = 600
        else:
            Assets.__HEIGHT = value
    
            
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
            self._window.blit(self.bg,(int(i*self.bg.get_width()+self.scroll)-10,0))
        
        
class Bird(Background):
    def __init__(self):
        super().__init__()
        #bird image
        self.bird_og = py.image.load("src/pngwing.com(1).png").convert_alpha()
        
        #bird co-ords
        self.bird_x = 400
        self.__bird_y = 0
        
        
        
        self.impulse = -5
        
        #smooth motion
        self.gravity = 0.3
        self.velocity = 0
        
        self.bird_scale()
        
            
    @property
    def bird_y(self):
        return self.__bird_y
    
    @bird_y.setter
    def bird_y(self,val):
        #ensuring bird remains within window limits
        if self.__bird_y +self.h+70 >= self.height:
            self.__bird_y = self.height -self.h -70
            self.velocity =0
        elif self.__bird_y <0:
            self.__bird_y = 0
            self.velocity =0
        else:
            self.__bird_y = val
    
    def bird_scale(self):
        #scaling down bird image
        self.w = int(self.bird_og.get_width()*0.13)
        self.h = int(self.bird_og.get_height()*0.13)
        
        self.bird = py.transform.scale(self.bird_og,(self.w,self.h))
        
        
    def draw_bird (self):
        self.__bird_y = int(self.bird_y)
        self.jump(False)
        self._window.blit(self.bird,(self.bird_x,self.bird_y))
        self._bird_rect = self.bird.get_rect(topleft=(self.bird_x,self.bird_y)) #type:ignore
    
    @property
    def bird_rect(self):
        return self._bird_rect 
    
    #constantly free falling bird using gravity for smoother transition
    def fall(self):
            self.velocity += self.gravity
            self.bird_y += self.velocity
        
    
    #FLAPPY bird.
    def jump(self,bool):
        if bool:
            
            self.velocity += self.impulse
            self.__bird_y += self.velocity
        else:
            
            self.fall()
                
            
class Pipes(Bird):
    
    def __init__(self):
        
        #pipe image
        self.pipe = py.image.load("src/Pi7_cropper(1).png").convert_alpha()
        #upside down pipe image
        self.pipe_up = py.transform.rotate(self.pipe,180)
        
        #for point keeping
        self.coin = py.image.load("src/coin.png").convert_alpha()
        self.collected = False
        
        #spawn rate = how far apart will each pipe/obstacle be. 
        self.spawn_rate = 100      
        #speed of the pipes moving in the x direction
        self.x_speed = -5
        #x-coord of the pipe
        self.p_x = Assets().width+self.spawn_rate
        
        self.p_w = int(self.pipe.get_width()*0.5)
        self.p_h = self.pipe.get_height()
        #top co-ordinate of the inverted pipe
        self.h_factor =  -int(self.pipe.get_height()) +r.randint(0,426)
        
        #function to scale pipes according to y coords
        self.pipet()

    def pipet(self):
        #scaling bottom pipe so the bottom ends above the green line in the background
        s = (-138-self.h_factor)/self.p_h
        #scaling upper pipe for look purposes
        s_up = (self.h_factor+self.p_h)/self.p_h
        
        self.pipe = py.transform.scale(self.pipe,(self.p_w,int(self.p_h*s)))
        self.pipe_up = py.transform.scale(self.pipe_up,(self.p_w,int(self.p_h*s_up)))
        
        
        
    def draw_pipe(self):
        
        self._window.blit(self.pipe_up,(self.p_x,0))

        #blitting bottom pipe while ensuring a 100px gap between the pipes for the bird to pass through
        self._window.blit(self.pipe,(self.p_x,self.p_h+100+self.h_factor))
        
        self._window.blit(self.coin,(self.p_x+25,self.p_h+self.h_factor+30))
        
        self._coin_rect = self.coin.get_rect(topleft=(self.p_x+25,self.p_h+self.h_factor+30)) #type:ignore
        
        #moving pipes towards left.
        self.p_x += self.x_speed
    @property
    def coin_rect(self):
        return self._coin_rect
            
#class object to run game
new_game = Bird()
test = Pipes()
counter = 0  
pipes =[]

while game:
    counter +=1
    #getting events from pygame
    for event in py.event.get():
        
        #quit event
        if event.type == py.QUIT:
            game = False
            exit()
            
        if event.type == py.KEYDOWN:
            if event.key == py.K_SPACE:
                new_game.jump(True)
            if event.key == py.K_z:
                game=False
                py.time.wait(5000)
            
                

    
    #updating pygame display every Frame
    py.display.flip()
    new_game.draw_bg()
    
    if counter % 90 ==0 or counter ==1:
        pipes.append(Pipes())
    
    for pipe in pipes[:]:
        pipe.draw_pipe()
    
    
    new_game.draw_bird()
    #running game with defined FPS
    new_game.clock.tick(new_game.FPS)
    
new_game.draw_bg()
