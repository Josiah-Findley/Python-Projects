# Import the pygame module
import pygame
import time
# Import random for random numbers
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Define the Player object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()


    # Move the sprite based on keypresses
    def update(self, pressed_keys, previous_time):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)




        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT



# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Define the Bullet object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        self.surf =  pygame.transform.scale(pygame.image.load("laser.png").convert(), (25,7))
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = player.rect.copy()
        self.speed = 15


    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

# Define the cloud object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


# Setup for sounds, defaults are good
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create our 'player'
player = Player()

# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# Load all our sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")

# Set the base volume for all sounds
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)

screen.fill((0, 0, 50))
font = pygame.font.Font(None, 36)
text = font.render("Get to the other side!!!", True, (255, 255, 255))
text_rect = text.get_rect()
text_x = screen.get_width() / 2 - text_rect.width / 2
text_y = screen.get_height() / 2 - text_rect.height / 2
screen.blit(text, [text_x, text_y])
pygame.display.flip()
pygame.time.delay(3000)

# Create custom events for adding a new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 100)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)


# Variable to keep our main loop running
running = True
seconds = time.time()
previous_time = 0
# Our main loop
while running:
    seconds2 = time.time()

    if (seconds2-seconds<=15 and seconds2-seconds>=14):
        pygame.time.set_timer(ADDENEMY, 80)
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False

            if event.key == K_SPACE:

                current_time = pygame.time.get_ticks()
                # We're ready to fire when 500 ms have passed.
                if ((current_time - previous_time) > 250):
                    previous_time = current_time
                    new_bullet = Bullet()
                    bullets.add(new_bullet)
                    all_sprites.add(new_bullet)


        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

        # Should we add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)


        # Should we add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud, and add it to our sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)




    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys, previous_time)

    # Update the position of our enemies and clouds
    enemies.update()
    clouds.update()
    bullets.update()

    # Fill the screen with sky blue
    screen.fill((0, 0, 50))

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    #bullet hits
    hit = pygame.sprite.groupcollide(bullets, enemies, True, True)
    if hit:
        collision_sound.play()

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        #pygame.time.delay(6000)
        # If so, remove the player
        player.kill()

        # Stop any moving sounds and play the collision sound
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()
        screen.fill((0, 0, 50))
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text, [text_x, text_y])

        # Stop the loop
        running = False
        pygame.display.flip()
        pygame.time.delay(3000)

    #Did one win?
    if player.rect.right == SCREEN_WIDTH:
        player.kill()
        move_up_sound.stop()
        move_down_sound.stop()
        screen.fill((0, 0, 50))
        font = pygame.font.Font(None, 36)
        text = font.render("You Won!", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text, [text_x, text_y])

        # Stop the loop
        running = False
        pygame.display.flip()
        pygame.time.delay(3000)
    # Flip everything to the display
    pygame.display.flip()

    # Ensure we maintain a 30 frames per second rate
    clock.tick(30)

# At this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()