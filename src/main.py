import pygame as py
import math 
import random as r

# variable responsible for running the game
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
        self.draw_bird()
        
            
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
    point = 0
    collisions =0
    def __init__(self):
        
        #pipe image
        self.pipe = py.image.load("src/Pi7_cropper(1).png").convert_alpha()
        #upside down pipe image
        self.pipe_up = py.transform.rotate(self.pipe,180)
        
        #for point keeping
        self.coin = py.image.load("src/coin.png").convert_alpha()
        self.collected = False
        self.coll = False
        
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
        
        
    #drawing pipes/obstacles with a 100 px gap for bird to go through    
    def draw_pipe(self,obj):
        self._window.blit(self.pipe_up,(self.p_x,0))
        self._window.blit(self.pipe,(self.p_x,self.p_h+100+self.h_factor))
        
        self.pipe_up_rect = self.pipe_up.get_rect(topleft=(self.p_x,0))
        self.pipe_rect = self.pipe.get_rect(topleft=(self.p_x,self.p_h+100+self.h_factor))
        
        self.p_x += self.x_speed
        
        self.pointss(obj)
        return self.collision(obj)

        
    #drawing coins as collectable object as well as point keeping    
    def draw_coin(self,bool):
        if not bool:
            self._window.blit(self.coin,(self.p_x+25,self.p_h+self.h_factor+30))
            self._coin_rect = self.coin.get_rect(topleft=(self.p_x+25,self.p_h+self.h_factor+30)) #type:ignore
        
    #collision check + points update
    def pointss(self,obj):
        self.draw_coin(self.collected)
        if obj._bird_rect.colliderect(self._coin_rect) and not self.collected:
            self.collected = True
            Pipes.point +=1
            
    # collision check with pipes         
    def collision(self,obj):
        if (obj._bird_rect.colliderect(self.pipe_rect) or  obj._bird_rect.colliderect(self.pipe_up_rect)) and not self.coll:
            Pipes.collisions +=1
            self.coll = True
            return False  
        else: return True      
              
class Extra (Bird):
    
    def __init__(self):
        super().__init__()
        #for fonts.
        py.init()

        #mode select
        self._hard = py.image.load("src/Screenshot from 2025-10-15 13-55-37.png").convert_alpha()
        self.hard_bool = False

        self._easy = py.image.load("src/Screenshot from 2025-10-15 13-54-58.png").convert_alpha()
        self.easy_bool = True

        #start screen
        self.blur = py.image.load("src/Screenshot from 2025-10-15 14-24-54.png").convert()
        
        self.start= py.image.load("src/start.png").convert_alpha()
        self.start_bool = False
        self.font = py.font.SysFont("Arial",30)
        
        #image scaling
        self.scale()
        
    @property
    def easy(self):
        return self.easy_bool
    @property   
    def hard (self):
        return self.hard_bool
     
    def scale(self):
        self._easy = py.transform.scale(self._easy,(150,50))
        self._hard = py.transform.scale(self._hard,(150,50))
        self.blur = py.transform.scale(self.blur,(1600,700))
    
    #in game text for points       
    def point (self):
        return self.font.render(f"Points:{Pipes.point}",True,(0,0,0))
    
    #in game text for collision
    def collision(self):
            return self.font.render(f"Collision: {Pipes.collisions}",True,(0,0,0,))
    
    #start screen
    def blurred (self):
        instructions = self.font.render("Selected game mode will be invisible, please click on the mode to select accordingly.",True,(0,0,0))
        instructions1 = self.font.render("Press Space to flap",True,(0,0,0))
        instructions2 = self.font.render("Easy Mode is selected by default and is never ending.",True,(0,0,0))
        instructions4= self.font.render("Hard Mode will let you collide 3 times before game over.",True,(0,0,0))
        self._window.blit(self.blur,(-50,-50))
        self._window.blit(self.start,(675,250))
        self._window.blit(instructions,(300,0))
        self._window.blit(instructions1,(500,50))
        self._window.blit(instructions2,(500,100))
        self._window.blit(instructions4,(500,150))
        
        self.draw_extra()
    
    #mode select     
    def mode(self,pos):
        if self._easy.get_rect(topleft= (0,0)).collidepoint(pos):
            self.easy_bool = True
            self.hard_bool = False
        if self._hard.get_rect(topleft= (0,55)).collidepoint(pos):
            self.hard_bool = True
            self.easy_bool = False
        if self.start.get_rect(topleft=(675,250)).collidepoint(pos):
            #resetting to 0 for every game
            Pipes.collisions = 0
            Pipes.point = 0
            return True
    
    #selected game mode is hidden    
    def draw_extra(self):
        info = self.font.render(f"Press R to restart",True,(0,0,0))
        
        if self.easy_bool:
            self._window.blit(self._hard,(0,55))
            self._window.blit(info,(400,545))
            

        if self.hard_bool:
            self._window.blit(self._easy,(0,0))

        self._window.blit(self.point(),(0,545))
        self._window.blit(self.collision(),(130,545))

            
def main():
    # 1 pipe spawns every 80 frames, increasing difficulty reduces this amount by 10 (game fps =60)
    difficulty = 80
    
    new_game = Extra()
    counter = 0  
    pipes =[]
    game = False
    while True:
        counter +=1
        #getting events from pygame
        if not game:  
                new_game.blurred()
                for event in py.event.get():
                    if event.type == py.QUIT:
                        exit()
                        
                    if event.type == py.MOUSEBUTTONDOWN:
                        game = new_game.mode(event.pos)
        else:
            for event in py.event.get():
            
                #quit event
                if event.type == py.QUIT:
                    game = False
                    exit()
                    
                if event.type == py.KEYDOWN:
                    if event.key == py.K_SPACE:
                        new_game.jump(True)
                        
                    if event.key == py.K_r:
                        main()
                        return
                    
        #updating pygame display every Frame
        py.display.flip()
        new_game.draw_bg()
        if game:
            if counter % difficulty  ==0 :
                pipes.append(Pipes())
            
            for pipe in pipes[:]:
                if pipe.draw_pipe(new_game):
                    pass
                elif new_game.hard and Pipes.collisions >=3:
                    main()
                    return
                else: break
        if counter >= 1500:
            counter =0 
            difficulty -=10
            
        new_game.draw_bird()
        new_game.draw_extra()
        
        #running game with defined FPS
        new_game.clock.tick(new_game.FPS)
        
main()