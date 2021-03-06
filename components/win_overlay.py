import league
import pygame
from components.sound_manager import SoundManager
from components.overlay import Overlay_Button

class Win_Overlay(league.DUGameObject):
    """This Window pops up when the player has gotten the acorn. It offers 
     them a chance to restart the level or quit the game.

    Fields:
    player - the controlled player to determine health
    reset + quit - the two buttons that are rendered alongside the popup
    engine - the game engine to manipulate rendering  
    """
    def __init__(self, player, reset, quit, engine):
        super().__init__(self)
        self._layer = 1001
        self.player = player
        self.font = pygame.font.Font('freesansbold.ttf',64)
        self.image = pygame.Surface([350, 150], pygame.SRCALPHA)
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

    #Checks for winning conditions conditions. If true, stop the entire game and render the popup
    def update(self, deltaTime):
        if self.player.got_acorn and self.active == False:
            self.player.sound = False
            s = SoundManager()
            if s.get_playing() == True:
                s.bgm_control()
                s.set_playing(True)
            s.play_sound('you_won.wav')
            self.e.events.clear()
            self.e.collisions.clear()
            self.e.registered_keys.clear()
            self.e.events[pygame.MOUSEBUTTONDOWN] = self.button_click
            self.e.events[pygame.QUIT] = self.e.stop
            self.active = True

        if self.active == True:
            self.image.fill((209, 45, 25))
            self.text = self.font.render("YOU WIN", True, (53,50,150))
            self.image.blit(self.text, (25, 50))
            self.reset.set_display(True)
            self.quit.set_display(True)

    #Passes button clicked event to child buttons
    def button_click(self, deltaTime):
        mouse = pygame.mouse.get_pos()
        self.reset.mouse_click(deltaTime, mouse)
        self.quit.mouse_click(deltaTime, mouse)