import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
BALL_RADIUS = 10
BALL_COLOR = (255, 0, 0)
PADDLE_COLOR = (0, 255, 0)
BUMPER_COLOR = (255, 255, 0)
TARGET_COLOR = (0, 0, 255)
BACKGROUND_COLOR = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
SCORE_COLOR = (255, 255, 255)
FONT_SIZE = 30

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Complicated Pinball Game')
clock = pygame.time.Clock()

# Font setup
font = pygame.font.SysFont(None, FONT_SIZE)

# Ball class
class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = 5

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def bounce(self, normal_angle):
        self.angle = 2 * normal_angle - self.angle

# Paddle class
class Paddle:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, direction):
        self.x += direction * 10
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > WIDTH:
            self.x = WIDTH - self.width

# Bumper class
class Bumper:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def collide(self, ball):
        dist = math.hypot(ball.x - self.x, ball.y - self.y)
        if dist < self.radius + ball.radius:
            angle = math.atan2(ball.y - self.y, ball.x - self.x)
            ball.bounce(angle)

# Target class
class Target:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hit = False

    def draw(self):
        if not self.hit:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def collide(self, ball):
        if not self.hit and self.x < ball.x < self.x + self.width and self.y < ball.y < self.y + self.height:
            self.hit = True
            return True
        return False

# Complicated board with obstacles
def draw_board():
    pygame.draw.line(screen, (255, 255, 255), (100, 100), (200, 50), 5)
    pygame.draw.line(screen, (255, 255, 255), (200, 50), (300, 150), 5)
    pygame.draw.line(screen, (255, 255, 255), (300, 150), (400, 100), 5)
    pygame.draw.line(screen, (255, 255, 255), (400, 100), (500, 200), 5)
    pygame.draw.line(screen, (255, 255, 255), (500, 200), (600, 100), 5)
    pygame.draw.line(screen, (255, 255, 255), (600, 100), (700, 200), 5)
    pygame.draw.line(screen, (255, 255, 255), (700, 200), (WIDTH, HEIGHT), 5)
    pygame.draw.line(screen, (255, 255, 255), (0, HEIGHT), (100, 100), 5)

def display_score(score):
    text = font.render(f'Score: {score}', True, SCORE_COLOR)
    screen.blit(text, (10, 10))

def main():
    run = True
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, BALL_COLOR)
    paddle = Paddle(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_COLOR)
    bumpers = [Bumper(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 200), 20, BUMPER_COLOR) for _ in range(5)]
    targets = [Target(random.randint(50, WIDTH - 100), random.randint(50, HEIGHT - 300), 50, 20, TARGET_COLOR) for _ in range(10)]
    score = 0

    while run:
        clock.tick(FPS)
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-1)
        if keys[pygame.K_RIGHT]:
            paddle.move(1)

        ball.move()
        ball.draw()
        paddle.draw()
        draw_board()
        display_score(score)

        # Ball collision with screen edges
        if ball.x - ball.radius <= 0 or ball.x + ball.radius >= WIDTH:
            ball.angle = math.pi - ball.angle
        if ball.y - ball.radius <= 0:
            ball.angle = -ball.angle
        if ball.y + ball.radius >= HEIGHT:
            run = False  # Ball fell off the bottom

        # Ball collision with paddle
        if (paddle.y < ball.y + ball.radius < paddle.y + paddle.height and
                paddle.x < ball.x < paddle.x + paddle.width):
            ball.angle = -ball.angle
            score += 10

        # Ball collision with bumpers
        for bumper in bumpers:
            bumper.draw()
            bumper.collide(ball)

        # Ball collision with targets
        for target in targets:
            if target.collide(ball):
                score += 50
            target.draw()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
