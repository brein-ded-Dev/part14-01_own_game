import pygame as py
import math 
import random as r

py.display.set_caption("Flappy Bird")
clock = py.time.Clock()
FPS = 60


WIDTH = 1500
HEIGHT = 600
window = py.display.set_mode((WIDTH,HEIGHT))
game = True

class Background:
    def __init__(self):
        pass
         
         
while game:
    for event in py.event.get():
        if event.type == py.QUIT:
            game = False
            exit()
    
    clock.tick(FPS)