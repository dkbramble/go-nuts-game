import league
import pygame

class Win_Overlay(league.DUGameObject):
    def __init__(self, player):
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

    def update(self, deltaTime):
        if self.player.got_acorn:
            self.image.fill((209, 45, 25))
            self.text = self.font.render("YOU WIN!", True, (53,50,150))
            self.image.blit(self.text, (25, 50))
