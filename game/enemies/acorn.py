from league import *
from components import *
import pygame
import sys
from enemies.movement import Movement

class Acorn(Character):

    def __init__(self, z=0, x=0, y=0):
        super().__init__(z, x, y)
        # Where the acorn is positioned
        self.x = x
        self.y = y
        self.next_x = x
        self.next_y = y
        # Tracks state of direction. D - Down. U - Up
        self.delta = 0
        # The image to use.  This will change frequently
        # in an animated Player class.
        self.image_num = 0
        self.images = {}
        temp = 0
        right = []
        for filename in sorted(os.listdir("./enemies/acorn/")):
            tmp = pygame.image.load('./enemies/acorn/' + filename).convert_alpha()
            tmp = pygame.transform.scale(tmp, (64, 128))
            right.append(tmp)
        self.images[Direction.WEST] = right
        # self.images = pygame.image.load('../enemies/bee/bee-0.png').convert_alpha()
        self.image = self.images[Direction.WEST][0]
        self.rect = self.image.get_rect()
        # How big the world is, so we can check for boundries
        self.world_size = (Settings.width, Settings.height)
        # What sprites am I not allowd to cross?
        self.blocks = pygame.sprite.Group()
        # Which collision detection function?
        self.collide_function = pygame.sprite.collide_circle
        self.collisions = []

        self.collider = Drawable()
        self.collider.image = pygame.Surface([int(Settings.tile_size/2), int(Settings.tile_size/2)])
        self.collider.rect = self.collider.image.get_rect()

    def update_image(self):
        self.image = self.images[Direction.WEST][self.image_num]

        if self.image_num == 7:
            self.image_num = 0
        else:
            self.image_num += 1 


    def move(self, time):
        self.collisions = []
        amount = self.delta * time
        self.update_image()
        next_dir = Direction.SOUTH
        self.x = self.x + amount
        self.update(0)
        if len(self.collisions) != 0:
            self.x = self.x - 2*amount
            self.update(0)
            self.direction = next_dir
            return True
        if  self.x >= self.next_x:
            self.direction = next_dir
            return True
        return False


    def update(self, time):
        self.rect.x = self.x
        self.rect.y = self.y
        self.collisions = []
        for sprite in self.blocks:
            self.collider.rect.x= sprite.x
            self.collider.rect.y = sprite.y
            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)