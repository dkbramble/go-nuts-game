from league import *
import pygame

playing = True

class SoundManager():
    """
    https://ozzed.net/music/friendship-adventure.shtml#tune13
    https://nerdparadise.com/programming/pygame/part3
    """

    def __init__(self):
        pygame.mixer.init()
        self.sound_path = '../assets/sounds/'

    def bgm_start(self, file):
        file_path = self.sound_path + file
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(-1)

    def bgm_control(self):
        global playing
        print(playing)
        if playing:
            pygame.mixer.music.pause()
            playing = False
        else:
            pygame.mixer.music.unpause()   
            playing = True
        return playing

    def play_sound(self, file):
        file_path = self.sound_path + file
        sound = pygame.mixer.Sound(file_path)
        sound.play()
    
    def get_playing(self):
        return playing

    def set_playing(self, play):
        global playing
        playing = play
