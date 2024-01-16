import config,animated_sprites_script,collision_script, particle_effects_script,random,math
from config import *
from math import sqrt
from animated_sprites_script import *
from collision_script import *
from particle_effects_script import *

idle_left = pygame.image.load("sprites/idle leftN.png")
idle_right = pygame.image.load("sprites/idle rightN.png")

walk_right = pygame.image.load("sprites/walk rightN.png")
walk_left = pygame.transform.flip(walk_right,True,False)

numbers_sheet = pygame.image.load("sprites/numbers.png")

jump_right = pygame.image.load("sprites/jump.png")
jump_left = pygame.transform.flip(jump_right, True, False)

fall_right = pygame.image.load("sprites/fall.png")
fall_left = pygame.transform.flip(fall_right, True, False)

mid_right = pygame.image.load("sprites/mid.png")
mid_left = pygame.transform.flip(mid_right, True, False)

class Player(AnimatedSprite):
    def __init__(self):
        AnimatedSprite.__init__(self)
        #self.new_animation("idle",pygame.image.load("sprites/test.png"),(0,0),(32,32),3,5)
        self.new_animation("idle right",idle_right,(0,0),(65,160),10,3)
        self.new_animation("idle left",idle_left,(0,0),(65,160),10,3)
        self.new_animation("move right",walk_right,(0,0),(126,160),12,2,"idle right")
        self.new_animation("move left",walk_left,(0,0),(126,160),12,2,"idle left")
        #self.new_animation("move left",numbers_sheet,(100,0),(100,100),7,2,"idle left")
        
        self.new_animation("jump left",jump_left,(0,0),(54,165),4,2)
        self.new_animation("fall left",fall_left,(0,0),(90,165),6,2)
        self.new_animation("mid left",mid_left,(0,0),(90,165),6,1,"fall left")
        
        self.new_animation("jump right",jump_right,(0,0),(54,165),4,2)
        self.new_animation("fall right",fall_right,(0,0),(90,165),6,2)
        self.new_animation("mid right",mid_right,(0,0),(90,165),6,1,"fall right")
        
        self.hitbox = pygame.Rect(0,0,50,150)
        self.hurtbox = (0,0,0,0)
        self.hurtbox_rect = pygame.Rect(0,0,0,0)
        
        self.x = 640
        self.y = 500
        self.velx = 0
        self.vely = 0
        self.speed = 18
        self.moving = False
        self.grounded = True
        self.attacking_active = False
        self.direction = "right"
        self.animation_lock = 0
        self.hp = 100
        self.max_hp = 100
        self.immunity = 0
        
        self.set_animation("idle right")
    
    def input(self,keys):
        if self.animation_lock == 0:
            if config.controls["attack_S"] in keys:
                self.attack_s()
            if config.controls["attack_M"] in keys:
                self.attack_m()
            if config.controls["attack_L"] in keys:
                self.attack_l()
                
            if config.controls["jump"] in keys:
                self.jump()
            if config.controls["left"] in keys and config.controls["right"] not in keys:
                self.move(-self.speed)
            elif config.controls["right"] in keys and config.controls["left"] not in keys:  
                self.move(self.speed)
            else:
                self.moving = False
            if K_h in keys:
                self.hurt(10)
            elif K_j in keys:
                self.hp = 100
            
    def interact(self):
        pass
  
    def move(self,x):
        if x > 0:
            self.direction = "right"
        else:
            self.direction = "left"
            
        self.x += x
        self.moving = True
    
    def jump(self):
        if self.grounded:
            self.grounded = False
            self.vely = -75
            self.set_animation(f"jump {self.direction}")
    
    def attack_s(self):
        pass
    
    def attack_m(self):
        pass
        
    def attack_l(self):
        pass
    
    def hurt(self,dmg=0,dir="p",type=0,kb=(0,0)):
        global particle_list
        if self.immunity <= 0:
            self.hp -= dmg
            self.set_animation(f"damage {dir}")
            self.animation_lock = 5
            particle_list.append(DamageNumber(self.x+random.randrange(-50,50),self.y+random.randrange(-50,50),dmg))
            if "u" in dir:
                self.vely = max(self.vely-kb[1],-75)
            elif "d" in dir:
                self.vely = min(self.vely+kb[1],75)
            if "l" in dir:
                self.velx -= kb[0]
            elif "r" in dir:
                self.velx += kb[0]
            self.immunity = 10
       
    def align(self):
        self.hitbox.center = self.x,self.y
        self.hurtbox_rect.center = self.x+self.hurtbox[0],self.y+self.hurtbox[1]
        self.hurtbox_rect.width,self.hurtbox_rect.height = self.hurtbox[2:]
        self.rect.center = self.x,self.y

    def collidex(self): #kid codes worlds worst collision system, asked to leave cs class
        self.velx = round(self.velx * 0.9,2)
        self.x += self.velx
        self.align()
        c = self.hitbox.collidelist(collision_list)
        if c != -1:
            hit = collision_list[c]
            left_in = self.hitbox.left < hit.rect.right and self.hitbox.left > hit.rect.left
            right_in = self.hitbox.right > hit.rect.left and self.hitbox.right < hit.rect.right
            if left_in and not right_in:
                self.x = hit.rect.right + self.hitbox.width/2# + 0.5
            elif right_in and not left_in:
                self.x = hit.rect.left - self.hitbox.width/2# - 0.5
        
        
        for object in objects_list:
            if object.__class__ == DamagingObject and self.hitbox.colliderect(object.rect):
                if self.direction == "left":
                    self.hurt(random.randint(1,5),"ur",kb=(10,40))
                elif self.direction == "right":
                    self.hurt(random.randint(1,5),"ul",kb=(10,40))
        
        self.align()
        
    def collidey(self):
        self.vely = round(self.vely * 0.9,2)
        self.y += 30 + self.vely
        self.grounded = False
        self.align()
        c = self.hitbox.collidelist(collision_list)
        if c != -1:
            hit = collision_list[c]
            bottom_in = self.hitbox.bottom > hit.rect.top and self.hitbox.bottom < hit.rect.bottom
            top_in = self.hitbox.top > hit.rect.top and self.hitbox.top < hit.rect.bottom
            if bottom_in and not top_in:
                self.y = hit.rect.top - self.hitbox.height/2
                self.grounded = True
                self.vely = -20
            elif top_in and not bottom_in:
                self.y = hit.rect.bottom + self.hitbox.height/2
                self.vely = -20
        self.align()      
    
    def update_animation(self):
        global particle_list
        if not self.animation_lock:
            if not self.grounded:
                if self.vely >= -28:
                    self.set_animation(f"fall {self.direction}")
                elif self.vely >= -40:
                    if self.current_animation["name"][:4] != "fall":
                        self.set_animation(f"mid {self.direction}")
            elif self.moving:
                self.set_animation(f"move {self.direction}")
            else:
                self.set_animation(f"idle {self.direction}")
            
        self.align()
        AnimatedSprite.update(self)
    
    def update(self):
        self.collidex()
        self.collidey()
        self.update_animation()
        
        if self.animation_lock > 0: self.animation_lock -= 1
        self.immunity -= 1
        
        if self.hp > self.max_hp: self.hp = self.max_hp
        elif self.hp < 0: self.hp = 0

    def draw(self):
        pygame.draw.rect(screen,(63,200,0),(self.hitbox[0]-camera.x,self.hitbox[1]-camera.y,self.hitbox[2],self.hitbox[3]))
        AnimatedSprite.draw(self)
        bar_w = 60
        bar_h = 8
        n = self.hp/self.max_hp
        bar_c = (255*(1-n**2),255*(1-(n-1)**2),0)
        pygame.draw.rect(screen,(0,0,0),(self.x-camera.x-bar_w/2-1,self.y-camera.y-86-bar_h,bar_w+2,bar_h+2))
        pygame.draw.rect(screen,bar_c,(self.x-camera.x-bar_w/2,self.y-camera.y-85-bar_h,bar_w*(self.hp/self.max_hp),bar_h))


player = Player()  


class PlayerDamaging:
    pass       
        
