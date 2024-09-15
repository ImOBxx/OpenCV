import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH = 700
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Game variables
gravity = 0.25
bird_movement = 0
pipe_speed = 3
bird_y = HEIGHT // 2
bird_x = 50
score = 0
game_active = True

# Bird image
bird_image = pygame.Surface((30, 30))
bird_image.fill(GREEN)

# Pipes
pipe_width = 60
pipe_gap = 150
pipes = []

# Create initial pipes
for i in range(2):
    pipe_height = random.randint(150, 450)
    pipes.append(pygame.Rect(WIDTH + i * 300, 0, pipe_width, pipe_height))
    pipes.append(pygame.Rect(WIDTH + i * 300, pipe_height + pipe_gap, pipe_width, HEIGHT - pipe_height - pipe_gap))

# Font for score
font = pygame.font.Font(None, 36)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -6
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipes = []
                bird_y = HEIGHT // 2
                bird_movement = 0
                score = 0
                for i in range(2):
                    pipe_height = random.randint(150, 450)
                    pipes.append(pygame.Rect(WIDTH + i * 300, 0, pipe_width, pipe_height))
                    pipes.append(pygame.Rect(WIDTH + i * 300, pipe_height + pipe_gap, pipe_width, HEIGHT - pipe_height - pipe_gap))

    if game_active:
        # Bird movement
        bird_movement += gravity
        bird_y += bird_movement
        bird_rect = pygame.Rect(bird_x, bird_y, 30, 30)

        # Draw bird
        screen.blit(bird_image, bird_rect)

        # Pipe movement and collision detection
        for pipe in pipes:
            pipe.x -= pipe_speed
            if bird_rect.colliderect(pipe):
                game_active = False

        # Remove off-screen pipes and create new ones
        if pipes[0].x < -pipe_width:
            pipes.pop(0)
            pipes.pop(0)
            pipe_height = random.randint(150, 450)
            pipes.append(pygame.Rect(WIDTH, 0, pipe_width, pipe_height))
            pipes.append(pygame.Rect(WIDTH, pipe_height + pipe_gap, pipe_width, HEIGHT - pipe_height - pipe_gap))
            score += 1

        # Draw pipes
        for pipe in pipes:
            pygame.draw.rect(screen, BLACK, pipe)

        # Display score
        score_surface = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_surface, (10, 10))

        # Check if the bird hits the ground or flies off the screen
        if bird_y > HEIGHT or bird_y < 0:
            game_active = False
    else:
        # Display game over message
        game_over_surface = font.render("Game Over! Press SPACE to Restart", True, BLACK)
        screen.blit(game_over_surface, (WIDTH // 2 - 150, HEIGHT // 2))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
