import league
import pygame

class Overlay(league.DUGameObject):
    def __init__(self, player):
        super().__init__(self)
        self._layer = 1000
        self.player = player
        self.font = pygame.font.Font('freesansbold.ttf',20)
        self.image = pygame.Surface([120, 24])
        self.image.fill((127, 127, 127))
        self.text = self.font.render("Health: " + str(self.player.health), True, (0,0,0))
        self.image.blit(self.text, (0, 0))
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.rect.x = 000
        self.rect.y = 0
        self.static = True

    def update(self, deltaTime):
        self.image.fill((127, 127, 127))
        self.text = self.font.render("Health: " + str(self.player.health), True, (0,0,0))
        self.image.blit(self.text, (0, 0))

class Overlay_Button(league.DUGameObject):
    def __init__(self, x, y, display, tx, font, color1, color2):
        super().__init__(self)
        self._layer = 1000
        self.font = pygame.font.Font('freesansbold.ttf',20)
        self.image = pygame.Surface([175, 24])
        self.rect = self.image.get_rect()
        self.x = 200
        self.y = 100
        self.rect.x = x
        self.rect.y = y
        self.static = True
        self.wait_time = -1
        self.display = display
        self.tx = tx
        self.font_color = font #(0,0,0)
        self.bg_color_1 = color1 #(0, 130, 0)
        self.bg_color_2 = color2 #(127, 127, 127)

    def update(self, deltaTime):
        if self.display:
            mouse = pygame.mouse.get_pos()
            if self.rect.x + 140 > mouse[0] > self.rect.x + 50 and 275 > mouse[1] > 245:
                self.image.fill(self.bg_color_2)
            else:
                self.image.fill(self.bg_color_1)
            self.text = self.font.render(self.tx, True, self.font_color)
            self.image.blit(self.text, (0, 0))
        
    def mouse_click(self):
        mouse = pygame.mouse.get_pos()
        if self.rect.x + 140 > mouse[0] > self.rect.x + 50 and 275 > mouse[1] > 245:
            if "Reset" in self.tx:
                print("YO")
            if "Quit" in self.tx:
                print("YOYO")
    def set_display(self, option):
        self.display = option
        