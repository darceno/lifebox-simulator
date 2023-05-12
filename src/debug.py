import pygame
from settings import *

pygame.init()
font = pygame.font.SysFont(None, debug_font_size)

def debug(info, y=HEIGHT_SIZE-debug_font_size, x=WIDTH_SIZE-debug_font_size):
    screen = pygame.display.get_surface()
    debug_surface = font.render(str(info), anti_aliasing, debug_font_color)
    debug_rect = debug_surface.get_rect(center = (x, y))
    pygame.draw.rect(screen, debug_background_color, debug_rect)
    screen.blit(debug_surface, debug_rect)