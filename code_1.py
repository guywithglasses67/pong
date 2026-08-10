import pygame
import random
import math

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), vsync=1)
clock = pygame.time.Clock()

#ball
ball_size = 30
ball_radius = ball_size //2
ball_rect = pygame.Rect(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, ball_size, ball_size)


SPEED = 6
BALL_SPEED = 5
#BOT_SPEED = random.randint(3, 6)
ball_direction = -1
ball_vel_y = 0
play = True
keep_playing = True
user_score = 0
bot_score = 0
kp = 1/15
g = 255
b = 255

font = pygame.font.SysFont(None, 180)
small_font = pygame.font.SysFont(None, 30)

#paddles
paddle_height = 100
user_paddle_rect = pygame.Rect(WINDOW_WIDTH-20, WINDOW_HEIGHT // 2, 50, paddle_height)
bot_paddle_rect = pygame.Rect(-30, WINDOW_HEIGHT // 2, 50, paddle_height)


def reset_game():
    global user_paddle_rect, bot_paddle_rect, ball_rect, g, b, baba_paddle_height
    global BOT_SPEED, BALL_SPEED, SPEED, ball_direction, play, ball_vel_y

    #Reset paddles
    user_paddle_rect.y = WINDOW_HEIGHT // 2
    bot_paddle_rect.y = WINDOW_HEIGHT // 2

    #Reset ball
    ball_rect.x = WINDOW_WIDTH // 2
    ball_rect.y = WINDOW_HEIGHT // 2
    

    #Reset speeds
    #BOT_SPEED = random.randint(3,6)
    BALL_SPEED = 5
    SPEED = 6
    ball_direction = -1
    ball_vel_y = 0


    play = True

    user_paddle_rect.height = 100
    bot_paddle_rect.height = 100

    g = 255
    b = 255


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(mouse_pos):
                reset_game()
        
    if play:
        keys = pygame.key.get_pressed()


        screen.fill((30, 30, 30))

        #user movement
        if keys[pygame.K_UP]:
            user_paddle_rect.y -= abs(SPEED)  # In Pygame, Y decreases as you go UP
        if keys[pygame.K_DOWN]:
            user_paddle_rect.y += abs(SPEED)

        #special moves
        if keys[pygame.K_SPACE]:
            BALL_SPEED = BALL_SPEED + 1.5
            g = max(0, g - 34)
            b = max(0, b - 34)
        if keys[pygame.K_a]:
            if user_paddle_rect.height < 200:
                user_paddle_rect.height = user_paddle_rect.height + 2
                SPEED = SPEED - 0.1
        if keys[pygame.K_f]:
            if user_paddle_rect.height > 50:
                user_paddle_rect.height = user_paddle_rect.height - 2
                SPEED = SPEED + 0.1


        #Bot speeds
        dif_y = ball_rect.centery - bot_paddle_rect.centery
        BOT_SPEED = abs(kp * dif_y)

        score_text = small_font.render(f"Player: {user_score} Bot: {bot_score}", True, (255,255,255))
        score_text_rect = score_text.get_rect(center = (WINDOW_WIDTH - 100, 50))

        screen.blit(score_text, score_text_rect)


        #paddles
        pygame.draw.rect(screen, (255,255,255), user_paddle_rect)
        pygame.draw.rect(screen, (255,255,255), bot_paddle_rect)

        if user_paddle_rect.y < 0:
            user_paddle_rect.y = WINDOW_HEIGHT
        elif user_paddle_rect.y > WINDOW_HEIGHT:
            user_paddle_rect.y = 0

    
        #ball
        pygame.draw.rect(screen, (255, g, b ), ball_rect, border_radius=ball_radius)

        ball_rect.x += ball_direction * BALL_SPEED
        ball_rect.y += ball_vel_y

        #ball hitting paddle
        if ball_rect.colliderect(user_paddle_rect) or ball_rect.colliderect(bot_paddle_rect):
            ball_direction = ball_direction * -1
            ball_vel_y = random.randint(-6, 6)
            BALL_SPEED = BALL_SPEED + 1
            g = max(0,g - 17)
            b = max(0, b - 17)

            

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
            bot_score = bot_score + 1

        if ball_rect.x < 0:
            play = False
            outcome = "You Won"
            user_score = user_score + 1

    else:
        screen.fill((30,30,30))

        text_1 = font.render("Game Over", True, (255,255,255))
        text_rect_1 = text_1.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        text_2 = font.render(outcome, True, (255,255,255))
        text_rect_2 = text_2.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))      

        screen.blit(text_1, text_rect_1)
        screen.blit(text_2, text_rect_2)

        #button
        button_rect = pygame.Rect(WINDOW_WIDTH - 120, WINDOW_HEIGHT - 100, 100, 80)
        pygame.draw.rect(screen, (255, 255, 255), button_rect)

        button_text = small_font.render("Play Again", True, (0,0,0))
        button_text_rect = button_text.get_rect(center=button_rect.center)

        screen.blit(button_text, button_text_rect)

        #Is it clicked
        mouse_pos = pygame.mouse.get_pos()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
