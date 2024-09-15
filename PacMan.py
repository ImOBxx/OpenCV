import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 600, 400
FPS = 60
PACMAN_SIZE = 20
SPEED = 5
ENEMY_SPEED = 3
DOT_RADIUS = 5

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man with Enemies")

# Define the Pac-Man class
class PacMan:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, PACMAN_SIZE, PACMAN_SIZE)
        self.direction = pygame.Vector2(0, 0)

    def move(self):
        self.rect.x += self.direction.x * SPEED
        self.rect.y += self.direction.y * SPEED

        # Keep Pac-Man within the screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, self.rect.center, PACMAN_SIZE // 2)

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction = pygame.Vector2(-1, 0)
        elif keys[pygame.K_RIGHT]:
            self.direction = pygame.Vector2(1, 0)
        elif keys[pygame.K_UP]:
            self.direction = pygame.Vector2(0, -1)
        elif keys[pygame.K_DOWN]:
            self.direction = pygame.Vector2(0, 1)
        else:
            self.direction = pygame.Vector2(0, 0)

# Define the Dot class
class Dot:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            pygame.draw.circle(screen, WHITE, (int(self.pos.x), int(self.pos.y)), DOT_RADIUS)

# Define the Enemy class
class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PACMAN_SIZE, PACMAN_SIZE)
        self.direction = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))

    def move(self):
        self.rect.x += self.direction.x * ENEMY_SPEED
        self.rect.y += self.direction.y * ENEMY_SPEED

        # Bounce off the screen edges
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction.x *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.direction.y *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, RED, self.rect.center, PACMAN_SIZE // 2)

# Create game objects
pacman = PacMan()
dots = [Dot(100, 100), Dot(200, 200), Dot(300, 300), Dot(400, 100), Dot(500, 300)]
enemies = [Enemy(50, 50), Enemy(550, 350)]

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle Pac-Man movement
    pacman.handle_keys()
    pacman.move()

    # Move enemies
    for enemy in enemies:
        enemy.move()

    # Check for dot collection
    for dot in dots:
        if pacman.rect.collidepoint(dot.pos.x, dot.pos.y):
            dot.collected = True

    # Check for collisions with enemies
    for enemy in enemies:
        if pacman.rect.colliderect(enemy.rect):
            pygame.quit()
            sys.exit("Game Over! Pac-Man was caught by an enemy.")

    # Drawing
    screen.fill(BLACK)
    pacman.draw(screen)
    for dot in dots:
        dot.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)
