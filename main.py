import pygame
import sys
import random
pygame.init()



WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-понг")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


FPS = 60
clock = pygame.time.Clock()


PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 7
AI_PADDLE_SPEED = 5


BALL_SIZE = 20
BALL_SPEED_X = 5
BALL_SPEED_Y = 5


SCORE_FONT = pygame.font.SysFont("Arial", 30)



class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= PADDLE_SPEED

    def move_down(self):
        if self.rect.bottom < HEIGHT:
            self.rect.y += PADDLE_SPEED

    def ai_move(self, ball):

        if self.rect.centery < ball.rect.centery and self.rect.bottom < HEIGHT:
            self.rect.y += AI_PADDLE_SPEED
        elif self.rect.centery > ball.rect.centery and self.rect.top > 0:
            self.rect.y -= AI_PADDLE_SPEED

        if random.randint(0, 100) < 10:  # 10% вероятность
            self.rect.y += random.choice([-AI_PADDLE_SPEED, AI_PADDLE_SPEED])

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self, window):
        pygame.draw.rect(window, WHITE, self.rect)


class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x *= -1
        self.speed_y *= -1

    def draw(self, window):
        pygame.draw.ellipse(window, WHITE, self.rect)


def draw_score(window, score_a, score_b):
    score_text = SCORE_FONT.render(f"Игрок: {score_a}    Компьютер: {score_b}", True, WHITE)
    window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))


def main():
    # Создание ракеток и мяча
    paddle_a = Paddle(20, HEIGHT // 2 - PADDLE_HEIGHT // 2)  # Игрок
    paddle_b = Paddle(WIDTH - 20 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)  # Компьютер
    ball = Ball(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2)

    score_a = 0
    score_b = 0

    running = True
    while running:
        clock.tick(FPS)
        WINDOW.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()


        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            paddle_a.move_up()
        if keys[pygame.K_DOWN]:
            paddle_a.move_down()


        paddle_b.ai_move(ball)
        ball.move()


        if ball.rect.colliderect(paddle_a.rect):
            ball.speed_x *= -1
            ball.rect.left = paddle_a.rect.right

        if ball.rect.colliderect(paddle_b.rect):
            ball.speed_x *= -1
            ball.rect.right = paddle_b.rect.left


        if ball.rect.left <= 0:
            score_b += 1
            ball.reset()
        if ball.rect.right >= WIDTH:
            score_a += 1
            ball.reset()


        paddle_a.draw(WINDOW)
        paddle_b.draw(WINDOW)
        ball.draw(WINDOW)
        draw_score(WINDOW, score_a, score_b)


        pygame.display.flip()

if __name__ == "__main__":
    main()
