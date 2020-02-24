from league import *
from components import *
import pygame
import sys
from enemies.movement import Movement

class Bee(Character):

    def __init__(self, z=0, x=0, y=0, motion_range=100, motion_type="h", delta = 400):
        super().__init__(z, x, y)
        # Where the bee is positioned
        self.x = x
        self.y = y
        self.next_x = x
        self.next_y = y
        # Range of motion the bee will have
        self.motion_range = motion_range
        self.motion_type = motion_type

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
            "h": [Direction.WEST, Direction.EAST],
            "v": [Direction.NORTH, Direction.SOUTH],
            "L": [Direction.SOUTH, Direction.EAST, Direction.WEST, Direction.NORTH],
            "fL": [Direction.EAST, Direction.SOUTH, Direction.NORTH, Direction.WEST],
            "s": [Direction.EAST, Direction.SOUTH, Direction.WEST, Direction.NORTH]
        }
        self.move_order = movement_orders[motion_type]

        # Direction initialization
        self.h_direction = Direction.WEST
        self.direction = self.move_order[0]
        self.change_direction(self.direction)

        self.delta = delta
        # Load in images to animate bee
        self.image_num = 0
        self.images = {}
        right = []
        left = []
        for filename in sorted(os.listdir("./enemies/bee/")):
            tmp = pygame.image.load('./enemies/bee/' + filename).convert_alpha()
            tmp = pygame.transform.scale(tmp, (64, 64))
            right.append(tmp)
            left.append(pygame.transform.flip(tmp, True, False))
        self.images[Direction.EAST] = right
        self.images[Direction.WEST] = left
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
        self.collider.image = pygame.Surface([int(Settings.tile_size/2), int(Settings.tile_size/2)])
        self.collider.rect = self.collider.image.get_rect()
        self.movement = Movement(self,motion_range,motion_type)

    #Updates animation image to next in the series
    def update_image(self):
        self.image = self.images[self.h_direction][self.image_num]

        if self.image_num == 10:
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