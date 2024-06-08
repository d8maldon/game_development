import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (165, 42, 42)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
RAINBOW = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Infinite Runner")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Player settings
player_size = 50
player_color = GREEN
player_speed = 5
player_jump_height = 10
player_gravity = 0.5
player_lives = 3
max_lives = 3

# Obstacle settings
obstacle_speed = 3
obstacles = []

# Blue ball settings
blue_ball_color = BLUE
blue_balls = []

# Orange star settings
orange_star_color = ORANGE
orange_stars = []
invincibility_duration = 5  # seconds
invincible = False
invincibility_end_time = 0

# Rainbow triangle settings
rainbow_triangle_size = 30
rainbow_triangles = []
can_shoot = False

# Bullet settings
bullets = []
bullet_speed = 10
bullet_duration = 5  # seconds
bullet_spawn_time = 0

# Confetti settings
confetti = []
confetti_duration = 2  # seconds
confetti_start_time = 0

# Player initialization
player = pygame.Rect(50, SCREEN_HEIGHT - player_size, player_size, player_size)
player_velocity_y = 0
player_on_ground = False
can_double_jump = False

# Load soundtrack
background_songs = ['background1.mp3', 'background2.mp3', 'background3.mp3', 'background4.mp3', 'background5.mp3']
pygame.mixer.music.load(random.choice(background_songs))
pygame.mixer.music.play()

# Font for score and lives
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)
input_font = pygame.font.SysFont(None, 48)

# Score settings
start_time = time.time()
score = 0

leaderboard_file = "leaderboard.txt"

try:
    with open(leaderboard_file, "r") as file:
        scores = [int(line.strip().split()[1]) for line in file if line.strip()]
        high_score = max(scores) if scores else 0
except FileNotFoundError:
    high_score = 0

def draw():
    screen.fill(WHITE)
    if invincible:
        pygame.draw.rect(screen, random.choice(RAINBOW), player)
    else:
        pygame.draw.rect(screen, player_color, player)
    for obstacle in obstacles:
        if isinstance(obstacle, pygame.Rect):
            pygame.draw.rect(screen, BROWN, obstacle)
        elif isinstance(obstacle, list):  # Octagon
            pygame.draw.polygon(screen, BROWN, obstacle)
    for ball in blue_balls:
        pygame.draw.circle(screen, blue_ball_color, (ball.x + ball.width // 2, ball.y + ball.height // 2), ball.width // 2)
    for star in orange_stars:
        pygame.draw.polygon(screen, orange_star_color, [(star.x, star.y + star.height), 
                                                        (star.x + star.width / 2, star.y), 
                                                        (star.x + star.width, star.y + star.height)])
    for triangle in rainbow_triangles:
        pygame.draw.polygon(screen, random.choice(RAINBOW), [(triangle.x, triangle.y + triangle.height), 
                                                            (triangle.x + triangle.width / 2, triangle.y), 
                                                            (triangle.x + triangle.width, triangle.y + triangle.height)])
    for bullet in bullets:
        pygame.draw.rect(screen, BLACK, bullet)

    # Draw score and lives
    score_text = font.render(f"Score: {int(score)}", True, BLACK)
    lives_text = font.render(f"Lives: {player_lives}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    # Draw confetti
    for piece in confetti:
        pygame.draw.circle(screen, random.choice(RAINBOW), piece, 5)

    pygame.display.flip()

def move_player():
    global player_velocity_y, player_on_ground, can_double_jump, player_lives, invincible, can_shoot, player_speed

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < SCREEN_WIDTH:
        player.x += player_speed

    if player_on_ground:
        if keys[pygame.K_SPACE]:
            player_velocity_y = -player_jump_height
            player_on_ground = False
            can_double_jump = True
    elif can_double_jump and keys[pygame.K_SPACE]:
        player_velocity_y = -player_jump_height
        can_double_jump = False

    player_velocity_y += player_gravity
    player.y += player_velocity_y

    if player.bottom > SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT
        player_velocity_y = 0
        player_on_ground = True
        can_double_jump = False

    for obstacle in obstacles:
        if isinstance(obstacle, pygame.Rect) and player.colliderect(obstacle):
            if not invincible:
                obstacles.remove(obstacle)
                player_lives -= 1
                if player_lives == 0:
                    game_over()
        elif isinstance(obstacle, list):  # Octagon
            if player.colliderect(pygame.Rect(obstacle[0][0], obstacle[0][1], 100, 100)):
                if not invincible:
                    obstacles.remove(obstacle)
                    player_lives -= 1
                    if player_lives == 0:
                        game_over()

    for ball in blue_balls:
        if player.colliderect(ball):
            blue_balls.remove(ball)
            if player_lives < max_lives:
                player_lives += 1

    for star in orange_stars:
        if player.colliderect(star):
            orange_stars.remove(star)
            global invincibility_end_time
            invincible = True
            invincibility_end_time = time.time() + invincibility_duration

    for triangle in rainbow_triangles:
        if player.colliderect(triangle):
            rainbow_triangles.remove(triangle)
            can_shoot = True

def spawn_obstacles_and_items():
    if len(obstacles) < 5:
        shape_type = random.choice(['rect', 'long_rect', 'octagon'])
        if shape_type == 'rect':
            obstacle_x = random.randint(0, SCREEN_WIDTH - 50)
            obstacle_y = random.randint(-300, -50)
            obstacle = pygame.Rect(obstacle_x, obstacle_y, 50, 50)
        elif shape_type == 'long_rect':
            obstacle_x = random.randint(0, SCREEN_WIDTH - 200)
            obstacle_y = random.randint(-300, -50)
            obstacle = pygame.Rect(obstacle_x, obstacle_y, 200, 20)
        elif shape_type == 'octagon':
            obstacle_x = random.randint(0, SCREEN_WIDTH - 100)
            obstacle_y = random.randint(-300, -50)
            obstacle = [
                (obstacle_x, obstacle_y + 20), (obstacle_x + 20, obstacle_y), (obstacle_x + 80, obstacle_y),
                (obstacle_x + 100, obstacle_y + 20), (obstacle_x + 100, obstacle_y + 80),
                (obstacle_x + 80, obstacle_y + 100), (obstacle_x + 20, obstacle_y + 100),
                (obstacle_x, obstacle_y + 80)
            ]
        obstacles.append(obstacle)

    if len(blue_balls) < 2:
        ball_x = random.randint(0, SCREEN_WIDTH - 30)
        ball_y = random.randint(-600, -100)
        blue_balls.append(pygame.Rect(ball_x, ball_y, 30, 30))

    if len(orange_stars) < 1:
        star_x = random.randint(0, SCREEN_WIDTH - 30)
        star_y = random.randint(-900, -100)
        orange_stars.append(pygame.Rect(star_x, star_y, 30, 30))

    if len(rainbow_triangles) < 1:
        triangle_x = random.randint(0, SCREEN_WIDTH - rainbow_triangle_size)
        triangle_y = random.randint(-1200, -100)
        rainbow_triangles.append(pygame.Rect(triangle_x, triangle_y, rainbow_triangle_size, rainbow_triangle_size))

def move_obstacles_and_items():
    global obstacle_speed, score

    for obstacle in obstacles:
        if isinstance(obstacle, pygame.Rect):
            obstacle.y += obstacle_speed
            obstacle.x += random.choice([-1, 1]) * obstacle_speed // 2
            if obstacle.y > SCREEN_HEIGHT:
                obstacles.remove(obstacle)
        elif isinstance(obstacle, list):  # Octagon
            for i in range(len(obstacle)):
                obstacle[i] = (obstacle[i][0] + random.choice([-1, 1]) * obstacle_speed // 2, obstacle[i][1] + obstacle_speed)
            if obstacle[0][1] > SCREEN_HEIGHT:
                obstacles.remove(obstacle)

    for ball in blue_balls:
        ball.y += obstacle_speed
        if ball.y > SCREEN_HEIGHT:
            blue_balls.remove(ball)

    for star in orange_stars:
        star.y += obstacle_speed
        if star.y > SCREEN_HEIGHT:
            orange_stars.remove(star)

    for triangle in rainbow_triangles:
        triangle.y += obstacle_speed
        if triangle.y > SCREEN_HEIGHT:
            rainbow_triangles.remove(triangle)

    # Increase game speed over time, now faster
    score = (time.time() - start_time) * 10
    obstacle_speed = 3 + (score // 10) * 1.5

def check_invincibility():
    global invincible, invincibility_end_time
    if invincible and time.time() > invincibility_end_time:
        invincible = False

def handle_bullets():
    global bullets, obstacles, bullet_spawn_time
    current_time = time.time()
    for bullet in bullets:
        bullet.y -= bullet_speed
        if bullet.y < 0 or current_time - bullet_spawn_time > bullet_duration:
            bullets.remove(bullet)
        for obstacle in obstacles:
            if isinstance(obstacle, pygame.Rect) and bullet.colliderect(obstacle):
                obstacles.remove(obstacle)
                if bullet in bullets:
                    bullets.remove(bullet)
            elif isinstance(obstacle, list):  # Octagon
                for rect in obstacle:
                    if bullet.colliderect(pygame.Rect(rect[0], rect[1], 10, 10)):
                        obstacles.remove(obstacle)
                        if bullet in bullets:
                            bullets.remove(bullet)
                        break

def shoot_bullet():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_f] and can_shoot:
        bullet = pygame.Rect(player.x + player.width // 2 - 5, player.y, 10, 20)
        bullets.append(bullet)
        global bullet_spawn_time
        bullet_spawn_time = time.time()

def game_over():
    global running, score, high_score, confetti_start_time
    username = enter_username()
    new_high_score = int(score) > high_score
    if new_high_score:
        high_score = int(score)
    save_score(username, int(score))
    if new_high_score:
        display_new_high_score()
    display_leaderboard_and_retry()
    confetti_start_time = time.time()

def enter_username():
    username = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

        screen.fill(WHITE)
        prompt_text = input_font.render("Enter your name:", True, BLACK)
        input_text = input_font.render(username, True, BLACK)
        screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(input_text, (SCREEN_WIDTH // 2 - input_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        clock.tick(FPS)
    return username

def save_score(username, score):
    with open(leaderboard_file, "a") as file:
        file.write(f"{username} {score}\n")

def display_new_high_score():
    for _ in range(100):  # Generate 100 pieces of confetti
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        confetti.append((x, y))

    screen.fill(WHITE)
    new_high_score_text = game_over_font.render("New High Score!", True, random.choice(RAINBOW))
    screen.blit(new_high_score_text, (SCREEN_WIDTH // 2 - new_high_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - new_high_score_text.get_height() // 2))
    pygame.display.flip()
    time.sleep(2)

def display_leaderboard_and_retry():
    with open(leaderboard_file, "r") as file:
        scores = [line.strip().split() for line in file]
    scores = [(name, int(scr)) for name, scr in scores if scr.isdigit()]
    scores.sort(key=lambda x: x[1], reverse=True)

    screen.fill(WHITE)
    title_text = game_over_font.render("Leaderboard", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

    for i, (name, score) in enumerate(scores[:10], start=1):
        entry_text = font.render(f"{i}. {name}: {score}", True, BLACK)
        screen.blit(entry_text, (SCREEN_WIDTH // 2 - entry_text.get_width() // 2, 100 + i * 40))

    retry_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)
    pygame.draw.rect(screen, BLACK, retry_button)
    retry_text = font.render("Retry", True, WHITE)
    screen.blit(retry_text, (retry_button.x + retry_button.width // 2 - retry_text.get_width() // 2, retry_button.y + retry_button.height // 2 - retry_text.get_height() // 2))

    pygame.display.flip()
    wait_for_retry(retry_button)

def wait_for_retry(button):
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    reset_game()
                    waiting = False

def reset_game():
    global player, player_velocity_y, player_on_ground, can_double_jump, player_lives, invincible, can_shoot, obstacles, blue_balls, orange_stars, rainbow_triangles, bullets, start_time, score, player_speed, confetti
    player = pygame.Rect(50, SCREEN_HEIGHT - player_size, player_size, player_size)
    player_velocity_y = 0
    player_on_ground = False
    can_double_jump = False
    player_lives = 3
    invincible = False
    can_shoot = False
    obstacles = []
    blue_balls = []
    orange_stars = []
    rainbow_triangles = []
    bullets = []
    start_time = time.time()
    score = 0
    player_speed = 5
    confetti = []
    pygame.mixer.music.load(random.choice(background_songs))
    pygame.mixer.music.play()

# Main game loop
running = True
pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT + 1:
            pygame.mixer.music.load(random.choice(background_songs))
            pygame.mixer.music.play()

    move_player()
    shoot_bullet()
    handle_bullets()
    spawn_obstacles_and_items()
    move_obstacles_and_items()
    check_invincibility()
    draw()

    player_speed *= 1.001  # Increase player speed by a small factor each frame
    clock.tick(FPS)

pygame.quit()
sys.exit()
