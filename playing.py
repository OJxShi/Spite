import pygame,math,random,config,game_state,player_script,area_script,interactable_objects_script
from pygame.locals import *
from config import *
from game_state import *
from player_script import *
from area_script import *
from interactable_objects_script import *

pygame.init()
pygame.font.init()
pygame.mixer.init()

class Playing(GameState):
    def __init__(self):
        super().__init__()
    
    def enter(self):
        global saving_game
        super().enter()
        if saving_game:
            self.draw()
            saving_game = False
            save_game()
    
    def event_handle(self,event):
        global active_keys, current_area
        if event.type == WINDOWFOCUSLOST:
            self.next_state = "Pause"
            return True
        if event.type == KEYDOWN:
            active_keys.add(event.key)
            if event.key == K_ESCAPE:
                self.next_state = "Pause"
                return True
            elif event.key == K_SPACE:
                interact_check()
        if event.type == KEYUP:
            if event.key in active_keys:
                active_keys.remove(event.key)
        if event.type == MOUSEBUTTONDOWN:
            pass
    
    def update(self):
        player.input(active_keys)
        player.update()
        
        update_area()
        
        camera.focus(player.x-640,player.y-450,0.15)
        camera.update()
    
    def draw(self):
        screen.fill((150,150,150))
#         screen.blit(miku,(100-camera.x,0-camera.y))
        draw_area()
        draw_items()
        player.draw()
        draw_particles()
        
#         pygame.draw.circle(screen,(0,0,0),(640,360),7)
#         pygame.draw.circle(screen,(255,255,255),(640,360),5)

class Pause(GameState):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont('Trebuchet MS', 80)
        self.pause_screen_text = self.font.render("Paused", True, (240,240,240))
    
    def event_handle(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
#             global saving_game
#             saving_game = True
            self.next_state = "Playing"
            return True
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.next_state = "Main Menu"
                return True
            active_keys.add(event.key)
        if event.type == KEYUP:
            if event.key in active_keys:
                active_keys.remove(event.key)
                     
    def draw(self):
        screen.fill((150,150,150))
#         screen.blit(miku,(100-camera.x,0-camera.y))
        draw_area()
        draw_items()
        player.draw()
        
        pygame.draw.rect(screen,(0,0,0),(0,0,350,720))
        screen.blit(screen_overlay,(0,0))
        screen.blit(self.pause_screen_text,(45,25))
            

def save_game():
    global save_1_icon
    save_surface = pygame.Surface((500,300))
    save_surface.blit(screen,(-player.x+camera.x+250,-player.y+camera.y+200))
    save_surface = pygame.transform.scale(save_surface,(250,150))
    pygame.image.save(save_surface,"Saves/save_1.jpg")
    save_1_icon = pygame.image.load("Saves/save_1.jpg")

miku = pygame.image.load("sprites/project voltage.jpeg")

screen_overlay = pygame.Surface((WIDTH, HEIGHT))
screen_overlay.fill((0,0,0))
screen_overlay.set_alpha(128)

try:
    save_1_icon = pygame.image.load("Saves/save_1.jpg")
except FileNotFoundError:
    save_1_icon = pygame.Surface((250,150))



saving_game = False

load_area(0)#current_area)
