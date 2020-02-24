import league
import pygame
from components import *

class MusicButton(league.DUGameObject):
    """This Button stays up the entirety of the game, and allows the 
    player to toggle the background music on and off.
    """
    def __init__(self):
        super().__init__(self)
        self.music = "On"
        self._layer = 1000
        self.font = pygame.font.Font('freesansbold.ttf',20)
        self.image = pygame.Surface([120, 24])
        self.image.fill((127, 127, 127))
        self.text = self.font.render("Music: " + self.music, True, (0,0,0))
        self.image.blit(self.text, (0, 0))
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.rect.x = 660
        self.rect.y = 0
        self.static = True
        self.wait_time = -1

    #When the mouse hovers over the button, render a different color
    def update(self, deltaTime):
        mouse = pygame.mouse.get_pos()
        if 800 > mouse[0] > 699 and 40 > mouse[1] > 0:
            self.image.fill((0, 130, 0))
        else:
            self.image.fill((127, 127, 127))
        self.text = self.font.render("Music: " + self.music, True, (0,0,0))
        self.image.blit(self.text, (0, 0))
        
    #This is called by a MOUSEDOWN event, toggles the music and updates the button text
    def mouse_click(self, deltaTime):
        mouse = pygame.mouse.get_pos()
        if 800 > mouse[0] > 699 and 40 > mouse[1] > 0:
            s = SoundManager()
            play = s.bgm_control() 
            if play == False:
                self.music = "Off"
            else:
                self.music = "On"
    
            
