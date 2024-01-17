import animated_sprites_script
from animated_sprites_script import *

dust_left = pygame.image.load("sprites/dust.png")
dust_right = pygame.transform.flip(dust_left,True,False)

class ParticleEffect(AnimatedSprite):
    def __init__(self,x=500,y=500):
        AnimatedSprite.__init__(self)
        self.x = x
        self.y = y
        self.lifespan = 30
        self.new_animation()
        self.set_animation("default")
    
    def update(self):
        self.align()
        AnimatedSprite.update(self)
        self.lifespan -= 1

def draw_particles():
    for particle in particle_list:
        particle.draw()

def update_particles():
    global particle_list
    i = 0
    particles_to_kill = []
    for particle in particle_list:
        particle.update()
        if particle.lifespan < 0:
            particles_to_kill.insert(0,i)
        i += 1
        
    for particle_index in particles_to_kill:
        particle_list.pop(particle_index)

class DamageNumber(ParticleEffect):
    def __init__(self,x=500,y=500,dmg=0,type=0,crit=False):
        super().__init__(x,y)
        self.size = 20
        self.font = pygame.font.SysFont("Arial",20,True,True)
        self.dmg = dmg
        self.text = self.font.render(str(dmg),True,(255,255,255))
        self.lifespan = 15
        self.rect = self.text.get_rect()
    
    def update(self):
        super().update()
        n = 15-self.lifespan
        size = -n*(n-13)/42.25*self.size
        self.font = pygame.font.SysFont("Arial",int(20+size),True,True)
        colour = 255#-(n*1/5)**3
        self.text = self.font.render(str(self.dmg),True,(colour,colour,colour))
        self.rect.center = (self.x,self.y)
    
    def draw(self):
        screen.blit(self.text,(self.rect.x-camera.x,self.rect.y-camera.y))
        

particle_list = []        