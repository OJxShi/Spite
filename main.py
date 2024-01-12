import pygame, random, math
from pygame.locals import *
import config, animated_sprites_script, game_state, playing
from config import *
from game_state import *
from playing import *
    
def main():
    pygame.init()
    pygame.font.init()

    current_state = MainMenu()
    current_state.enter()

    running = True
    while running:
        for event in pygame.event.get():
            current_state.event_handle(event)
            if event.type == QUIT:
                running = False
    
        if current_state.next_state != None:
            current_state.exit()
            if current_state.next_state == "Quit":
                running = False
            elif current_state.next_state == "Playing":
                current_state = Playing()
            elif current_state.next_state == "Pause":
                current_state = Pause()
            elif current_state.next_state == "Main Menu":
                current_state = MainMenu()
            elif current_state.next_state == "Save Screen":
                current_state = SaveScreen()
            current_state.enter()
    
        current_state.update()
    
        screen.fill((255,255,255))
        current_state.draw()
    
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main()