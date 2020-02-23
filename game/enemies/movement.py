from league import *
from components import *
import pygame
import sys

class Movement():
    def __init__(self, enemy, motion_range=100, motion_type="h"):
        self.enemy = enemy

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
            "h": [Direction.EAST, Direction.WEST],
            "v": [Direction.SOUTH, Direction.NORTH],
            "L": [Direction.SOUTH, Direction.EAST, Direction.WEST, Direction.NORTH],
            "fL": [Direction.NORTH, Direction.WEST, Direction.EAST, Direction.SOUTH],
            "s": [Direction.EAST, Direction.SOUTH, Direction.WEST, Direction.NORTH]
        }
        self.move_order = movement_orders[motion_type]
        self.direction = self.move_order[0]
        self.change_direction(self.direction)

    def get_next_direction(self):
        return self.move_order[(self.move_order.index(self.direction)+1)%len(self.move_order)]

    def change_direction(self, direction):
        if direction == Direction.NORTH:
            self.enemy.next_y = self.enemy.next_y - self.motion_range
        elif direction == Direction.SOUTH:
            self.enemy.next_y = self.enemy.next_y + self.motion_range
        elif direction == Direction.EAST:
            self.enemy.next_x = self.enemy.next_x + self.motion_range
            self.enemy.h_direction = direction
        elif direction == Direction.WEST:
            self.enemy.next_x = self.enemy.next_x - self.motion_range
            self.enemy.h_direction = direction

    def move(self, amount):
        next_dir = self.get_next_direction()
        if self.cardinal_movement[self.direction](amount, next_dir):
            self.change_direction(next_dir)

    def move_north(self, amount, next_dir):
        self.enemy.y = self.enemy.y - amount
        self.enemy.update(0)
        if len(self.enemy.collisions) != 0:
            self.enemy.y = self.enemy.y + 2*amount
            self.enemy.update(0)
            self.direction = next_dir
            return True
        if  self.enemy.y <= self.enemy.next_y:
            self.direction = next_dir
            return True
        return False

    def move_south(self, amount, next_dir):
        self.enemy.y = self.enemy.y + amount
        self.enemy.update(0)
        if len(self.enemy.collisions) != 0:
            self.enemy.y = self.enemy.y - 2*amount
            self.enemy.update(0)
            self.direction = next_dir
            return True
        if self.enemy.y >= self.enemy.next_y:
            self.direction = next_dir
            return True
        return False

    def move_west(self, amount, next_dir):
        self.enemy.x = self.enemy.x - amount
        self.enemy.update(0)
        if len(self.enemy.collisions) != 0:
            self.enemy.x = self.enemy.x + 2*amount
            self.enemy.update(0)
            self.direction = next_dir
            return True
        if self.enemy.x <= self.enemy.next_x:
            self.direction = next_dir
            return True
        return False

    def move_east(self, amount, next_dir):
        self.enemy.x = self.enemy.x + amount
        self.enemy.update(0)
        if len(self.enemy.collisions) != 0:
            self.enemy.x = self.enemy.x - 2*amount
            self.enemy.update(0)
            self.direction = next_dir
            return True
        if  self.enemy.x >= self.enemy.next_x:
            self.direction = next_dir
            return True
        return False