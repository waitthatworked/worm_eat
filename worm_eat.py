# This is only the beginning - Jeremy 12/27/2021

import pygame
import time
import random

# initializes all imported Pygame modules
pygame.init()

# colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
brown = (150, 100, 75)
dark_brown = (55, 25, 10)
green = (0, 255, 0)

# creates a 800 x 600 window for playing the game
DIS_WIDTH = 800
DIS_HEIGHT = 600
dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))

# border parameters
BORDER_WIDTH = 40

# parameters of the bounding box
BB_WIDTH = DIS_WIDTH - 2*BORDER_WIDTH
BB_HEIGHT = DIS_HEIGHT - 2*BORDER_WIDTH

# Captions the window
pygame.display.set_caption('Worm Eat by Jeremy Chung')

clock = pygame.time.Clock()

SNAKE_SPEED = 15
SNAKE_GIRTH = 10
last_key = 4

# Game font
regular_font = pygame.font.SysFont('Helvetica', 50)
score_font = pygame.font.SysFont('Helvetica', BORDER_WIDTH-5)

music = pygame.mixer.music.load('halo_music.mp3')
pygame.mixer.music.play(-1)
eat_sound = pygame.mixer.Sound('munch.wav')

# Displays player score
def displayScore(score, game_over):
    score_string = "Score: " + str(score)

    score_colour = (255-5*score, 255, 255-5*score)

    if game_over:
        displayText(score_string, score_colour, -100, score_font)
    else:
        displayText(score_string, score_colour, -DIS_HEIGHT/2+30, score_font)

# Changes length of snake as it eats
def snakeGrow(SNAKE_GIRTH, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], SNAKE_GIRTH, SNAKE_GIRTH])

# displayText function
def displayText(text, color, y_trans, font):
    display_text = font.render(text, True, color)
    text_rect = display_text.get_rect(center=(DIS_WIDTH/2, DIS_HEIGHT/2 + y_trans))
    dis.blit(display_text, text_rect)

def gameLoop():
    game_over = False
    game_close = False

    global last_key

    # starting location of player
    x1 = DIS_WIDTH/2
    y1 = DIS_HEIGHT/2
    snake_list = []
    length_of_snake = 1

    # movement of player
    x1_change = 0
    y1_change = 0

    # defines location of food
    foodx = BORDER_WIDTH + SNAKE_GIRTH + round(random.randrange(0, BB_WIDTH - BORDER_WIDTH - 2*SNAKE_GIRTH) / 10.0) * 10.0
    foody = BORDER_WIDTH + SNAKE_GIRTH + round(random.randrange(0, BB_HEIGHT - BORDER_WIDTH - 2*SNAKE_GIRTH) / 10.0) * 10.0
    # main loop of the game
    while not game_close:
        # While the game is closed, prompts player to quit or play again
        while game_over == True:
            dis.fill(dark_brown)
            displayText("You Lost!", white, 0, regular_font)
            displayText("Quit (q) or Play Again (c) ?", white, 40, regular_font)

            displayScore(length_of_snake-1, game_over)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # user presses 'q', game closes
                    if event.key == pygame.K_q:
                        game_over = False
                        game_close = True
                    # user presses 'c', calls gameLoop
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():

            # if player quits, game over
            if event.type == pygame.QUIT:
                game_close = True



            # if a key is pressed...
            if event.type == pygame.KEYDOWN:
                print("l: " +str(last_key))
                # codes for the movement of the snake
                if event.key == pygame.K_UP and last_key != 1:
                    last_key = 0
                    y1_change = -SNAKE_GIRTH
                    x1_change = 0
                elif event.key == pygame.K_DOWN and last_key != 0:
                    last_key = 1
                    y1_change = SNAKE_GIRTH
                    x1_change = 0
                elif event.key == pygame.K_LEFT and last_key != 3:
                    last_key = 2
                    x1_change = -SNAKE_GIRTH
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and last_key != 2:
                    last_key = 3
                    x1_change = SNAKE_GIRTH
                    y1_change = 0

        # if the player steps out of bounds, game over
        if x1 >= BB_WIDTH+BORDER_WIDTH or x1 < BORDER_WIDTH or y1 >= BB_HEIGHT+BORDER_WIDTH or y1 <= BORDER_WIDTH:
            game_over = True

        # calculates player movement
        x1 += x1_change
        y1 += y1_change

        # display fill colour
        dis.fill(dark_brown)

        # draws the bounding box
        pygame.draw.rect(dis, brown, [BORDER_WIDTH, BORDER_WIDTH, BB_WIDTH, BB_HEIGHT])

        # draws food particles
        pygame.draw.rect(dis, green, [foodx, foody, SNAKE_GIRTH, SNAKE_GIRTH])

        # draws the snake
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_list.append(snake_Head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_Head:
                game_over = True

        snakeGrow(SNAKE_GIRTH, snake_list)
        displayScore(length_of_snake - 1, game_over)

        # updates the display every tick
        pygame.display.update()

        # if food is eaten, spawn new food, grow snake
        if x1 == foodx and y1 == foody:
            foodx = BORDER_WIDTH + SNAKE_GIRTH + round(random.randrange(0, BB_WIDTH - BORDER_WIDTH - 2*SNAKE_GIRTH) / 10.0) * 10.0
            foody = BORDER_WIDTH + SNAKE_GIRTH + round(random.randrange(0, BB_HEIGHT - BORDER_WIDTH - 2*SNAKE_GIRTH) / 10.0) * 10.0
            eat_sound.play()
            length_of_snake+=1

        # makes the clock tick at the speed of the snake
        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

gameLoop()

# print(event) - prints out all the actions that the snake does
# pygame.draw.rect(dis,blue,[200,150,10,10]) - creates a blue rectangle
# pygame.draw.rect(dis, black, [x1, y1, SNAKE_GIRTH, SNAKE_GIRTH])
