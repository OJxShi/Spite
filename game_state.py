import pygame, config, interface
from pygame.locals import *
from config import *
from interface import *

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Big thank you to my dad for telling me to do this :thumbs_up:

class GameState():
    def __init__(self):
        self.next_state = None
        
    def enter(self):
        self.next_state = None
                
    def event_handle(self,event):
        pass
        
    def update(self):
        pass
        
    def draw(self):
        pass
        
    def exit(self):
        pass


class MainMenu(GameState):
    def __init__(self):
        super().__init__()
        self.title_font = pygame.font.SysFont('Trebuchet MS', 100)
        self.button_font = pygame.font.SysFont('Trebuchet MS', 60)
        self.title_text = self.title_font.render("title", True, (255,255,255))
        
        self.x = 0
        self.title_text_x = 0
        self.button_text_x = [0,0,0,0]
        self.exiting = False
        self.next_state_stored = "Playing"
        
        self.buttons = [
            Button(-25,285,350,90,"New Game"),
            Button(-25,385,350,90,"Load Game"),
            Button(-25,485,350,90,"Settings"),
            Button(-25,585,350,90,"Quit")
        ]
    
    def enter(self):
        self.x = 0
        self.exiting = False
        self.next_state_stored = "Playing"
    
    def event_handle(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.exiting:
                for i, button in enumerate(self.buttons):
                    if button.rect.collidepoint(event.pos):
                        if button.upon_clicked():
                            if i == 0:
                                self.next_state_stored = "Playing"
                            elif i == 1:
                                self.next_state_stored = "Save Screen"
                            elif i == 2:
                                self.next_state_stored = "Pause"
                            elif i == 3:
                                self.next_state_stored = "Quit"
                            self.exiting = True
                            
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.next_state = "Quit"
                return True
                
    def update(self):
        if self.exiting:
            self.x -= 5
            if self.x < 15:
                self.title_text_x = round((-1)*(self.x-10)**2+64)
            for i in range(len(self.button_text_x)):
                if self.x <(20+i*5):
                    self.buttons[i].rect.x = round((-1.5)*(self.x-(15+i*5))**2+59)
            if self.x < -20:
                self.next_state = self.next_state_stored
                
        
        if self.x <= 35:
            self.x += 1
            if self.x < 15:
                self.title_text_x = round((-1)*(self.x-10)**2+64)
            for i, buttons in enumerate(self.buttons):
                if self.x <(20+i*5):
                    self.buttons[i].rect.x = round((-1.5)*(self.x-(15+i*5))**2+59)
    
    def draw(self):
        screen.fill((0,0,0))
        screen.blit(self.title_text,(self.title_text_x,100))
        
        for button in self.buttons:
            button.draw()    
 

class SaveScreen(GameState):
    def __init__(self):
        super().__init__()
    
    def event_handle(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:  
            self.next_state = "Main Menu"  
        

active_keys = set()
            
    