import pygame
import random

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), vsync=1)
clock = pygame.time.Clock()

#paddles
paddle_height = 100
user_paddle_rect = pygame.Rect(WINDOW_WIDTH-20, WINDOW_HEIGHT // 2, 50, paddle_height)

bot_paddle_rect = pygame.Rect(-30, WINDOW_HEIGHT // 2, 50, paddle_height)

#ball
ball_size = 30
ball_radius = ball_size //2
ball_rect = pygame.Rect(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, ball_size, ball_size)

SPEED = 5
BALL_SPEED = 5
BOT_SPEED = random.randint(3, 6)
ball_direction = -1
ball_vel_y = 0
play = True

font = pygame.font.SysFont(None, 72)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if play:
        keys = pygame.key.get_pressed()

        #user movement
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            user_paddle_rect.y -= SPEED  # In Pygame, Y decreases as you go UP
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            user_paddle_rect.y += SPEED

        screen.fill((30, 30, 30))


        #paddles
        pygame.draw.rect(screen, (255,255,255), user_paddle_rect)
        pygame.draw.rect(screen, (255,255,255), bot_paddle_rect)

        #ball
        pygame.draw.rect(screen, (255, 255, 255 ), ball_rect, border_radius=ball_radius)

        ball_rect.x += ball_direction * BALL_SPEED
        ball_rect.y += ball_vel_y

        #ball hitting paddle
        if ball_rect.colliderect(user_paddle_rect) or ball_rect.colliderect(bot_paddle_rect):
            ball_direction = ball_direction * -1
            ball_vel_y = random.randint(-6, 6)
            BALL_SPEED = BALL_SPEED + 1
            

        #ball hitting wall

        if ball_rect.top <= 0 or ball_rect.bottom >= WINDOW_HEIGHT:
            ball_vel_y = ball_vel_y * -1

        #bot movement
        if ball_direction == -1:
            difference = ball_rect.centery - bot_paddle_rect.centery

            if abs(difference) > 15:
                if difference > 0:
                    bot_paddle_rect.y = bot_paddle_rect.y + BOT_SPEED
                elif difference < 0:
                    bot_paddle_rect.y = bot_paddle_rect.y - BOT_SPEED

        #Winners!!!!!
        if ball_rect.x > WINDOW_WIDTH:
            play = False
            outcome = "You Lost"

        if ball_rect.x < 0:
            play = False
            outcome = "You Won"

    else:
        screen.fill((30,30,30))

        text_1 = font.render("Game Over", True, (255,255,255))
        text_rect_1 = text_1.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        text_2 = font.render(outcome, True, (255,255,255))
        text_rect_2 = text_2.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))      

        screen.blit(text_1, text_rect_1)
        screen.blit(text_2, text_rect_2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()