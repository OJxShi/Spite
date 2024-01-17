import config
from config import *

class Button:
    def __init__(self,x,y,w,h,text,
                 text_colour=(255,255,255),button_colour=(100,0,0),
                visible=True):
        self.rect = pygame.Rect(x,y,w,h)
        self.text = pygame.font.SysFont("Trebuchet MS",int(h*0.7)).render(text,True,text_colour)
        self.colour = button_colour
        self.visible = visible
    
    def upon_clicked(self):
        return True
    
    def update(self):
        pass
    
    def draw(self):
        if self.visible:
            pygame.draw.rect(screen,self.colour,self.rect)
            screen.blit(self.text,(self.rect.x,self.rect.y+self.rect.height*0.1))