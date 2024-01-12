import pygame, config, camera_script
from pygame.locals import *
from config import *
from camera_script import *

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.animations = {}
        self.frame = 0
        self.animation_timer = 0
        self.animation_loop = True
        self.new_animation()
        self.x = 100
        self.y = 100
        self.current_animation = None
        
    def new_animation(self,name="default",image=pygame.image.load("sprites/default.png"),start=(0,0),dimensions=(100,100),frames=1,speed=1,end="default",offset=(0,0)):
        '''
        Creates a new animation for your sprite, from a spritesheet.
        '''
        animation = {"name":name,"spritesheet":image,"start":start,"dimensions":dimensions,"frames":frames,"speed":speed,"end":end,"offset":offset}
        self.animations[name] = animation
        
    def set_animation(self,anim="default",loop=-1,override=False):
        if anim not in self.animations:
            anim = "default"
        
        valid = True
        if self.current_animation:
            if self.current_animation["name"] == anim:
                valid = False
                
        if valid:
            self.frame = 0
            self.animation_timer = 0
            self.animation_loop = True
            self.current_animation = self.animations[anim]
            self.animation_loop = loop
            self.image = pygame.Surface(self.current_animation["dimensions"]).convert_alpha()
            self.rect = self.image.get_rect()
    
    def play_animation(self):
        '''
        Updates animation. Goes down vertically through the spritesheet.
        '''
        self.image.fill((0,0,0,0))
        self.image.blit(self.current_animation["spritesheet"],(-(self.current_animation["start"][0]),-(self.current_animation["start"][1]+self.current_animation["dimensions"][1]*self.frame)))
        self.align()
        self.animation_timer += 1
        if self.animation_timer == self.current_animation["speed"]:
            self.animation_timer = 0
            self.frame += 1
            if self.frame == self.current_animation["frames"]:
                if self.animation_loop == 0:
                    self.finish_animation()
                else:
                    self.animation_loop -= 1
                self.frame = 0
    
    def align(self):
        self.rect.center = self.x,self.y
    
    def finish_animation(self):
        self.set_animation(self.current_animation["end"])

    def draw(self):
#         pygame.draw.rect(screen, (255,255,255),(self.rect.x+self.current_animation["offset"][0]-camera.x, self.rect.y+self.current_animation["offset"][1]-camera.y,self.rect.width,self.rect.height),1)
        screen.blit(self.image,(self.rect.x+self.current_animation["offset"][0]-camera.x, self.rect.y+self.current_animation["offset"][1]-camera.y))
    
    def update(self):
        self.play_animation()
        
