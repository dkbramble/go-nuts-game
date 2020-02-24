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
    def __init__(self, z=0, x=0, y=0, motion_range=100, motion_type ="h", delta=400):
        super().__init__(z, x, y)
        # Where the spider is positioned
        self.x = x
        self.y = y
        self.next_x = x
        self.next_y = y

        # Set motion type and range for spider
        self.motion_range = motion_range
        self.motion_type = motion_type

        # Assigns directions to movement functions for simpler movement
        self.cardinal_movement = {
            Direction.NORTH: self.move_north,
            Direction.SOUTH: self.move_south,
            Direction.EAST: self.move_east,
            Direction.WEST: self.move_west
        }
        ''' 
        Movement types are as follows:
            h: Horizontal line
            v: Vertical Line
            L: L-shaped motion
            fL: Flipped L-Shape Motion
            s: Square
        '''
        movement_orders = {
            "h": [Direction.EAST, Direction.WEST],
            "v": [Direction.SOUTH, Direction.NORTH],
            "L": [Direction.SOUTH, Direction.EAST, Direction.WEST, Direction.NORTH],
            "fL": [Direction.EAST, Direction.SOUTH, Direction.NORTH, Direction.WEST],
            "s": [Direction.EAST, Direction.SOUTH, Direction.WEST, Direction.NORTH]
        }
        self.move_order = movement_orders[motion_type]

        # Current animation and movement direction
        self.direction = self.move_order[0]
        self.change_direction(self.direction)

        self.delta = delta
        # Range of motion spider will have
        self.motion_range = motion_range
        # Tracks state of direction. D - Down. U - Up

        self.delta = 400
        # Loads all images for animations
        self.image_num = 0
        self.images = self.load_images()

        self.image = self.images[self.direction][0]

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

    # Load spritesheet for animation 
    def load_images(self):
        sprites = Spritesheet("./enemies/LPC_Spiders/spider01.png", int(Settings.tile_size/2), 10)
        images = {
            Direction.NORTH: [],
            Direction.WEST: [],
            Direction.SOUTH: [],
            Direction.EAST: []
        }
        for i in range(0,10):
            images[Direction.NORTH].append(sprites.sprites[i+3].image)
            images[Direction.WEST].append(sprites.sprites[i+13].image)
            images[Direction.SOUTH].append(sprites.sprites[i+23].image)
            images[Direction.EAST].append(sprites.sprites[i+33].image)
        return images

    #Updates animation image to next in the series
    def update_image(self):
        self.image = self.images[self.direction][self.image_num]

        if self.image_num == 5:
            self.image_num = 0
        else:
            self.image_num += 1 

    # Get next direction for the initialized movement shape.
    def get_next_direction(self):
        return self.move_order[(self.move_order.index(self.direction)+1)%len(self.move_order)]

    def change_direction(self, direction):
        if direction == Direction.NORTH:
            self.next_y = self.next_y - self.motion_range
        elif direction == Direction.SOUTH:
            self.next_y = self.next_y + self.motion_range
        elif direction == Direction.EAST:
            self.next_x = self.next_x + self.motion_range
            self.h_direction = direction
        elif direction == Direction.WEST:
            self.next_x = self.next_x - self.motion_range
            self.h_direction = direction

    # Move based on curernt direction
    def move(self, time):
        self.collisions = []
        amount = self.delta * time
        self.update_image()
        next_dir = self.get_next_direction()
        if self.cardinal_movement[self.direction](amount, next_dir):
            self.change_direction(next_dir)

    #Movement methods for each cardinal direction

    def move_north(self, amount, next_dir):
        self.y = self.y - amount
        self.update(0)
        if len(self.collisions) != 0:
            self.y = self.y + 2*amount
            self.update(0)
            self.direction = next_dir
            return True
        if  self.y <= self.next_y:
            self.direction = next_dir
            return True
        return False

    def move_south(self, amount, next_dir):
        self.y = self.y + amount
        self.update(0)
        if len(self.collisions) != 0:
            self.y = self.y - amount
            self.update(0)
            self.direction = next_dir
            return True
        if self.y >= self.next_y:
            self.direction = next_dir
            return True
        return False

    def move_west(self, amount, next_dir):
        self.x = self.x - amount
        self.update(0)
        if len(self.collisions) != 0:
            self.x = self.x + 2*amount
            self.update(0)
            self.direction = next_dir
            return True
        if self.x <= self.next_x:
            self.direction = next_dir
            return True
        return False

    def move_east(self, amount, next_dir):
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