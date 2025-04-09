import pygame
import sys
import random
import sqlite3
conn = sqlite3.connect('snake_game.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS user_score (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    score INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
''')
conn.commit()
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLOCK_SIZE = 20
clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
username = input("Введи своё имя: ")
cursor.execute('SELECT id FROM user WHERE username = ?', (username,))
user = cursor.fetchone()
if user:
    user_id = user[0]
    cursor.execute('SELECT score, level FROM user_score WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        start_score, start_level = user_data
        print(f"Пам парам, пам парам, {username}! Уровень: {start_level}, Очки: {start_score}")
    else:
        cursor.execute('INSERT INTO user_score (user_id, score, level) VALUES (?, 0, 1)', (user_id,))
        conn.commit()
        start_score = 0
        start_level = 1
else:
    cursor.execute('INSERT INTO user (username) VALUES (?)', (username,))
    conn.commit()
    user_id = cursor.lastrowid
    cursor.execute('INSERT INTO user_score (user_id, score, level) VALUES (?, 0, 1)', (user_id,))
    conn.commit()
    start_score = 0
    start_level = 1

def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, GREEN, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])

def show_message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH/6, HEIGHT/3])

def save_game(score, level):
    cursor.execute('UPDATE user_score SET score = ?, level = ? WHERE user_id = ?', (score, level, user_id))
    conn.commit()

def gameLoop():
    snake_speed = 10 + (start_level - 1) * 5

    game_over = False
    game_close = False
    x = WIDTH / 2
    y = HEIGHT / 2
    x_change = 0
    y_change = 0
    snake_list = []
    snake_length = 1
    foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    score = start_score
    level = start_level
    foods_eaten = 0
    while not game_over:
        while game_close:
            screen.fill(BLACK)
            show_message("Ты проиграл! Q - выйти, C - заново", RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(score, level)
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_p:  # пауза
                    save_game(score, level)
                    paused = True
                    while paused:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_p:
                                    paused = False

        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        x += x_change
        y += y_change
        screen.fill(WHITE)
        pygame.draw.rect(screen, RED, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(snake_list)
        value = score_font.render("Очки: " + str(score) + " Уровень: " + str(level), True, BLACK)
        screen.blit(value, [0, 0])
        pygame.display.update()
        if x == foodx and y == foody:
            foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            snake_length += 1
            score += 10
            foods_eaten += 1

            if foods_eaten % 5 == 0:
                level += 1
                snake_speed += 3

        clock.tick(snake_speed)
    pygame.quit()
    save_game(score, level)
    sys.exit()

gameLoop()
