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
        
        self.h_direction = Direction.EAST

        self.state_switch_time = 0
        
        # Initial x and y to reset the player position to.  
        # Debug purposes.
        self.xI = x
        self.yI = y

        self.got_acorn = False
        # Last time I was hit
        self.last_hit = pygame.time.get_ticks()
        # A unit-less value.  Bigger is faster.
        self.delta = 400
        # Where the player is positioned
        self.x = x
        self.y = y
        self.state = State.IDLE
        # The image to use.  This will change frequently
        # in an animated Player class.
        self.images = self.load_images()
        self.image_num = 0
        self.image_delay = 0
        self.image = self.images[self.state][self.h_direction][0]
        self.animation_delays = {
            State.JUMP: 150,
            State.RUN: 75,
            State.IDLE: 75,
            State.CLIMB: 220
        }
        self.reverse_climb = False
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

    def load_images(self):
        images = {
            State.IDLE: {
                Direction.EAST: [],
                Direction.WEST: []
            },
            State.RUN: {
                Direction.EAST: [],
                Direction.WEST: []
            },
            State.JUMP: {
                Direction.EAST: [],
                Direction.WEST: []
            },
            State.CLIMB: {
                Direction.EAST: [],
                Direction.WEST: []
            }
        }
        sprites = Spritesheet("../assets/nutthaniel/sprMidiP.png", Settings.tile_size/4, 16)
        for i in range(1,5):
            tmp = sprites.sprites[i].image
            tmp = pygame.transform.scale(tmp, (64, 64))
            images[State.IDLE][Direction.EAST].append(tmp)
            images[State.IDLE][Direction.WEST].append(pygame.transform.flip(tmp, True, False))
        for i in range(0,11):
            tmp = sprites.sprites[i+33].image
            tmp = pygame.transform.scale(tmp, (64, 64))
            images[State.RUN][Direction.EAST].append(tmp)
            images[State.RUN][Direction.WEST].append(pygame.transform.flip(tmp, True, False))
        for i in range(0,5):
            tmp = sprites.sprites[i+9].image
            tmp = pygame.transform.scale(tmp, (64, 64))
            images[State.JUMP][Direction.EAST].append(tmp)
            images[State.JUMP][Direction.WEST].append(pygame.transform.flip(tmp, True, False))
        for i in range(0,4):
            tmp = sprites.sprites[i+72].image
            tmp = pygame.transform.scale(tmp, (64, 64))
            images[State.CLIMB][Direction.EAST].append(tmp)
            images[State.CLIMB][Direction.WEST].append(tmp)
        return images

    def reset_position(self, time):
        self.x = self.xI
        self.y = self.yI

    def change_state(self, next_state):
        if self.state != next_state and not self.jumping:
            if next_state == State.JUMP:
                self.state = next_state
                self.image_num = 0
            elif not self.climb:
                self.state = next_state
                self.image_num = 0
        self.state_switch_time = pygame.time.get_ticks()


    def move_left(self, time):
        self.update_image(time)
        self.change_state(State.RUN)
        self.h_direction = Direction.WEST
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
        self.change_state(State.RUN)
        self.h_direction = Direction.EAST
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

    def reset_idle(self):
        if self.state != State.IDLE and pygame.time.get_ticks() - self.state_switch_time > 100:
            self.change_state(State.IDLE)
        if pygame.time.get_ticks() - self.state_switch_time > 4000:
            s = SoundManager()
            idle_titles = ['feelin_peckish.wav','im_ready.wav','nut_my_day.wav']
            s.play_sound(random.choice(idle_titles))
            self.state_switch_time = pygame.time.get_ticks()

    def jump(self, time):  
        
        if not self.jumping:
            self.jump_delta = 0
            self.jump_start = self.y
        self.change_state(State.JUMP)
        self.jumping = True
        self.climb_off(time)

    def update_jump(self, time):
        if self.jumping:
            if (self.jump_delta >= 1) or (self.y < self.y-self.jump_height):
                self.falling = True
                return
            self.jump_delta = self.jump_delta + .1
            if not self.falling:
                self.move_up(time)
            self.update(0)

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
                if self.jumping and not self.falling :
                    self.y = self.lerpY(time, self.jump_delta)
                elif self.climb:
                    amount = self.delta * time * self.climb_direction
                    self.x = self.x + amount * 3
                self.update(0)
                if len(self.collisions) != 0:
                    self.y = self.y + amount
                    self.falling = True
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

    def move_down(self, time):
        amount = self.delta * time
        # if self.climb:
        #     amount = self.delta * time
        self.update_image(time)
        
        try:
            if self.y + amount > self.world_size[1] - Settings.tile_size:
                raise OffScreenBottomException
            else:
                if self.climb:
                    self.y = self.y + amount
                else:
                    self.y = self.y + amount/2
                self.update(0)
                if len(self.collisions) != 0:
                    self.y = self.y - amount
                    self.update(0)
                    self.jumping = False
                    self.falling = False
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

    def move_down_gravity(self, time):
        amount = self.gravity * time
        # if self.climb:
        #     amount = self.delta * time
        self.update_image(time)
        
        try:
            if self.y + amount > self.world_size[1] - Settings.tile_size:
                raise OffScreenBottomException
            elif not self.climb:
                self.y = self.y + amount
                self.update(0)
                if len(self.collisions) != 0:
                    self.y = self.y - amount
                    self.update(0)
                    self.jumping = False
                    self.falling = False
                    self.collisions = []
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
                self.falling = False
                self.jumping = False
                self.update(0)
                if len(self.collisions) == 0:
                    self.x = self.x - amount
                    self.update(0)
                else:
                    self.change_state(State.CLIMB)
                    self.climb = True
                    while(len(self.collisions) != 0):
                        self.x = self.x - amount
                        self.update(0)
        except:
            pass

    def climb_off(self, time):
        self.climb = False

    def update_image(self, time):
        self.image = self.images[self.state][self.h_direction][self.image_num]
        now = pygame.time.get_ticks()
        images_size = len(self.images[self.state][self.h_direction])
        if now - self.image_delay > self.animation_delays[self.state]:
            if self.state == State.JUMP and self.image_num == images_size-1:
                self.image_num -= 1
                self.image_delay = now
            elif self.state == State.CLIMB: 
                if now - self.image_delay > self.animation_delays[self.state]:
                    if self.image_num == images_size-1:
                        self.reverse_climb = True
                    elif self.image_num == 0:
                        self.reverse_climb = False
                    if self.reverse_climb:
                        self.image_num -= 1
                    else:
                        self.image_num += 1
            else: 
                if self.image_num == images_size-1:
                    self.image_num = 0
                else:
                    self.image_num +=1
            self.image_delay = now

    def print_place(self, time):
        print(str(self.x) + "   " + str(self.y))

    def update(self, time):
        self.rect.x = self.x
        self.rect.y = self.y
        self.collisions = []
        
        for sprite in self.blocks:
            self.collider.rect.x= sprite.x
            self.collider.rect.y = sprite.y
            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)
        self.reset_idle()

    def ouch(self):
        now = pygame.time.get_ticks()
        if now - self.last_hit > 1000:
            s = SoundManager()
            oucies_soundies = ['ow_1.wav','ow_2.wav','op.wav']
            s.play_sound(random.choice(oucies_soundies))
            self.health = self.health - 10
            if self.health < 0:
                self.health = 0
            self.last_hit = now

    def win(self):
        now = pygame.time.get_ticks()
        if now - self.last_hit > 1000:
            self.got_acorn = True
