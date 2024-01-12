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

particle_list = []        