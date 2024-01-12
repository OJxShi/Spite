import pygame, config
from pygame.locals import *
from config import *

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
        
        self.button_0_text = self.button_font.render("New Game", True, (255,255,255))
        self.button_1_text = self.button_font.render("Load Game", True, (255,255,255))
        self.button_2_text = self.button_font.render("Settings", True, (255,255,255))
        self.button_3_text = self.button_font.render("Quit", True, (255,255,255))

        self.button_0_rect = pygame.Rect(self.button_text_x[0]-25,285,350,90)
        self.button_1_rect = pygame.Rect(self.button_text_x[1]-25,385,350,90)
        self.button_2_rect = pygame.Rect(self.button_text_x[2]-25,485,350,90)
        self.button_3_rect = pygame.Rect(self.button_text_x[3]-25,585,350,90)
    
    def enter(self):
        self.x = 0
        self.exiting = False
        self.next_state_stored = "Playing"
    
    def event_handle(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.exiting:
                if self.button_0_rect.collidepoint(event.pos):
                    self.next_state_stored = "Playing"
                    self.exiting = True
                if self.button_1_rect.collidepoint(event.pos):
                    #self.next_state_stored = "Save Screen"
                    self.exiting = True
                if self.button_2_rect.collidepoint(event.pos):
                    self.next_state_stored = "Pause"
                    self.exiting = True
                if self.button_3_rect.collidepoint(event.pos):
                    self.next_state = "Quit"
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
                    self.button_text_x[i] = round((-1.5)*(self.x-(15+i*5))**2+84)
            if self.x < -20:
                self.next_state = self.next_state_stored
                
        
        if self.x <= 35:
            self.x += 1
            if self.x < 15:
                self.title_text_x = round((-1)*(self.x-10)**2+64)
            for i in range(len(self.button_text_x)):
                if self.x <(20+i*5):
                    self.button_text_x[i] = round((-1.5)*(self.x-(15+i*5))**2+84)
        
        self.button_0_rect = pygame.Rect(self.button_text_x[0]-25,285,350,90)
        self.button_1_rect = pygame.Rect(self.button_text_x[1]-25,385,350,90)
        self.button_2_rect = pygame.Rect(self.button_text_x[2]-25,485,350,90)
        self.button_3_rect = pygame.Rect(self.button_text_x[3]-25,585,350,90)
    
    def draw(self):
        screen.fill((0,0,0))
        screen.blit(self.title_text,(self.title_text_x,100))
        screen.blit(self.button_0_text,(self.button_text_x[0],300))
        screen.blit(self.button_1_text,(self.button_text_x[1],400))
        screen.blit(self.button_2_text,(self.button_text_x[2],500))
        screen.blit(self.button_3_text,(self.button_text_x[3],600))      
 

class SaveScreen(GameState):
    def __init__(self):
        super().__init__()
    
    def event_handle(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:  
            self.next_state = "Main Menu"  
        

active_keys = set()
            
    