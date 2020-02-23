import league
import pygame
from components import *
from components.overlay import Overlay_Button

class Lose_Overlay(league.DUGameObject):
    def __init__(self, player, reset, quit, engine):
        super().__init__(self)
        self._layer = 1001
        self.player = player
        self.font = pygame.font.Font('freesansbold.ttf',64)
        self.image = pygame.Surface([350, 150])
        self.rect = self.image.get_rect()
        self.x = 200
        self.y = 100
        self.rect.x = 200
        self.rect.y = 100
        self.static = True
        self.active = False
        self.reset = False
        self.quit = False
        self.reset = reset
        self.quit = quit
        self.e = engine

    def update(self, deltaTime):
        if self.player.health < 1 and self.active == False:
            s = SoundManager()
            if s.get_playing() == True:
                s.bgm_control()
            s.play_sound('horn.wav')
            self.e.events.clear()
            self.e.collisions.clear()
            self.e.registered_keys.clear()
            self.e.events[pygame.MOUSEBUTTONDOWN] = self.button_click
            self.e.events[pygame.QUIT] = self.e.stop
            self.active = True

        if self.active == True:
            self.image.fill((0, 0, 0))
            self.text = self.font.render("YOU DIED", True, (209, 45, 25))
            self.image.blit(self.text, (25, 50))
            self.reset.set_display(True)
            self.quit.set_display(True)
    def button_click(self, deltaTime):
        mouse = pygame.mouse.get_pos()
        self.reset.mouse_click(deltaTime, mouse)
        self.quit.mouse_click(deltaTime, mouse)
         

