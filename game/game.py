#!/usr/bin/env python3

import pygame
import sys
sys.path.append('..')
import league
from components import *
from player import Player
from enemies.spider import Spider
from enemies.bee import Bee
from enemies.leafbug import Leafbug
from enemies.acorn import Acorn
from components.overlay import Overlay
from components.win_overlay import Win_Overlay

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
    p = Player(2, 400, 200)
    o = Overlay(p)
    bu = MusicButton()
    p.blocks.add(t.impassable)
    p.world_size = world_size
    p.rect = p.image.get_rect()

    s = Spider(10, 250, 50, 70, "h")
    s.blocks.add(t.impassable)
    s.world_size = world_size
    s.rect = s.image.get_rect()

    s2 = Spider(10, 1590, 630, 200, "v")
    s2.blocks.add(t.impassable)
    s2.world_size = world_size
    s2.rect = s.image.get_rect()

    s3 = Spider(10, 3090, 700, 230, "v")
    s3.blocks.add(t.impassable)
    s3.world_size = world_size
    s3.rect = s.image.get_rect()

    s4 = Spider(10, 3530, 957, 200, "fL")
    s4.blocks.add(t.impassable)
    s4.world_size = world_size
    s4.rect = s.image.get_rect()

    b = Bee(10, 200, 100, 20, "h")
    b.blocks.add(t.impassable)
    b.world_size = world_size
    b.rect = b.image.get_rect()

    b2 = Bee(10, 2486, 790, 200, "s")
    b2.blocks.add(t.impassable)
    b2.world_size = world_size
    b2.rect = b.image.get_rect()

    l = Leafbug(10, 50, 100, 70, "v")
    l.blocks.add(t.impassable)
    l.world_size = world_size
    l.rect = l.image.get_rect()

    l2 = Leafbug(10, 1230, 167, 400, "h")
    l2.blocks.add(t.impassable)
    l2.world_size = world_size
    l2.rect = l.image.get_rect()

    l3 = Leafbug(10, 4259, 30, 150, "s")
    l3.blocks.add(t.impassable)
    l3.world_size = world_size
    l3.rect = l.image.get_rect()

    ac = Acorn(10, 500, 100)
    ac.blocks.add(t.impassable)
    ac.world_size = world_size
    ac.rect = ac.image.get_rect()
    w = Win_Overlay(p)

    e.objects.append(p)

    e.objects.append(b)
    e.objects.append(b2)

    e.objects.append(l)
    e.objects.append(l2)
    e.objects.append(l3)

    e.objects.append(s)
    e.objects.append(s2)
    e.objects.append(s3)
    e.objects.append(s4)

    e.objects.append(ac)

    #Adding Drawables
    e.drawables.add(p)
    e.drawables.add(s)

    e.drawables.add(b)
    e.drawables.add(b2)

    e.drawables.add(l)
    e.drawables.add(l2)
    e.drawables.add(l3)

    e.drawables.add(s)
    e.drawables.add(s2)
    e.drawables.add(s3)
    e.drawables.add(s4)

    e.drawables.add(ac)

    e.drawables.add(o)
    e.drawables.add(w)
    e.drawables.add(bu)

    c = league.LessDumbCamera(800, 600, p, e.drawables, world_size)
    #c = league.DumbCamera(800, 600, p, e.drawables, world_size)
    
    e.objects.append(c)
    e.objects.append(o)
    e.objects.append(w)
    e.objects.append(bu)

    e.collisions[(p, p.ouch)] = [s,s2,s3,s4,b,b2,l,l2,l3]
    e.collisions[(p, p.win)] = [ac]
    pygame.time.set_timer(pygame.USEREVENT + 1, 100 // league.Settings.gameTimeFactor)
    pygame.time.set_timer(pygame.USEREVENT + 2, 125 // league.Settings.gameTimeFactor)
    pygame.time.set_timer(pygame.USEREVENT + 3, 100 // league.Settings.gameTimeFactor)
    pygame.time.set_timer(pygame.USEREVENT + 4, 100 // league.Settings.gameTimeFactor)
    pygame.time.set_timer(pygame.USEREVENT + 5, 125 // league.Settings.gameTimeFactor)
    pygame.time.set_timer(pygame.USEREVENT + 6, 100 // league.Settings.gameTimeFactor)
    pygame.time.set_timer(pygame.USEREVENT + 7, 100 // league.Settings.gameTimeFactor)
    pygame.time.set_timer(pygame.USEREVENT + 8, 100 // league.Settings.gameTimeFactor)
    pygame.time.set_timer(pygame.USEREVENT + 9, 100 // league.Settings.gameTimeFactor)

    e.key_events[pygame.K_a] = p.move_left
    e.key_events[pygame.K_d] = p.move_right
    e.key_events[pygame.K_w] = p.move_up
    e.key_events[pygame.K_s] = p.move_down
    e.add_key(pygame.K_a, p.move_left)
    e.add_key(pygame.K_d, p.move_right)
    e.add_key(pygame.K_w, p.move_up)
    e.add_key(pygame.K_s, p.move_down)
    e.add_key(pygame.K_b, p.climb_on)
    e.add_key(pygame.K_q, p.print_place)
    e.add_key(pygame.K_SPACE, p.climb_off)
    e.events[pygame.USEREVENT + 1] = b.move
    e.events[pygame.USEREVENT + 2] = b2.move
    e.events[pygame.USEREVENT + 3] = s.move
    e.events[pygame.USEREVENT + 4] = s2.move
    e.events[pygame.USEREVENT + 5] = s3.move
    e.events[pygame.USEREVENT + 6] = s4.move
    e.events[pygame.USEREVENT + 7] = l.move
    e.events[pygame.USEREVENT + 8] = l2.move
    e.events[pygame.USEREVENT + 9] = l3.move
    e.events[pygame.QUIT] = e.stop
    e.run()

if __name__=='__main__':
    main()
