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
from components.lose_overlay import Lose_Overlay
from components.overlay import Overlay_Button


def main():
    gamin = True
    while(gamin):
        gamin = False
        e = league.Engine("Go Nutts!")
        e.init_pygame()

        ##sprites = league.Spritesheet('../assets/base_chip_pipo.png', league.Settings.tile_size, 8)
        backgroundMaterial = league.Spritesheet('../assets/woodlandMaterials.png', league.Settings.tile_size, 5)
        directionalInfo = league.Spritesheet('../assets/directions.png', league.Settings.tile_size, 3)
        t = league.Tilemap('../assets/woodland.lvl', backgroundMaterial, layer = 1)
        ##d = league.Tilemap('../assets/directions.lvl', directionalInfo, layer = 2)
        b = league.Tilemap('../assets/background.lvl', backgroundMaterial, layer = 0)
        world_size = (t.wide*league.Settings.tile_size, t.high *league.Settings.tile_size)
        e.drawables.add(b.passable.sprites()) 
        e.drawables.add(t.passable.sprites())
        ##e.drawables.add(d.passable.sprites())
        m = SoundManager()
        m.bgm_start('Song_For_Someone.wav')
        p = Player(2, 420, 180)
        o = Overlay(p)
        bu = MusicButton()
        p.blocks.add(t.impassable)
        p.world_size = world_size
        p.rect = p.image.get_rect()

        s = Spider(10, 250, 50, 70)
        s.blocks.add(t.impassable)
        s.world_size = world_size
        s.rect = s.image.get_rect()

        b = Bee(10, 200, 100, 120)
        b.blocks.add(t.impassable)
        b.world_size = world_size
        b.rect = b.image.get_rect()

        ac = Acorn(10, 7000, 3390)
        ac.blocks.add(t.impassable)
        ac.world_size = world_size
        ac.rect = ac.image.get_rect()
        w = Win_Overlay(p)
        reset = Overlay_Button(200,250, False, "            Reset", (209, 45, 25), (0,0,0), (255,255,255), e)
        qu = Overlay_Button(375,250, False, "         Quit", (209, 45, 25), (0,0,0), (255,255,255), e)
        lose = Lose_Overlay(p, reset, qu, e)

        l = Leafbug(10, 50, 100, 70)
        l.blocks.add(t.impassable)
        l.world_size = world_size
        l.rect = l.image.get_rect()


        e.objects.append(p)
        e.objects.append(s)
        e.objects.append(b)
        e.objects.append(l)
        e.objects.append(reset)
        e.objects.append(qu)
        e.objects.append(ac)

        e.drawables.add(p)
        e.drawables.add(s)
        e.drawables.add(b)
        e.drawables.add(l)
        e.drawables.add(qu)
        e.drawables.add(reset)
        e.drawables.add(ac)
        e.drawables.add(o)
        e.drawables.add(w)
        e.drawables.add(lose)
        e.drawables.add(bu)

        c = league.LessDumbCamera(800, 400, p, e.drawables, world_size)
        #c = league.DumbCamera(800, 600, p, e.drawables, world_size)
        
        e.objects.append(c)
        e.objects.append(o)
        e.objects.append(w)
        e.objects.append(lose)
        e.objects.append(bu)

        e.collisions[(p, p.ouch)] = [b,s,l]
        e.collisions[(p, p.win)] = [ac]
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // league.Settings.gameTimeFactor)
        pygame.time.set_timer(pygame.USEREVENT + 2, 125 // league.Settings.gameTimeFactor)
        pygame.time.set_timer(pygame.USEREVENT + 3, 100 // league.Settings.gameTimeFactor)
        pygame.time.set_timer(pygame.USEREVENT + 4, 100 // league.Settings.gameTimeFactor)

        e.add_key(pygame.K_a, p.move_left)
        e.add_key(pygame.K_d, p.move_right)
        e.add_key(pygame.K_w, p.move_up)
        e.add_key(pygame.K_s, p.move_down)
        e.add_key(pygame.K_b, p.climb_on)
        e.add_key(pygame.K_SPACE, p.climb_off)
        e.events[pygame.MOUSEBUTTONDOWN + 1] = bu.mouse_click
        e.events[pygame.USEREVENT + 2] = s.move
        e.events[pygame.USEREVENT + 3] = b.move
        e.events[pygame.USEREVENT + 4] = l.move
        e.events[pygame.QUIT] = e.stop
        e.run()
        if e.reset:
            gamin = True

if __name__=='__main__':
    main()
