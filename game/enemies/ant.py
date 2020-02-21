from league import *
from components import *
import pygame
import sys
sys.path.append('..')
import league


class Ant(Character):

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
        self.direction = "D"

        self.delta = 512
        # The image to use.  This will change frequently
        # in an animated Player class.
        self.sprites = league.Spritesheet("./enemies/LPC_Spiders/spider01.png", league.Settings.tile_size/2, 10)
        self.sp = self.sprites.sprites[2]
        self.image = self.sp.image
        # self.image = pygame.image.load('../assets/ant.png').convert_alpha()
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

    def move(self, time):
        self.collisions = []
        amount = self.delta * time
        try:
            if self.y + amount > self.world_size[0] - Settings.tile_size:
                raise OffScreenTopException
            elif self.direction == "D":
                self.y = self.y + amount
                self.update(0)
                while(len(self.collisions) != 0):
                    self.y = self.y - amount
                    self.update(0)
                if self.y - self.origin_y >= self.motion_range:
                    self.direction = "U"
            elif self.direction == "U":
                self.y = self.y - amount
                self.update(0)
                while(len(self.collisions) != 0):
                    self.y = self.y + amount
                    self.update(0)
                if  self.y - self.origin_y <= 0:
                    self.direction = "D"
        except:
            pass

    def update(self, time):
        self.rect.x = self.x
        self.rect.y = self.y
        self.collisions = []
        for sprite in self.blocks:
            self.collider.rect.x= sprite.x
            self.collider.rect.y = sprite.y
            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)