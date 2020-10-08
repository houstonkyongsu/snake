from pynput import keyboard
import random

board = []
BOARD_SIZE = 12
direction = 'u'

listener = keyboard.Listener(on_press=on_press)
listener.start()
# listener.join()

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
                print('o')
            elif board[i][j] == 2:
                print('x')
            else:
                print(' ')
        print('\n')

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

# function to detect keypresses and update the snake direction
def on_press(key):
    try:
        k = key.char
        if k == 'w': # up
            self.direction = 'w'
        elif k == 's': # down
            self.direction = 's'
        elif k == 'a': # left
            self.direction = 'a'
        elif k == 'd': # right
            self.direction = 'd'
    except: # ignore non-char keypresses
        pass

# function to perform collision detection and return False on collision, or True otherwise
def check_no_collision(snake, food):
    head = snake.squares[-1]
    tup = (food.row, food.col)

    if direction == 'w':
        if head[0] - 1 < 0 || ((head[0] - 1, head[1]) in snake.squares):
            return False
        else:
            if tup == (head[0] - 1, head[1]):
                snake.extend_snake(head[0] - 1, head[1])
            else:
                snake.move_snake(head[0] - 1, head[1])
    elif direction == 's':
        if head[0] + 1 >= BOARD_SIZE || ((head[0] + 1, head[1]) in snake.squares):
            return False
        else:
            if tup == (head[0] + 1, head[1]):
                snake.extend_snake(head[0] + 1, head[1])
            else:
                snake.move_snake(head[0] + 1, head[1])
    elif direction == 'a':
        if head[1] - 1 < 0 || ((head[0], head[1] - 1) in snake.squares):
            return False
        else:
            if tup == (head[0], head[1] - 1):
                snake.extend_snake(head[0], head[1] - 1)
            else:
                snake.move_snake(head[0], head[1] - 1)
    elif direction == 'd':
        if head[1] + 1 >= BOARD_SIZE || ((head[0], head[1] + 1) in snake.squares):
            return False
        else:
            if tup == (head[0], head[1] + 1):
                snake.extend_snake(head[0], head[1] + 1)
            else:
                snake.move_snake(head[0], head[1] + 1)
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
    snake = Snake(5, 5)
    food = Food(0, 0)
    new_food_position(snake, food)
    update_board(snake, food)

    while(True):

        if check_no_collision(snake, food):
            update_board(snake, food)
        else:
            break

if __name__ == "__main__":
    main()

# snake class
class Snake:

    squares = []
    length = 1

    # snake class constructor requires starting row and column
    def __init__(self, row, col):
        squares.append((row, col))

    def move_snake(row, col):
        squares.append((row, col))
        squares.pop(0)

    def extend_snake(row, col):
        squares.append((row, col))
        length+=1

# snake food class
class Food:

    def __init__(self, row, col):
        self.row = row
        self.col = col
