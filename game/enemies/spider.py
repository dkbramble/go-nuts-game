from league import *
from components import *
import pygame
import sys

class Spider(Character):
    """This is a sample class for a player object.  A player
    is a character, is a drawable, and an updateable object.
    This class should handle everything a player does, such as
    moving, throwing/shooting, collisions, etc.  It was hastily
    written as a demo but should direction.
    """
    def __init__(self, z=0, x=0, y=0, motion_range=100):
        super().__init__(z, x, y)
        # Where the player is positioned
        self.x = x
        self.y = y
        self.origin_x = x
        self.origin_y = y
        # Range of motion spider will have
        self.motion_range = motion_range
        # Tracks state of direction. D - Down. U - Up
        self.direction = Direction.SOUTH

        self.delta = 400
        # The image to use.  This will change frequently
        # in an animated Player class.
        self.sprites = Spritesheet("./enemies/LPC_Spiders/spider01.png", Settings.tile_size/2, 10)
        self.sp = self.sprites.sprites[2]
        self.image_num = 0
        self.image = self.sp.image
        self.images = []
        for i in range(0,6):
            self.images.append(self.sprites.sprites[i+4].image)
        self.image = self.images[0]
        # self.image = pygame.image.load('../assets/cartoon-spider-png-1.png').convert_alpha()
        # self.image = pygame.transform.scale(self.image, (64, 64))
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

    def load_images(self):
        sprites = league.Spritesheet("./enemies/LPC_Spiders/spider01.png", league.Settings.tile_size*2, 10)
        images = []
        for i in range(0,8):
            images.append(sprites.sprites[0].image)
        images

    def move(self, time):
        self.collisions = []
        amount = self.delta * time
        self.update_image()
        try:
            if self.y + amount > self.world_size[0] - Settings.tile_size:
                raise OffScreenTopException
            elif self.direction == Direction.SOUTH:
                self.y = self.y + amount
                self.update(0)
                while(len(self.collisions) != 0):
                    self.y = self.y - amount
                    self.update(0)
                if self.y - self.origin_y >= self.motion_range:
                    self.direction = Direction.NORTH
            elif self.direction == Direction.NORTH:
                self.y = self.y - amount
                self.update(0)
                while(len(self.collisions) != 0):
                    self.y = self.y + amount
                    self.update(0)
                if  self.y - self.origin_y <= 0:
                    self.direction = Direction.SOUTH
        except:
            pass

    def update_image(self):
        self.image = self.images[self.image_num]
        if self.direction == Direction.NORTH:
            if self.image_num == 5:
                self.image_num = 0
            else:
                self.image_num += 1 
        else:
            if self.image_num == 0:
                self.image_num = 5
            else:
                self.image_num -= 1 

    def update(self, time):
        self.rect.x = self.x
        self.rect.y = self.y
        self.collisions = []
        for sprite in self.blocks:
            self.collider.rect.x= sprite.x
            self.collider.rect.y = sprite.y
            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)