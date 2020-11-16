import pygame, sys
from .mmu import MMU
from pygame import gfxdraw
from pygame.locals import *
# 160×144 pixels and shows 4 shades of grey (white, light grey,
# dark grey and black)
class Screen:

    DARKEST_GREEN = (15, 56, 15)
    DARK_GREEN = (48, 98, 48)
    LIGHT_GREEN = (139, 172, 15)
    LIGHTEST_GREEN = (155, 188, 15)
    

    def __init__(self, mmu):

        self.mmu = mmu
        # set up pygame
        pygame.init()

        self.multiply_factor = 12
        self.width = 160 * self.multiply_factor
        self.height = 144 * self.multiply_factor
        # set up the window

        self.windowSurface = pygame.display.set_mode((self.width, self.height), 0, 32)
        pygame.display.set_caption('Ekkels gameboy emulator')
        # set up the colors
       

        basicFont = pygame.font.SysFont(None, 48)

        self.windowSurface.fill(Screen.LIGHTEST_GREEN)
        # draw a green polygon onto the surface

        #gfxdraw.pixel(self.windowSurface, 100, 100, Screen.DARKEST_GREEN)
        #gfxdraw.pixel(self.windowSurface, 100, 101, Screen.DARKEST_GREEN)
        #3gfxdraw.pixel(self.windowSurface, 100, 102, Screen.DARKEST_GREEN)
        #gfxdraw.pixel(self.windowSurface, 100, 103, Screen.DARKEST_GREEN)
        #pixArray = pygame.PixelArray(self.windowSurface)
        #pixArray[100][100] = Screen.DARK_GREEN
        #del pixArray
        # draw the window onto the screen
        pygame.display.update()

    def _render_pixel(self, start_x, start_y, value):
        for y in range(self.multiply_factor):
            for x in range(self.multiply_factor):
                offset_x = start_x + x
                offset_y = start_y + y
                gfxdraw.pixel(self.windowSurface, offset_x, offset_y, value)

    def render_tile(self, tile):
        start_x = 100
        start_y = 100
        x = start_x
        y = start_y

        for tr in tile.rows:
            x = start_x
            y += self.multiply_factor
            for tc in tr.row:
                x += self.multiply_factor
                self._render_pixel(x, y, tc)
                #gfxdraw.pixel(self.windowSurface, x, y, tc)
            

        pygame.display.update()
        
 
