from league import *
from components import *
import pygame
import random

class Player(Character):
    """This is a sample class for a player object.  A player
    is a character, is a drawable, and an updateable object.
    This class should handle everything a player does, such as
    moving, throwing/shooting, collisions, etc.  It was hastily
    written as a demo but should direction.
    """
    def __init__(self, z=0, x=0, y=0):
        super().__init__(z, x, y)
        # This unit's health
        self.health = 100

        #states   
        self.climb = False
        self.jumping = False

        self.climb_direction = 0

        

        #movement constants
        self.jump_height = 100
        #defines how far along in the jump we are 0->1
        self.jump_delta = 0
        self.jump_start = self.y

        self.move_speed = 512
        self.gravity = 200
        
        
        # Initial x and y to reset the player position to.  
        # Debug purposes.
        self.xI = x
        self.yI = y

        # Last time I was hit
        self.last_hit = pygame.time.get_ticks()
        # A unit-less value.  Bigger is faster.
        self.delta = 512
        # Where the player is positioned
        self.x = x
        self.y = y
        self.state = State.IDLE
        # The image to use.  This will change frequently
        # in an animated Player class.
        self.image = pygame.image.load('../assets/zombie.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.images = self.load_images()
        self.image_num = 0
        self.image_delay = 0
        self.image = self.images[self.state][0]
        self.rect = self.image.get_rect()
        # How big the world is, so we can check for boundries
        self.world_size = (Settings.width, Settings.height)
        # What sprites am I not allowd to cross?
        self.blocks = pygame.sprite.Group()
        # Which collision detection function?
        self.collide_function = pygame.sprite.collide_circle
        self.collisions = []
        # For collision detection, we need to compare our sprite
        # with collideable sprites.  However, we have to remap
        # the collideable sprites coordinates since they change.
        # For performance reasons I created this sprite so we
        # don't have to create more memory each iteration of
        # collision detection.
        self.collider = Drawable()
        self.collider.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.collider.rect = self.collider.image.get_rect()
        # Overlay
        self.font = pygame.font.Font('freesansbold.ttf',32)
        self.overlay = self.font.render(str(self.health) + "        4 lives", True, (0,0,0))

    def load_images(self):
        images = {
            State.IDLE: []
        }
        sprites = Spritesheet("../assets/nutthaniel/sprMidiP.png", Settings.tile_size/4, 16)
        for i in range(1,5):
            tmp = sprites.sprites[i].image
            tmp = pygame.transform.scale(tmp, (64, 64))
            images[State.IDLE].append(tmp)
        return images

    def reset_position(self, time):
        self.x = self.xI
        self.y = self.yI



    def move_left(self, time):
        self.update_image(time)
        if not self.climb:
            amount = self.delta * time
            try:
                if self.x - amount < 0:
                    raise OffScreenLeftException
                else:
                    self.x = self.x - amount
                    self.update(0)
                    while(len(self.collisions) != 0):
                        self.x = self.x + amount
                        self.update(0)
            except:
                pass

    def move_right(self, time):
        self.update_image(time)
        if not self.climb:
            amount = self.delta * time
            try:
                if self.x + amount > self.world_size[0] - Settings.tile_size:
                    raise OffScreenRightException
                else:
                    self.x = self.x + amount
                    self.update(0)
                    while(len(self.collisions) != 0):
                        self.x = self.x - amount
                        self.update(0)
            except:
                pass

    def jump(self, time):  
        
        if not self.jumping:
            self.jump_delta = 0
            self.jump_start = self.y
        self.jumping = True
        self.climb_off(time)

    def lerpY(self, time, t):
        terminus = self.jump_start - self.jump_height
        return self.lerp(self.jump_start, terminus, t)

    def lerp(self, vI, vF, delta):
        return vI + delta * (vF - vI)

    def move_up(self, time):
        self.update_image(time)
        self.collisions = []
        amount = self.delta * time
        try:
            if self.y - amount < 0:
                raise OffScreenTopException
            else:
                if self.jumping :
                    self.y = self.lerpY(time, self.jump_delta)
                else:
                    self.y = self.y - amount
                self.update(0)
                if len(self.collisions) != 0:
                    self.y = self.y + amount
                    self.jumping = False
                    self.update(0)
                    self.collisions = []
            if self.climb:
                amount = self.delta * time * self.climb_direction
                self.x = self.x + amount * 3
                self.update(0)
                if len(self.collisions) == 0:
                    self.climb = False
                while(len(self.collisions) != 0):
                    self.x = self.x - amount
                    self.update(0)
        except: 
            pass

    def update_jump(self, time):
        if self.jumping:
            if (self.jump_delta >= 1) or (self.y < self.y-self.jump_height):
                self.jumping = False
                return
            self.jump_delta = self.jump_delta + .1
            print(self.jump_delta)
            self.move_up(time)
            self.update(0)

    def move_down(self, time):
        amount = self.gravity * time
        self.update_image(time)
        
        try:
            if self.y + amount > self.world_size[1] - Settings.tile_size:
                raise OffScreenBottomException
            else:
                self.y = self.y + amount
                self.update(0)
                if len(self.collisions) != 0:
                    self.y = self.y - amount
                    self.update(0)
                    self.jumping = False
                    self.collisions = []
            if self.climb:
                amount = self.delta * time * self.climb_direction
                self.x = self.x + amount
                self.update(0)
                if len(self.collisions) == 0:
                    self.x = self.x - amount
                    self.update(0)
                    self.climb = False
                while(len(self.collisions) != 0):
                    self.x = self.x - amount
                    self.update(0)
        except:
            pass
        
    #Hold right/left to run into an impassible object and press 'k' to climb. climbing will restrict horizontal movement until either the 
    #space bar is pressed or you reach the top or bottom of a the object.
    def climb_on(self, time, direction):
        amount = self.delta * time * direction
        self.climb_direction = direction
        try:
            if self.x + amount > self.world_size[0] - Settings.tile_size and direction > 0:
                raise OffScreenRightException
            elif self.x + amount < 0 and direction < 0:
                raise OffScreenLeftException
            else:
                self.x = self.x + amount
                self.update(0)
                if len(self.collisions) == 0:
                    self.x = self.x - amount
                    self.update(0)
                else:
                    self.climb = True
                    while(len(self.collisions) != 0):
                        self.x = self.x - amount
                        self.update(0)

        except:
            pass

    def climb_off(self, time):
        self.climb = False

    def update_image(self, time):
        self.image = self.images[self.state][self.image_num]
        now = pygame.time.get_ticks()
        if now - self.image_delay > 75:
            if self.image_num == 3:
                self.image_num = 0
            else:
                self.image_num +=1
            self.image_delay = now

    def update(self, time):
        self.rect.x = self.x
        self.rect.y = self.y
        self.collisions = []
        
        for sprite in self.blocks:
            self.collider.rect.x= sprite.x
            self.collider.rect.y = sprite.y
            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)

    def ouch(self):
        now = pygame.time.get_ticks()
        if now - self.last_hit > 1000:
            s = SoundManager()
            oucies_soundies = ['ow_1.wav','ow_2.wav','op.wav']
            s.play_sound(random.choice(oucies_soundies))
            self.health = self.health - 10
            self.last_hit = now
