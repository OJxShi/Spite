import pygame, config, camera_script
from pygame.locals import *
from config import *
from camera_script import *


class WorldObject:
    def __init__(self):
        self.selected = False
    
    def align(self):
        self.x1 = self.rect.x-camera.x
        self.y1 = self.rect.y-camera.y
        self.x2 = self.rect.x-camera.x+self.rect.width
        self.y2 = self.rect.y-camera.y+self.rect.height
        
    def draw_outlines(self,colour):
        pygame.draw.line(screen,colour,(self.x1,self.y1+2),(self.x2,self.y1+2),width=5)
        pygame.draw.line(screen,colour,(self.x2-2,self.y1),(self.x2-2,self.y2),width=5)
        pygame.draw.line(screen,colour,(self.x1,self.y2-2),(self.x2,self.y2-2),width=5)
        pygame.draw.line(screen,colour,(self.x1+2,self.y1),(self.x1+2,self.y2),width=5) 

class CollisionObject(WorldObject):
    def __init__(self,x,y,w,h):
        WorldObject.__init__(self)
        self.rect = pygame.Rect(x,y,w,h)
        self.colour = (0,70,200)
    
    def draw(self):
        WorldObject.align(self)
        if self.x1 <= 1480 and self.x2 >= -200 and self.y1 <= 920 and self.y2 >= -200:
            if self.selected:
                WorldObject.draw_outlines(self,(255,200,0)) 
            else:
                WorldObject.draw_outlines(self,(0,70,200)) 


class DamagingObject(WorldObject):
    def __init__(self,x,y,w,h):
        WorldObject.__init__(self)
        self.rect = pygame.Rect(x,y,w,h)
        
    def draw(self):
        WorldObject.align(self)
        if self.x1 <= 1480 and self.x2 >= -200 and self.y1 <= 920 and self.y2 >= -200:
            pygame.draw.rect(screen,(255,0,0),(self.x1,self.y1,self.rect.width,self.rect.height))    
            if self.selected:
                WorldObject.draw_outlines(self,(255,200,0)) 



def draw_colliders():
    for c in collision_list:
        c.draw()

collision_list = []
objects_list = []