from league import *
from components import *
from league import *
import pygame
import sys
sys.path.append('..')
import league

#Acorn sprite from https://ya-webdesign.com/imgdownload.html

class Acorn(Character):
    """This is a sample class for a player object.  A player
    is a character, is a drawable, and an updateable object.
    This class should handle everything a player does, such as
    moving, throwing/shooting, collisions, etc.  It was hastily
    written as a demo but should direction.
    """
    def __init__(self, z=0, x=0, y=0):
        super().__init__(z, x, y)
        # Where the player is positioned
        self.x = x
        self.y = y
        self.wait = 2
        self.origin_x = x
        self.origin_y = y

        self.delta = 512
        # The image to use.  This will change frequently
        # in an animated Player class.
        self.image_num = 0
        self.images = []
        temp = 0
        right = []
        for filename in sorted(os.listdir("./enemies/acorn/")):
            tmp = pygame.image.load('./enemies/acorn/' + filename).convert_alpha()
            print(filename)
            tmp = pygame.transform.scale(tmp, (32, 64))
            right.append(tmp)
        self.images = right
        # self.images = pygame.image.load('../enemies/bee/bee-0.png').convert_alpha()
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        # How big the world is, so we can check for boundries
        self.world_size = (Settings.width, Settings.height)
        # What sprites am I not allowd to cross?
        self.blocks = pygame.sprite.Group()
        # Which collision detection function?
        self.collide_function = pygame.sprite.collide_circle
        self.collisions = []

        self.collider = Drawable()
        self.collider.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.collider.rect = self.collider.image.get_rect()

    def update_image(self):
        self.image = self.images[self.image_num]
        if self.wait != 0:
            self.wait = self.wait - 1
        else:
            self.wait = 2
            if self.image_num == 7:
        	    self.image_num = 0
            else:
        	    self.image_num += 1
    
    def update(self, time):
        self.update_image()
        self.rect.x = self.x
        self.rect.y = self.y
        self.collisions = []
        for sprite in self.blocks:
            self.collider.rect.x= sprite.x
            self.collider.rect.y = sprite.y
            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)