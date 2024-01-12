import pygame, json
from pygame.locals import *

WIDTH = 1280
HEIGHT = 720
SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Title')
clock = pygame.time.Clock()

controls = {}

def load_preferences():
    global controls
    with open("preferences.json","r") as f:
        controls = json.loads(f.readline())

load_preferences()