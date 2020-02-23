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

        s = Spider(10, 2810, 2527, 210, "v")
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

        b = Bee(10, 3482, 3134, 220, "v")
        b.blocks.add(t.impassable)
        b.world_size = world_size
        b.rect = b.image.get_rect()

        b2 = Bee(10, 2486, 790, 200, "s")
        b2.blocks.add(t.impassable)
        b2.world_size = world_size
        b2.rect = b.image.get_rect()

        b3 = Bee(10, 5940, 1078, 170, "fL")
        b3.blocks.add(t.impassable)
        b3.world_size = world_size
        b3.rect = b.image.get_rect()

        b4 = Bee(10, 6185, 1509, 250, "s")
        b4.blocks.add(t.impassable)
        b4.world_size = world_size
        b4.rect = b.image.get_rect()

        l = Leafbug(10, 2213, 3103, 500, "h")
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

        l4 = Leafbug(10, 6559, 1215, 250, "h")
        l4.blocks.add(t.impassable)
        l4.world_size = world_size
        l4.rect = l.image.get_rect()

        ac = Acorn(10, 7000, 3300)
        ac.blocks.add(t.impassable)
        ac.world_size = world_size
        ac.rect = ac.image.get_rect()
        
       
        resetL = Overlay_Button(200,250, False, "            Reset", (209, 45, 25), (0,0,0), (255,255,255), e)
        quL = Overlay_Button(375,250, False, "         Quit", (209, 45, 25), (0,0,0), (255,255,255), e)
        resetW = Overlay_Button(200,250, False, "            Reset", (53,50,150), (209, 45, 25), (255,255,255), e)
        quW = Overlay_Button(375,250, False, "         Quit", (53,50,150), (209, 45, 25), (255,255,255), e)

        lose = Lose_Overlay(p, resetL, quL, e)
        w = Win_Overlay(p, resetW, quW, e)
        c = league.LessDumbCamera(800, 400, p, e.drawables, world_size)

        e.objects.append(p)

        e.objects.append(b)
        e.objects.append(b2)
        e.objects.append(b3)
        e.objects.append(b4)

        e.objects.append(l)
        e.objects.append(l2)
        e.objects.append(l3)
        e.objects.append(l4)

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
        e.drawables.add(b3)
        e.drawables.add(b4)

        e.drawables.add(l)
        e.drawables.add(l2)
        e.drawables.add(l3)
        e.drawables.add(l4)

        e.drawables.add(s)
        e.drawables.add(s2)
        e.drawables.add(s3)
        e.drawables.add(s4)

        e.drawables.add(ac)

        e.drawables.add(o)
        e.drawables.add(bu)

        e.objects.append(resetL)
        e.objects.append(quL)
        e.objects.append(resetW)
        e.objects.append(quW)
        e.objects.append(lose)
        e.objects.append(c)
        e.objects.append(o)
        e.objects.append(w)
        e.objects.append(bu)

        e.drawables.add(quL)
        e.drawables.add(resetL)
        e.drawables.add(quW)
        e.drawables.add(resetW)
        e.drawables.add(lose)
        e.drawables.add(w)

        e.collisions[(p, p.ouch)] = [s,s2,s3,s4,b,b2,b3,b4,l,l2,l3,l4]
        e.collisions[(p, p.win)] = [ac]
        #Bees
        pygame.time.set_timer(pygame.USEREVENT + 1, 100 // league.Settings.gameTimeFactor)
        pygame.time.set_timer(pygame.USEREVENT + 2, 100 // league.Settings.gameTimeFactor)
        pygame.time.set_timer(pygame.USEREVENT + 3, 100 // league.Settings.gameTimeFactor)
        pygame.time.set_timer(pygame.USEREVENT + 4, 100 // league.Settings.gameTimeFactor)
        #Leafbugs
        pygame.time.set_timer(pygame.USEREVENT + 10, 100 // league.Settings.gameTimeFactor)
        pygame.time.set_timer(pygame.USEREVENT + 11, 100 // league.Settings.gameTimeFactor)
        pygame.time.set_timer(pygame.USEREVENT + 12, 100 // league.Settings.gameTimeFactor)
        pygame.time.set_timer(pygame.USEREVENT + 13, 100 // league.Settings.gameTimeFactor)
        #Spiders
        pygame.time.set_timer(pygame.USEREVENT + 20, 100 // league.Settings.gameTimeFactor)
        pygame.time.set_timer(pygame.USEREVENT + 21, 100 // league.Settings.gameTimeFactor)
        pygame.time.set_timer(pygame.USEREVENT + 22, 100 // league.Settings.gameTimeFactor)
        pygame.time.set_timer(pygame.USEREVENT + 23, 100 // league.Settings.gameTimeFactor)
        #Nutthaniel
        pygame.time.set_timer(pygame.USEREVENT + 30, 20 // league.Settings.gameTimeFactor)
        pygame.time.set_timer(pygame.USEREVENT + 31, 20 // league.Settings.gameTimeFactor)

        e.add_key(pygame.K_a, p.move_left)
        e.add_key(pygame.K_d, p.move_right)

        e.add_key(pygame.K_q, p.print_place)

        e.add_key(pygame.K_b, p.climb_on)
        e.add_key(pygame.K_SPACE, p.jump)

        e.events[pygame.MOUSEBUTTONDOWN] = bu.mouse_click

        e.events[pygame.USEREVENT + 1] = b.move
        e.events[pygame.USEREVENT + 2] = b2.move
        e.events[pygame.USEREVENT + 3] = b3.move
        e.events[pygame.USEREVENT + 4] = b4.move
        e.events[pygame.USEREVENT + 10] = l.move
        e.events[pygame.USEREVENT + 11] = l2.move
        e.events[pygame.USEREVENT + 12] = l3.move
        e.events[pygame.USEREVENT + 13] = l4.move
        e.events[pygame.USEREVENT + 20] = s.move
        e.events[pygame.USEREVENT + 21] = s2.move
        e.events[pygame.USEREVENT + 22] = s3.move
        e.events[pygame.USEREVENT + 23] = s4.move
        e.events[pygame.USEREVENT + 30] = p.move_down #gravity
        e.events[pygame.USEREVENT + 31] = p.update_jump

        e.events[pygame.QUIT] = e.stop
        e.run()
        if e.reset:
            gamin = True

if __name__=='__main__':
    main()
