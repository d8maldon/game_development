import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
PLAYER_SIZE = 40
PLAYER_COLOR = (255, 0, 0)  # Red color
BG_COLOR = (0, 0, 255)  # Blue color
PLATFORM_COLOR = (0, 255, 0)  # Green color
SPIKE_COLOR = (255, 255, 255)  # White color
FPS = 60

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario Clone")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_y = 0
        self.jump = False

    def update(self):
        # Gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        self.rect.y += self.vel_y

        # Check for collisions with platforms
        self.rect.y += self.vel_y
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.jump = False

        # Check for collisions with spikes
        if pygame.sprite.spritecollideany(self, spikes):
            self.kill()
            global running
            running = False

    def move(self, dx):
        self.rect.x += dx

    def jump_up(self):
        if not self.jump:
            self.vel_y = -20
            self.jump = True

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

# Spike class
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(SPIKE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

# Create player
player = Player(100, SCREEN_HEIGHT - PLAYER_SIZE - 100)

# Create platforms and spikes groups
platforms = pygame.sprite.Group()
spikes = pygame.sprite.Group()

# Initial platforms
platforms.add(Platform(0, SCREEN_HEIGHT - TILE_SIZE, SCREEN_WIDTH, TILE_SIZE))
platforms.add(Platform(200, SCREEN_HEIGHT - 2 * TILE_SIZE, TILE_SIZE * 3, TILE_SIZE))
platforms.add(Platform(500, SCREEN_HEIGHT - 4 * TILE_SIZE, TILE_SIZE * 2, TILE_SIZE))

# Group all sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(*platforms)

# Game loop
running = True
clock = pygame.time.Clock()
score = 0
start_ticks = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump_up()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-5)
    if keys[pygame.K_RIGHT]:
        player.move(5)

    # Update player and platforms
    player.update()
    platforms.update()
    spikes.update()

    # Generate new platforms and spikes
    if random.randint(1, 100) < 5:
        platforms.add(Platform(SCREEN_WIDTH, SCREEN_HEIGHT - TILE_SIZE * random.randint(1, 4), TILE_SIZE * random.randint(1, 3), TILE_SIZE))
        all_sprites.add(platforms)

    if random.randint(1, 100) < 2:
        spikes.add(Spike(SCREEN_WIDTH, SCREEN_HEIGHT - TILE_SIZE - PLAYER_SIZE, PLAYER_SIZE))
        all_sprites.add(spikes)

    # Update score
    score = 1.1 * ((pygame.time.get_ticks() - start_ticks) / 1000)

    # Redraw screen
    screen.fill(BG_COLOR)
    all_sprites.draw(screen)

    # Display score 
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {int(score)}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS) 

pygame.quit()
