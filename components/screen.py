import pygame, sys
from .mmu import MMU
from pygame import gfxdraw
from pygame.locals import *
# 160×144 pixels and shows 4 shades of grey (white, light grey,
# dark grey and black)
class Screen:

    
    def __init__(self, mmu):

        self.mmu = mmu
        # set up pygame
        pygame.init()

        # set up the window
        windowSurface = pygame.display.set_mode((160, 144), 0, 32)
        pygame.display.set_caption('Ekkels gameboy emulator')

        # set up the colors
        DARKEST_GREEN = (15, 56, 15)
        DARK_GREEN = (48, 98, 48)
        LIGHT_GREEN = (139, 172, 15)
        LIGHTEST_GREEN = (155, 188, 15)

        basicFont = pygame.font.SysFont(None, 48)

        windowSurface.fill(LIGHTEST_GREEN)
        # draw a green polygon onto the surface

        gfxdraw.pixel(windowSurface, 100, 100, DARKEST_GREEN)
        gfxdraw.pixel(windowSurface, 100, 101, DARKEST_GREEN)
        gfxdraw.pixel(windowSurface, 100, 102, DARKEST_GREEN)
        gfxdraw.pixel(windowSurface, 100, 103, DARKEST_GREEN)
        pixArray = pygame.PixelArray(windowSurface)
        pixArray[100][100] = DARK_GREEN
        del pixArray
        # draw the window onto the screen
        pygame.display.update()
 
