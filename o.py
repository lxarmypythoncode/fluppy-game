import pygame
import sys
import random

# Inisialisasi pygame
pygame.init()

# Dimensi layar
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Warna
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)

# FPS dan Clock
FPS = 60
clock = pygame.time.Clock()

# Variabel game
GRAVITY = 0.6
JUMP_STRENGTH = -7  # Lompatan lebih pendek
PIPE_GAP = 150
PIPE_SPEED = 3

# Load font
font = pygame.font.SysFont("Arial", 30)

# Load gambar
bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (40, 40))

# Fungsi untuk membuat pipa
def create_pipe():
    pipe_height = random.randint(100, 400)
    top_pipe = {"rect": pygame.Rect(SCREEN_WIDTH, 0, 50, pipe_height), "scored": False}
    bottom_pipe = {
        "rect": pygame.Rect(SCREEN_WIDTH, pipe_height + PIPE_GAP, 50, SCREEN_HEIGHT - pipe_height - PIPE_GAP),
        "scored": False,
    }
    return top_pipe, bottom_pipe

# Fungsi untuk menggambar teks
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    SCREEN.blit(text_surface, (x, y))

# Fungsi utama game
def game():
    bird = pygame.Rect(50, SCREEN_HEIGHT // 2, 40, 40)
    bird_speed = 0
    score = 0
    pipes = []
    SPAWN_PIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWN_PIPE, 1500)

    running = True
    while running:
        SCREEN.fill(BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_speed = JUMP_STRENGTH
            if event.type == SPAWN_PIPE:
                pipes.extend(create_pipe())

        # Gerakan burung
        bird_speed += GRAVITY
        bird.y += bird_speed

        # Pipa bergerak
        for pipe in pipes:
            pipe["rect"].x -= PIPE_SPEED

        # Menghapus pipa yang keluar layar
        pipes = [pipe for pipe in pipes if pipe["rect"].x + pipe["rect"].width > 0]

        # Deteksi tabrakan
        for pipe in pipes:
            if bird.colliderect(pipe["rect"]):
                running = False

        # Hitung skor
        for pipe in pipes:
            if pipe["rect"].x + pipe["rect"].width < bird.x and not pipe["scored"]:
                score += 1
                pipe["scored"] = True  # Tandai pipa telah dihitung

        # Gambar elemen game
        SCREEN.blit(bird_img, (bird.x, bird.y))
        for pipe in pipes:
            pygame.draw.rect(SCREEN, GREEN, pipe["rect"])

        # Tampilkan skor di layar
        draw_text(f"Score: {score}", font, BLACK, 10, 10)

        # Game over jika burung keluar layar
        if bird.top <= 0 or bird.bottom >= SCREEN_HEIGHT:
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    # Tampilkan skor akhir
    SCREEN.fill(WHITE)
    draw_text(f"Game Over! Your Score: {score}", font, BLACK, 50, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(2000)

# Jalankan game
if __name__ == "__main__":
    while True:
        game()
