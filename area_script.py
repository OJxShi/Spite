import pygame, config, camera_script, collision_script, interactable_objects_script, particle_effects_script
from pygame.locals import *
from config import *
from camera_script import *
from collision_script import *
from interactable_objects_script import *
from particle_effects_script import *

def load_area(area):
    global collision_list,item_list
    collision_list.clear()
    item_list.clear()

    if area == 0:
        load_area_from_file("default")
#         collision_list.append(CollisionObject(0,575,1000,100))
#         collision_list.append(CollisionObject(50,100,100,300))
#         collision_list.append(CollisionObject(800,400,100,70))
#         collision_list.append(CollisionObject(700,500,100,50))
#         collision_list.append(CollisionObject(300,270,400,50))
#         collision_list.append(CollisionObject(150,200,100,100))
#         collision_list.append(CollisionObject(-100,1200,1500,50))
        item_list.append(AreaChanger(500,1100,100,100,50,0))


    else:
        collision_list.append(CollisionObject(0,575,1000,100))
        item_list.append(AreaChanger(500,500,100,150,50,0))

def load_area_from_file(file_name):
    global collision_list,item_list,objects_list
    try:
        file = open(f"custom levels/{file_name}.txt")
    except FileNotFoundError:
        file = open(f"custom levels/default.txt")
    
    for line in file:
        id, data = line.split(":")
        if id == "c":
            c = [int(coord) for coord in data.split(",")]
            collision_list.append(CollisionObject(c[0],c[1],c[2],c[3]))
        elif id == "d":
            c = [int(coord) for coord in data.split(",")]
            objects_list.append(DamagingObject(c[0],c[1],c[2],c[3]))
    
    file.close()

def draw_area():
    grid = 50
    for x in range(-grid,WIDTH+grid,grid):
        pygame.draw.line(screen,(75,75,75),(x-camera.x%grid,0),(x-camera.x%grid,HEIGHT),1)
    for y in range(-grid,HEIGHT+grid,grid):
        pygame.draw.line(screen,(75,75,75),(0,y-camera.y%grid),(WIDTH,y-camera.y%grid),1)
    for object in objects_list:
        object.draw()
    
    draw_colliders()
    draw_items()
    # draw_particles()

def update_area():
    update_particles()
    for item in item_list:
        item.update()

current_area = 0

class AreaChanger(InteractableObject):
    def __init__(self,x=500,y=1100,w=100,h=100,interactRange=50,destination=0,coords=(640,500)):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x,y,w,h)
        self.interactRect = pygame.Rect(x,y,w+interactRange,h+interactRange)
        self.rect.center = (self.x, self.y)
        self.interactRect.center = (self.x, self.y)
        self.destination = destination
        self.coords = coords
        
    def interact(self):
        load_area(self.destination)
        player.x, player.y = self.coords
        camera.focus(player.x,player.y,1)