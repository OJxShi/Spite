import pygame, config, camera_script
from pygame.locals import *
from config import *
from camera_script import *

class CollisionObject():
    def __init__(self,x,y,w,h):
        self.rect = pygame.Rect(x,y,w,h)
        self.selected = False
        self.colour = (0,70,200)
    
    def draw(self):
        x1 = self.rect.x-camera.x
        y1 = self.rect.y-camera.y
        x2 = self.rect.x-camera.x+self.rect.width
        y2 = self.rect.y-camera.y+self.rect.height
#             pygame.draw.rect(screen,(0,255,255),(self.rect[0]-camera.x,self.rect[1]-camera.y,self.rect[2],self.rect[3]))
        if x1 <= 1480 and x2 >= -200 and y1 <= 920 and y2 >= -200:
            pygame.draw.line(screen,self.colour,(x1,y1+2),(x2,y1+2),width=5)
            pygame.draw.line(screen,self.colour,(x2-2,y1),(x2-2,y2),width=5)
            pygame.draw.line(screen,self.colour,(x1,y2-2),(x2,y2-2),width=5)
            pygame.draw.line(screen,self.colour,(x1+2,y1),(x1+2,y2),width=5)       

def draw_colliders():
    for c in collision_list:
        c.draw()

collision_list = []