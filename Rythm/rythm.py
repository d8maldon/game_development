import pygame
import random
import numpy as np
import threading
import time
import json
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 0, 255)
GRAY = (50, 50, 50)

COLUMN_COLORS = [BLUE, RED, YELLOW, PINK]

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rhythm Tile Game")

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Clock
clock = pygame.time.Clock()

# Tile settings
tile_width = SCREEN_WIDTH // 4
tile_radius = 25
tile_speed = 5
tiles = []

# Score
score = 0
multiplier = 1
consecutive_hits = 0

# Leaderboard
leaderboard_file = 'leaderboard.json'

# Feedback messages
feedback_message = ""
feedback_time = 0

def load_leaderboard():
    try:
        with open(leaderboard_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_leaderboard(leaderboard):
    with open(leaderboard_file, 'w') as f:
        json.dump(leaderboard, f)

def update_leaderboard(username, score):
    leaderboard = load_leaderboard()
    leaderboard.append({'username': username, 'score': score})
    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)[:10]
    save_leaderboard(leaderboard)
    return leaderboard

def draw_text(text, font, color, surface, x, y, center=True):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def create_tile():
    column = random.choice([0, 1, 2, 3])
    x = column * tile_width + tile_width // 2
    y = 0
    color = COLUMN_COLORS[column]
    duration = random.choice([1, 2, 3])  # Duration for long press (in frames)
    tiles.append([x, y, color, duration])

def draw_tiles():
    for tile in tiles:
        pygame.draw.circle(screen, tile[2], (tile[0], tile[1]), tile_radius)
        if tile[3] > 1:  # Draw trailing edge for long press beats
            trail_height = tile[3] * tile_speed
            for i in range(trail_height):
                alpha = 255 - int(255 * (i / trail_height))
                color = (tile[2][0], tile[2][1], tile[2][2], alpha)
                surface = pygame.Surface((tile_radius * 2, 1), pygame.SRCALPHA)
                pygame.draw.line(surface, color, (0, 0), (tile_radius * 2, 0))
                screen.blit(surface, (tile[0] - tile_radius, tile[1] - i))

def update_tiles():
    global score, multiplier, consecutive_hits, feedback_message, feedback_time
    for tile in tiles:
        tile[1] += tile_speed
        if tile[1] > SCREEN_HEIGHT:
            tiles.remove(tile)
            consecutive_hits = 0
            multiplier = 1
            feedback_message = "Miss"
            feedback_time = time.time()
            if score > 0:
                score -= 1

def load_beats(file_path):
    return np.loadtxt(file_path)

def play_music(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def title_screen():
    while True:
        screen.fill(BLACK)
        draw_text("Rhythm Tile Game", large_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        draw_text("Press Enter to Start", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def song_selection_menu():
    songs = ["background1", "background2", "background3", "background4", "background5"]
    selected_song = 0

    while True:
        screen.fill(BLACK)
        draw_text("Select a Song", large_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200)

        for i, song in enumerate(songs):
            color = WHITE if i == selected_song else GRAY
            draw_text(song, font, color, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + i * 50)

        draw_text("Use Arrow Keys to Navigate, Enter to Select", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected_song > 0:
                    selected_song -= 1
                if event.key == pygame.K_DOWN and selected_song < len(songs) - 1:
                    selected_song += 1
                if event.key == pygame.K_RETURN:
                    return songs[selected_song]

def difficulty_selection_menu():
    difficulties = ["easy", "med", "hard"]
    selected_difficulty = 0

    while True:
        screen.fill(BLACK)
        draw_text("Select Difficulty", large_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)

        for i, difficulty in enumerate(difficulties):
            color = WHITE if i == selected_difficulty else GRAY
            draw_text(difficulty, font, color, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + i * 50)

        draw_text("Use Arrow Keys to Navigate, Enter to Select", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected_difficulty > 0:
                    selected_difficulty -= 1
                if event.key == pygame.K_DOWN and selected_difficulty < len(difficulties) - 1:
                    selected_difficulty += 1
                if event.key == pygame.K_RETURN:
                    return difficulties[selected_difficulty]

def get_username():
    username = ""
    active = True

    while active:
        screen.fill(BLACK)
        draw_text("Enter your username:", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        draw_text(username, font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

    return username

def display_leaderboard(leaderboard):
    while True:
        screen.fill(BLACK)
        draw_text("Leaderboard", large_font, WHITE, screen, SCREEN_WIDTH // 2, 50)

        for i, entry in enumerate(leaderboard):
            draw_text(f"{i + 1}. {entry['username']} - {entry['score']}", font, WHITE, screen, SCREEN_WIDTH // 2, 150 + i * 50)

        draw_text("Press R to Retry, Q to Quit", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    return False

def display_feedback():
    global feedback_message, feedback_time
    if feedback_message and time.time() - feedback_time < 1.0:
        draw_text(feedback_message, large_font, WHITE, screen, SCREEN_WIDTH // 2, 50)
    else:
        feedback_message = ""

# Main game loop
while True:
    title_screen()
    selected_song = song_selection_menu()
    selected_difficulty = difficulty_selection_menu()
    beatmap_file = f"{selected_song}_{selected_difficulty}.txt"
    
    if not os.path.exists(beatmap_file):
        beat_times = analyze_beats(f"{selected_song}.mp3", selected_difficulty)
        np.savetxt(beatmap_file, beat_times)
    else:
        beat_times = load_beats(beatmap_file)

    running = True
    start_time = time.time()
    music_thread = threading.Thread(target=play_music, args=(f"{selected_song}.mp3",))
    music_thread.start()
    beat_index = 0
    tiles = []
    score = 0
    multiplier = 1
    consecutive_hits = 0
    leaderboard = load_leaderboard()
    high_score = max(entry['score'] for entry in leaderboard) if leaderboard else 0

    while running:
        screen.fill(BLACK)

        # Draw column lines
        for i in range(1, 4):
            pygame.draw.line(screen, GRAY, (i * tile_width, 0), (i * tile_width, SCREEN_HEIGHT), 5)

        # Draw press indicator
        pygame.draw.line(screen, WHITE, (0, SCREEN_HEIGHT - 50), (SCREEN_WIDTH, SCREEN_HEIGHT - 50), 5)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                key_to_column = {
                    pygame.K_s: 0,
                    pygame.K_d: tile_width,
                    pygame.K_j: tile_width * 2,
                    pygame.K_k: tile_width * 3
                }
                if event.key in key_to_column:
                    column = key_to_column[event.key]
                    for tile in tiles:
                        if SCREEN_HEIGHT - 100 <= tile[1] + tile_radius <= SCREEN_HEIGHT:
                            if tile[0] == column + tile_width // 2:
                                tiles.remove(tile)
                                if abs(tile[1] + tile_radius - (SCREEN_HEIGHT - 50)) < tile_speed:
                                    feedback_message = "Perfect"
                                    score += 2 * multiplier
                                else:
                                    feedback_message = "Good"
                                    score += 1 * multiplier
                                feedback_time = time.time()
                                consecutive_hits += 1
                                multiplier = min(consecutive_hits // 5 + 1, 5)
                                break

        # Create new tile based on beat times
        current_time = time.time() - start_time
        if beat_index < len(beat_times) and current_time >= beat_times[beat_index]:
            create_tile()
            beat_index += 1

        # Update tiles
        update_tiles()

        # Draw tiles
        draw_tiles()

        # Draw score and feedback
        draw_text(f"Score: {score}", font, WHITE, screen, 10, 10, center=False)
        draw_text(f"High Score: {high_score}", font, WHITE, screen, SCREEN_WIDTH - 10, 10, center=False)
        display_feedback()

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

        # Check if song is finished
        if not pygame.mixer.music.get_busy() and beat_index >= len(beat_times) and not tiles:
            running = False

    # Get username input
    username = get_username()

    # Update leaderboard
    leaderboard = update_leaderboard(username, score)

    # Display leaderboard and retry option
    retry = display_leaderboard(leaderboard)
    if not retry:
        break

# Quit Pygame
pygame.quit()
