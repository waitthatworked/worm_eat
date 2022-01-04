# This is only the beginning - Jeremy 12/27/2021

import pygame
import time
import random

# initializes all imported Pygame modules
pygame.init()

# colours
white = (255, 255, 255)
black = (0, 0, 0)
# semitrans_black = (0, 0, 0, 50)
red = (255, 0, 0)
blue = (0, 0, 255)
brown = (150, 100, 75)
dark_brown = (55, 25, 10)
green = (0, 255, 0)
worm_pink = (255, 100, 100)

# creates a 800 x 600 window for playing the game
DIS_WIDTH = 800
DIS_HEIGHT = 500
dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
background = pygame.image.load('images/dirt_block.png')

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

music = pygame.mixer.music.load('sounds/halo_music.mp3')
pygame.mixer.music.play(-1)
eat_sound = pygame.mixer.Sound('sounds/munch.wav')
womp_womp = pygame.mixer.Sound('sounds/womp_womp.wav')

# Displays player score
def displayScore(score, game_over):
    score_string = "Score: " + str(score)

    score_colour = (255-5*score, 255, 255-5*score)

    if game_over:
        displayText(score_string, score_colour, -100, score_font)
    else:
        displayText(score_string, score_colour, -DIS_HEIGHT/2+30, score_font)

# Changes length of snake as it eats
def drawSnake(SNAKE_GIRTH, snake_list, colour):
    for snake_segment in snake_list:
        pygame.draw.rect(dis, colour, [snake_segment[0], snake_segment[1], SNAKE_GIRTH, SNAKE_GIRTH])

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
    trail_list = []
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
        if game_over:
            womp_womp.play()
        while game_over:
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

        # fills the background with dirt_block
        dis.blit(background, [0,0])

        # draws the bounding box
        bounding_box = pygame.draw.rect(dis, brown, [BORDER_WIDTH, BORDER_WIDTH, BB_WIDTH, BB_HEIGHT])
        # bounding_box.set_alpha(100)

        # draws food particles
        pygame.draw.rect(dis, green, [foodx, foody, SNAKE_GIRTH, SNAKE_GIRTH])

        # snake_list is a list that tracks the x and y coordinates of the snake's head
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_list.append(snake_Head)

        # as the length of the snake_list exceeds the actual length of the snake,
        # we terminate the last segment of the snake
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        snail_trail = []
        snail_trail.append(x1)
        snail_trail.append(y1)
        trail_list.append(snail_trail)

        if len(trail_list) > length_of_snake+20:
            del trail_list[0]

        # if the snake runs into itself, game over
        for x in snake_list[:-1]:
            if x == snake_Head:
                game_over = True

        # draws the snail trail (under the snake)
        drawSnake(SNAKE_GIRTH, trail_list, dark_brown)

        #draws the snake
        drawSnake(SNAKE_GIRTH, snake_list, worm_pink)

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
