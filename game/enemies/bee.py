from league import *
from components import *
from league import *
import pygame
import sys
sys.path.append('..')
import league

class Bee(Character):
    """This is a sample class for a player object.  A player
    is a character, is a drawable, and an updateable object.
    This class should handle everything a player does, such as
    moving, throwing/shooting, collisions, etc.  It was hastily
    written as a demo but should direction.
    """
    def __init__(self, z=0, x=0, y=0, motion_range=100, motion_shape="I"):
        super().__init__(z, x, y)
        # Where the player is positioned
        self.x = x
        self.y = y
        self.origin_x = x
        self.origin_y = y
        # Range of motion spider will have
        self.motion_range = motion_range
        # Tracks state of direction. D - Down. U - Up
        self.h_direction = Direction.WEST
        self.v_direction = Direction.NORTH

        self.delta = 350
        # The image to use.  This will change frequently
        # in an animated Player class.
        self.image_num = 0
        self.images = {}
        temp = 0
        right = []
        left = []
        for filename in sorted(os.listdir("./enemies/bee/")):
            print(filename)
            tmp = pygame.image.load('./enemies/bee/' + filename).convert_alpha()
            tmp = pygame.transform.scale(tmp, (64, 64))
            right.append(tmp)
            left.append(pygame.transform.flip(tmp, True, False))
        self.images[Direction.EAST] = right
        self.images[Direction.WEST] = left
        # self.images = pygame.image.load('../enemies/bee/bee-0.png').convert_alpha()
        self.image = self.images[self.h_direction][0]
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
        self.image = self.images[self.h_direction][self.image_num]

        if self.image_num == 10:
        	self.image_num = 0
        else:
        	self.image_num += 1 

    def move(self, time):
        self.collisions = []
        amount = self.delta * time
        self.update_image()
        try:
            if self.y + amount > self.world_size[0] - Settings.tile_size:
                raise OffScreenTopException
            elif self.v_direction == Direction.SOUTH:
                self.move_south(amount)
            elif self.v_direction == Direction.NORTH:
                self.move_north(amount)

            if self.x + amount > self.world_size[0] - Settings.tile_size:
                raise OffScreenTopException
            elif self.h_direction == Direction.WEST:
                self.move_west(amount)
            elif self.h_direction == Direction.EAST:
                self.move_east(amount)
        except:
            pass

    def move_north(self, amount):
        self.y = self.y - amount
        self.update(0)
        while(len(self.collisions) != 0):
            self.y = self.y + amount
            self.update(0)
        if  self.y - self.origin_y <= 0:
            self.v_direction = Direction.SOUTH

    def move_south(self, amount):
        self.y = self.y + amount
        self.update(0)
        while(len(self.collisions) != 0):
            self.y = self.y - amount
            self.update(0)
        if self.y - self.origin_y >= self.motion_range:
            self.v_direction = Direction.NORTH

    def move_west(self, amount):
        self.x = self.x - amount
        self.update(0)
        while(len(self.collisions) != 0):
            self.x = self.x + amount
            self.update(0)
        if self.x - self.origin_x <= 0:
            self.h_direction = Direction.EAST

    def move_east(self, amount):
        self.x = self.x + amount
        self.update(0)
        while(len(self.collisions) != 0):
            self.x = self.x - amount
            self.update(0)
        if  self.x - self.origin_x >= self.motion_range:
            self.h_direction = Direction.WEST

    def update(self, time):
        self.rect.x = self.x
        self.rect.y = self.y
        self.collisions = []
        for sprite in self.blocks:
            self.collider.rect.x= sprite.x
            self.collider.rect.y = sprite.y
            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)