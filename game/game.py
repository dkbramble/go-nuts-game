#!/usr/bin/env python3

import pygame
import sys
sys.path.append('..')
import league
from components import *
from player import Player
from components.overlay import Overlay


"""This file is garbage. It was a hastily coded mockup
to demonstrate how to use the engine.  We will be creating
a Game class that organizes this code better (and is
reusable).
"""

# Function to call when colliding with zombie

def main():
    e = league.Engine("Go Nutts!")
    e.init_pygame()

    ##sprites = league.Spritesheet('../assets/base_chip_pipo.png', league.Settings.tile_size, 8)
    backgroundMaterial = league.Spritesheet('../assets/woodlandMaterials.png', league.Settings.tile_size, 5)
    t = league.Tilemap('../assets/woodland.lvl', backgroundMaterial, layer = 1)
    b = league.Tilemap('../assets/background.lvl', backgroundMaterial, layer = 0)
    world_size = (t.wide*league.Settings.tile_size, t.high *league.Settings.tile_size)
    e.drawables.add(b.passable.sprites()) 
    e.drawables.add(t.passable.sprites())
    m = SoundManager()
    m.bgm_start('Song_For_Someone.wav')
    p = Player(2, 400, 300)
    o = Overlay(p)
    bu = MusicButton()
    p.blocks.add(t.impassable)
    p.world_size = world_size
    p.rect = p.image.get_rect()
    q = Player(10, 100, 100)
    q.image = p.image
    e.objects.append(p)
    e.objects.append(q)
    e.drawables.add(p)
    e.drawables.add(q)
    e.drawables.add(o)
    e.drawables.add(bu)
    c = league.LessDumbCamera(800, 600, p, e.drawables, world_size)
    #c = league.DumbCamera(800, 600, p, e.drawables, world_size)
    
    e.objects.append(c)
    e.objects.append(o)
    e.objects.append(bu)

    e.collisions[p] = (q, p.ouch) 
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // league.Settings.gameTimeFactor)
    e.add_key(pygame.K_a, p.move_left)
    e.add_key(pygame.K_d, p.move_right)
    e.add_key(pygame.K_w, p.move_up)
    e.add_key(pygame.K_s, p.move_down)
    e.add_key(pygame.K_b, p.climb_on)
    e.add_key(pygame.K_SPACE, p.climb_off)
    e.events[pygame.USEREVENT + 1] = q.move_right
    e.events[pygame.QUIT] = e.stop
    e.run()

if __name__=='__main__':
    main()
