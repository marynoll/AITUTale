import pygame
import os

def load_texture(filename):
    path = os.path.join("textures", filename)
    try:
        return pygame.image.load(path).convert_alpha()
    except:
        return pygame.Surface((100, 100))

def load_texture_no_alpha(filename):
    path = os.path.join("textures", filename)
    try:
        return pygame.image.load(path).convert()
    except:
        return pygame.Surface((100, 100))

def load_black_mask(filename, fallback_size):
    path = os.path.join("textures", filename)
    try:
        img = pygame.image.load(path).convert_alpha()
        white_bg = pygame.Surface(img.get_size())
        white_bg.fill((255, 255, 255))
        white_bg.blit(img, (0, 0))
        mask = pygame.mask.from_threshold(white_bg, (0, 0, 0, 255), (80, 80, 80, 255))
        return mask
    except:
        return pygame.Mask(fallback_size)

class SpriteSheet:
    def __init__(self, filename):
        path = os.path.join("textures", filename)
        try:
            self.sheet = pygame.image.load(path).convert_alpha()
            bg_color = self.sheet.get_at((0, 0))
            self.sheet.set_colorkey(bg_color)
        except:
            self.sheet = pygame.Surface((160, 10)) 

    def get_image(self, x, y, width, height, scale_w, scale_h):
        image = self.sheet.subsurface(pygame.Rect(x, y, width, height))
        return pygame.transform.scale(image, (scale_w, scale_h))