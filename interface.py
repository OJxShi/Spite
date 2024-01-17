import config
from config import *

class Button:
    def __init__(self,x,y,w,h,text,image=None,hover_text=None,
                 text_colour=(255,255,255),button_colour=(100,0,0),
                visible=True):
        self.rect = pygame.Rect(x,y,w,h)
        self.text = pygame.font.SysFont("Trebuchet MS",int(h*0.7)).render(text,True,text_colour)
        self.image = image
        if image:
            image_rect = image.get_rect()
            self.rect.width,self.rect.height = image_rect.width,image_rect.height
        self.colour = button_colour
        if hover_text:
            self.hover_text = pygame.font.SysFont("monospace",15).render(hover_text,True,(0,0,0))
            self.hover_text_width = self.hover_text.get_rect().width
        else:
            self.hover_text = None
        self.visible = visible
    
    def upon_clicked(self):
        return True
    
    def update(self):
        pass
    
    def hover(self,mouse_pos):
        if self.hover_text and self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen,(255,255,255),(mouse_pos[0],mouse_pos[1]-19,self.hover_text_width+4,19))
            screen.blit(self.hover_text,(mouse_pos[0]+2,mouse_pos[1]-17))
    
    def draw(self):
        if self.visible:
            pygame.draw.rect(screen,self.colour,self.rect)
            screen.blit(self.text,(self.rect.x,self.rect.y+self.rect.height*0.1))
