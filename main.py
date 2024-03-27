import pygame
import random

pygame.init()

cloud_speed = 1
cactus_speed = 1

WIDTH = 600
HEIGHT = 200

screen = pygame.display.set_mode((WIDTH, HEIGHT))

dino_image = pygame.image.load("dino.png")
cactus_image = pygame.image.load("cactus.png")
cloud_image = pygame.image.load("cloud.png")
gameover_image = pygame.image.load("gameover.png")

cloud_x = WIDTH
cloud_y = random.randint(0, HEIGHT // 2)

dino_x = 20
dino_y = HEIGHT - 50
velocity = 0
dino_jumping = False

cactus_list = []

next_cactus_time = 1

def jump():
    global velocity, dino_jumping
    if not dino_jumping:
        velocity = -1
        dino_jumping = True

def create_cactus():
    cactus_x = WIDTH
    cactus_y = HEIGHT - 50
    cactus_list.append((cactus_x, cactus_y))

create_cactus()

button_height = gameover_image.get_height()
button_width = gameover_image.get_width()

button_x = WIDTH // 2 - button_width // 2
button_y = HEIGHT // 2 - button_height // 2

button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
button_show = False
paused = False

def press_button():
    global button_show, paused
    while len(cactus_list) !=0:
        cactus_list.pop(0)
        button_show = False
        paused = False
        create_cactus()

def draw_button():
    if button_show == True:
        global paused
        paused = True
        screen.blit(gameover_image, button_rect)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos) and button_show == True:
                press_button()

    if not paused :
        for i in range(len(cactus_list)):
            cactus_x, cactus_y = cactus_list[i]
            cactus_x -= cactus_speed
            if cactus_x + cactus_image.get_width() < 0:
                cactus_list.pop(i)
                break
            cactus_list[i] = (cactus_x, cactus_y)

    if cactus_list[-1][0] < WIDTH - 125:
        next_cactus_time -= 0.1
        if next_cactus_time <= 0:
            create_cactus()
            next_cactus_time = random.randint(1, 40)

    dino_y += velocity
    velocity += 0.01
    if dino_y >= HEIGHT - 50:
        dino_y = HEIGHT - 50
        velocity = 0
        dino_jumping = False

    for cactus_x, cactus_y in cactus_list:
        if dino_x + dino_image.get_width() > cactus_x and \
            dino_x < cactus_x + cactus_image.get_width() and \
            dino_y + dino_image.get_height() > cactus_y and \
            dino_y < cactus_y + cactus_image.get_height():
            button_show = True
            draw_button()

    screen.fill((255, 255, 255))
    screen.blit(dino_image, (dino_x, dino_y))
    screen.blit(cloud_image, (cloud_x, cloud_y))
    for cactus_x, cactus_y in cactus_list:
        screen.blit(cactus_image, (cactus_x, cactus_y))
    draw_button()

    pygame.display.update()

    pygame.time.Clock().tick(300)