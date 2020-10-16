import pygame
import random
import time
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

DISPLAY_SIZE = 720
screen = pygame.display.set_mode((DISPLAY_SIZE, DISPLAY_SIZE))
screen.fill((0, 0, 0))
board = []
BOARD_SIZE = 20
BLOCK_SIZE = DISPLAY_SIZE/BOARD_SIZE
clock = pygame.time.Clock()

# snake class
class Snake:

    squares = []
    length = 3
    direction = 'w'

    # snake class constructor requires starting row and column
    def __init__(self, row, col):
        self.squares.append((row+2, col))
        self.squares.append((row+1, col))
        self.squares.append((row, col))


    def move_snake(self, move):
        self.squares.append(move)
        self.squares.pop(0)

    def extend_snake(self, move):
        self.squares.append(move)
        self.length+=1


# snake food class
class Food:

    def __init__(self, row, col):
        self.row = row
        self.col = col

# function to initialise the game board
def init_board():
    for i in range(BOARD_SIZE):
        list = []
        for j in range(BOARD_SIZE):
            list.append(0)
        board.append(list)

# function to print out the board to console
def print_board():
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 1:
                block = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                block.fill((255, 255, 255))
                screen.blit(block, (j*BLOCK_SIZE,i*BLOCK_SIZE))
            elif board[i][j] == 2:
                block = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                block.fill((255, 0, 0))
                screen.blit(block, (j*BLOCK_SIZE,i*BLOCK_SIZE))
            else:
                pass

# function to update the board representation
def update_board(snake, food):
    for i in range(len(board)):
        for j in range(len(board[0])):
            tuple = (i, j)
            if tuple in snake.squares:
                board[i][j] = 1
            elif tuple == (food.row, food.col):
                board[i][j] = 2
            else:
                board[i][j] = 0

def near_danger(snake):
    head = snake.squares[-1]
    tup = (0, 0, 0) # left, straight, right
    if snake.direction == 'w':
        if head[0] - 1 < 0 or ((head[0] - 1, head[1]) in snake.squares):
            tup[1] = 1
        if head[1] - 1 < 0 or ((head[0], head[1] - 1) in snake.squares):
            tup[0] = 1
        if head[1] + 1 >= BOARD_SIZE or ((head[0], head[1] + 1) in snake.squares):
            tup[2] = 1
    if snake.direction == 's':
        if head[0] + 1 >= BOARD_SIZE or ((head[0] + 1, head[1]) in snake.squares):
            tup[1] = 1
        if head[1] - 1 < 0 or ((head[0], head[1] - 1) in snake.squares):
            tup[2] = 1
        if head[1] + 1 >= BOARD_SIZE or ((head[0], head[1] + 1) in snake.squares):
            tup[0] = 1
    if snake.direction == 'a':
        if head[0] - 1 < 0 or ((head[0] - 1, head[1]) in snake.squares):
            tup[2] = 1
        if head[1] - 1 < 0 or ((head[0], head[1] - 1) in snake.squares):
            tup[1] = 1
        if head[0] + 1 >= BOARD_SIZE or ((head[0] + 1, head[1]) in snake.squares):
            tup[0] = 1
    if snake.direction == 'd':
        if head[0] - 1 < 0 or ((head[0] - 1, head[1]) in snake.squares):
            tup[0] = 1
        if head[0] + 1 >= BOARD_SIZE or ((head[0] + 1, head[1]) in snake.squares):
            tup[2] = 1
        if head[1] + 1 >= BOARD_SIZE or ((head[0], head[1] + 1) in snake.squares):
            tup[1] = 1
            
    return tup

# function to perform collision detection and return False on collision, or True otherwise
def check_no_collision(snake, food):
    head = snake.squares[-1]
    tup = (food.row, food.col)

    if snake.direction == 'w':
        if head[0] - 1 < 0 or ((head[0] - 1, head[1]) in snake.squares):
            return False
        else:
            move = ((head[0] - 1), head[1])
            if tup == move:
                snake.extend_snake(move)
                new_food_position(snake, food)
            else:
                snake.move_snake(move)
    elif snake.direction == 's':
        if head[0] + 1 >= BOARD_SIZE or ((head[0] + 1, head[1]) in snake.squares):
            return False
        else:
            move = ((head[0] + 1), head[1])
            if tup == move:
                snake.extend_snake(move)
                new_food_position(snake, food)
            else:
                snake.move_snake(move)
    elif snake.direction == 'a':
        if head[1] - 1 < 0 or ((head[0], head[1] - 1) in snake.squares):
            return False
        else:
            move = (head[0], (head[1] - 1))
            if tup == move:
                snake.extend_snake(move)
                new_food_position(snake, food)
            else:
                snake.move_snake(move)
    elif snake.direction == 'd':
        if head[1] + 1 >= BOARD_SIZE or ((head[0], head[1] + 1) in snake.squares):
            return False
        else:
            move = (head[0], (head[1] + 1))
            if tup == move:
                snake.extend_snake(move)
                new_food_position(snake, food)
            else:
                snake.move_snake(move)
    return True

# function to randomly find a new place to put the food
def new_food_position(snake, food):
    while(True):
        row = random.randint(0, BOARD_SIZE-1)
        col = random.randint(0, BOARD_SIZE-1)
        if (row, col) not in snake.squares:
            food.row = row
            food.col = col
            return

def main():
    snake = Snake(10, 10)
    food = Food(0, 0)
    init_board()
    new_food_position(snake, food)
    update_board(snake, food)
    print_board()
    pygame.display.flip()
    clock.tick(5)

    while(True):

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    break
                elif event.type == QUIT:
                    break
                elif event.key == K_w:
                    snake.direction = 'w'
                elif event.key == K_s:
                    snake.direction = 's'
                elif event.key == K_a:
                    snake.direction = 'a'
                elif event.key == K_d:
                    snake.direction = 'd'

        screen.fill((0, 0, 0))
        if check_no_collision(snake, food):
            update_board(snake, food)
            print_board()
            pygame.display.flip()
            clock.tick(5)
        else:
            break

    print('Game Over')

if __name__ == "__main__":
    main()
