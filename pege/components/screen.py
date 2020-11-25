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
    RED = (255, 0, 0)



    def __init__(self, mmu):

        self.mmu = mmu
        # set up pygame
        pygame.init()

        self.current_x = 0
        self.current_y = 0
        self.grid = True
        self.multiply_factor = 1
        self.width = 256 * self.multiply_factor
        self.height = 256 * self.multiply_factor
        # set up the window

        self.windowSurface = pygame.display.set_mode((self.width, self.height), 0, 32)
        pygame.display.set_caption('Ekkels gameboy emulator')
        # set up the colors


        basicFont = pygame.font.SysFont(None, 48)

        self.windowSurface.fill(Screen.LIGHT_GREEN)

        pygame.display.update()

    def _render_pixel(self, start_x, start_y, value):
        for y in range(self.multiply_factor):
            for x in range(self.multiply_factor):
                offset_x = start_x + x
                offset_y = start_y + y
                gfxdraw.pixel(self.windowSurface, offset_x, offset_y, value)

    def new_scanline(self):
        self.current_x = 0

    def render_tile_row(self, tr, y):
        self.current_y = y
        pointer = 0
        for tc in tr:
            self.current_x += 1
            self._render_pixel(self.current_x, self.current_y, tc)



    def update(self):
        pygame.display.update()

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
