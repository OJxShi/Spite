import pygame,config,camera_script,animated_sprites_script,player_script
from config import *
from camera_script import *
from animated_sprites_script import AnimatedSprite
from player_script import player

class InteractableObject():
    def __init__(self,x=500,y=1100,w=100,h=100,interactRange=50):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x,y,w,h)
        self.interactRect = pygame.Rect(x,y,w+interactRange,h+interactRange)
        self.rect.center = (self.x, self.y)
        self.interactRect.center = (self.x, self.y)
    
    def check_in_range(self):
        if self.interactRect.colliderect(player.hitbox):
            self.interact()
    
    def interact(self):
        pass
    
    def draw(self):
        pygame.draw.rect(screen,(200,0,0),(self.interactRect.x - camera.x, self.interactRect.y - camera.y, self.interactRect.width, self.interactRect.height))
        pygame.draw.rect(screen,(0,0,200),(self.rect.x - camera.x, self.rect.y - camera.y, self.rect.width, self.rect.height))
    
    def update(self):
        pass
        
def interact_check():
    for item in item_list:
        item.check_in_range()

def draw_items():
    for i in range(len(item_list)):
        item_list[i].draw()

class TeleportObject(InteractableObject):
    def interact(self):
        player.y -= 1000
        
item_list = []
