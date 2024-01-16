import pygame,collision_script,random,game_state#,area_script
from pygame import *
from collision_script import *
from game_state import GameState

pygame.init()
pygame.font.init()
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Custom Level Editor - Untitled Level')
clock = pygame.time.Clock()

DOUBLE_CLICK_COOLDOWN = 15
grid = 50
mouse_pos_font = pygame.font.SysFont("monospace",20)
button_hover_font = pygame.font.SysFont("Arial",20)
file_name_font = pygame.font.SysFont("Arial",30)
current_file_name = "Untitled Level"
mouse_down = False
snapping = False
last_mouse_click = 100
active_keys = set()
mouse_screen_pos = (0,0)
mouse_movement = 0
mouse_world_pos = (0,0)

bowling = pygame.image.load("level editor assets/bowling.png")
cm = pygame.image.load("level editor assets/custom mouse.png")
cm_point = pygame.image.load("level editor assets/custom mouse point.png")
cm_grab = pygame.image.load("level editor assets/custom mouse grab.png")
cm_grip = pygame.image.load("level editor assets/custom mouse grip.png")
cm_draw = pygame.image.load("level editor assets/custom mouse draw.png")

custom_mouse = cm


class Default(GameState):
    def __init__(self):
        super().__init__()
        self.buttons = [
            SAVE_BUTTON
        ]
        pygame.mouse.set_visible(False)
    def event_handle(self,event):
        if event.type == MOUSEBUTTONDOWN:
            if SAVE_BUTTON.is_clicked():
                save_level()
                
            if last_mouse_click <= DOUBLE_CLICK_COOLDOWN:
                for i,c in enumerate(objects_list):
                    objects_list[i].selected = False
                for i,c in enumerate(objects_list):
                    if c.rect.collidepoint(mouse_world_pos):
                        objects_list[i].selected = True
                        break
        
        elif event.type == KEYDOWN:
            if (K_LCTRL in active_keys or 1073742051 in active_keys) and event.key == K_s:
                save_level()
            elif event.key == K_SPACE:
                self.next_state = "Drag;Default"

    def update(self):
        global objects_list
        for i,c in enumerate(objects_list):
            if c.selected:
                if K_g in active_keys and K_SPACE not in active_keys:
                    objects_list[i].rect.x += mouse_movement[0]
                    objects_list[i].rect.y += mouse_movement[1]
    
    def draw(self):
        mouse_img = cm
        for button in self.buttons: 
            button.draw()
            if button.hover():
                mouse_img = cm_point
                button.draw_text()
        mouse_pos_text = mouse_pos_font.render(f"{mouse_world_pos}",True,(0,0,0))
        if mouse_screen_pos[1] >= 72:
            screen.blit(mouse_pos_text,(mouse_screen_pos[0],mouse_screen_pos[1]-20))
        
        custom_mouse(mouse_img)


class Drag(GameState):
    def __init__(self,temp=False):
        super().__init__()
        self.queued_state = temp
        self.buttons = [
            SAVE_BUTTON
        ]
        
    def event_handle(self,event):
        if event.type == MOUSEBUTTONDOWN:
            if SAVE_BUTTON.is_clicked():
                save_level()
                
    def update(self):
        if mouse_down and mouse_screen_pos[1] >= 72:
            camera.x -= mouse_movement[0]
            camera.y -= mouse_movement[1]
        
        if K_SPACE not in active_keys:
            self.next_state = self.queued_state
    
    def draw(self):
        mouse_img = cm
        mouse_offset = (0,0)
        mouse_pos_text = mouse_pos_font.render(f"{mouse_world_pos}",True,(255,255,255),(0,0,0))
        for button in self.buttons: 
            button.draw()
            if button.hover():
                mouse_img = cm_point
                button.draw_text()
        
        if mouse_screen_pos[1] >= 72:
            screen.blit(mouse_pos_text,(mouse_screen_pos[0],mouse_screen_pos[1]-20))
            mouse_offset = (-12,3)
            if mouse_down:  
                mouse_img = cm_grip
            else:
                mouse_img = cm_grab

        custom_mouse(mouse_img,mouse_offset)
    def draw(self):
        mouse_img = cm
        offset = (0,0)
        for button in self.buttons: 
            button.draw()
            if button.hover():
                mouse_img = cm_point
                button.draw_text()
        mouse_pos_text = mouse_pos_font.render(f"{mouse_world_pos}",True,(255,255,255),(0,0,0))
        if mouse_screen_pos[1] >= 72:
            screen.blit(mouse_pos_text,(mouse_screen_pos[0],mouse_screen_pos[1]-20))
            offset = (-15,0)
            if mouse_down:
                mouse_img = cm_grip
            else:
                mouse_img = cm_grab
        
        custom_mouse(mouse_img,offset)
        

class NewRect(GameState):
    def __init__(self):
        super().__init__()


def custom_mouse(img,offset=(0,0)):
    screen.blit(img,(mouse_screen_pos[0]+offset[0],mouse_screen_pos[1]+offset[1]))

def switch_states():
    global current_state
    if current_state.next_state:
        current_state.exit()
        if current_state.next_state == "Default":
            current_state = Default()
        elif current_state.next_state == "Drag":
            current_state = Drag()
        elif current_state.next_state[:4] == "Drag":
            current_state = Drag(current_state.next_state.split(";")[1])
        elif current_state.next_state == "New Rect":
            current_state = NewRect()
        
        current_state.enter()


class Button:
    def __init__(self,x,y,w,h,image=bowling,text=None):
        self.rect = pygame.Rect(x,y,w,h)
        self.image = pygame.transform.scale(image,(w,h))
        self.text = button_hover_font.render(text,True,(0,0,0),(255,255,255))
    
    def is_clicked(self):
        return self.hover()
    
    def hover(self):
        if self.rect.collidepoint(mouse_screen_pos):
            return True
    
    def draw(self):
        screen.blit(self.image,(self.rect.x,self.rect.y))
    
    def draw_text(self):
        screen.blit(self.text,(mouse_screen_pos[0]+20,mouse_screen_pos[1]-20)) 
   
SAVE_BUTTON = Button(200,10,30,30,text="Save Level")     

current_state = Default()

def main():
    global mouse_down,snapping,active_keys,last_mouse_click,mouse_screen_pos,mouse_movement,mouse_world_pos
    
    load_area_from_file("Untitled Level")

    running = True
    while running:
        events = [event for event in pygame.event.get()]
        for event in events:
            current_state.event_handle(event)
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                active_keys.add(event.key)
                if event.key == K_LSHIFT:
                    if snapping:
                        snapping = False
                    else:
                        snapping = True
            elif event.type == KEYUP:
                active_keys.remove(event.key)
            elif event.type == MOUSEBUTTONDOWN:
                mouse_down = True
                last_mouse_click = 0
            elif event.type == MOUSEBUTTONUP:
                mouse_down = False
    
        
        last_mouse_click += 1
        mouse_screen_pos = pygame.mouse.get_pos()
        mouse_movement = pygame.mouse.get_rel()
        
#         if K_SPACE in active_keys:# and mouse_down:
#             camera.x -= mouse_movement[0]
#             camera.y -= mouse_movement[1]
            
        current_state.update()
        
        mouse_world_pos = (mouse_screen_pos[0]+camera.x,mouse_screen_pos[1]+camera.y)
                
        screen.fill((150,150,150))    
        for x in range(-grid,WIDTH+grid,grid):
            pygame.draw.line(screen,(75,75,75),(x-camera.x%grid,0),(x-camera.x%grid,HEIGHT),1)
        for y in range(-grid,HEIGHT+grid,grid):
            pygame.draw.line(screen,(75,75,75),(0,y-camera.y%grid),(WIDTH,y-camera.y%grid),1)
        
        for o in objects_list:
            o.draw()
        
#         if K_SPACE in active_keys:
#             mouse_pos_text = mouse_pos_font.render(f"{mouse_world_pos}",True,(255,255,255),(50,50,50))
#         else:
#             mouse_pos_text = mouse_pos_font.render(f"{mouse_world_pos}",True,(0,0,0))
#         screen.blit(mouse_pos_text,(mouse_screen_pos[0],mouse_screen_pos[1]-20))
        
        draw_gui()
        current_state.draw()
        
        switch_states()
        
        pygame.display.flip()
        clock.tick(30)
#     save_level()
    pygame.quit()
    
def load_area_from_file(file_name):
    global objects_list,item_list
    try:
        file = open(f"custom levels/{file_name}.txt")
    except FileNotFoundError:
        file = open(f"custom levels/default.txt")
    
    for line in file:
        id, data = line.split(":")
        if id == "c":
            c = [int(coord) for coord in data.split(",")]
            objects_list.append(CollisionObject(c[0],c[1],c[2],c[3]))
        elif id == "d":
            c = [int(coord) for coord in data.split(",")]
            objects_list.append(DamagingObject(c[0],c[1],c[2],c[3]))
            
def save_level(name="Untitled Level"):
    file = open(f"custom levels/{name}.txt","w")
    for o in objects_list:
        if o.__class__ == CollisionObject:
            file.write(f"c:{o.rect.x},{o.rect.y},{o.rect.width},{o.rect.height}\n")
        elif o.__class__ == DamagingObject:
            file.write(f"d:{o.rect.x},{o.rect.y},{o.rect.width},{o.rect.height}\n")
    file.close()

def draw_gui():
    pygame.draw.polygon(screen,(185,192,200),((0,0),(0,60),(3,66),(6,69),(12,72),(WIDTH-12,72),(WIDTH-6,69),(WIDTH-3,66),(WIDTH,60),(WIDTH,0)))
    file_name_text = file_name_font.render(current_file_name,True,(0,0,0))
    screen.blit(file_name_text,(10,5))


if __name__ == "__main__":
    main()

