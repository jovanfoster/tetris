import pygame
import random, sys, time
from pygame.locals import *

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
CELL_SIZE = 20
TEMPLATE_WIDTH = 5
TEMPLATE_HEIGHT = 5

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

WHITE = (255, 255, 255)
BLUE = (0, 0, 125)
GREEN = (0, 125, 0)
YELLOW = (175, 175, 0)
RED = (125, 0, 0)
LIGHTBLUE = (50, 50, 205)
LIGHTGREEN =(50, 205, 50)
LIGHTYELLOW = (225, 225, 75)
LIGHTRED = (205, 50, 50)
BLACK = (0, 0, 0)

COLORS = [BLUE, GREEN, YELLOW, RED]
LIGHTCOLORS = [LIGHTBLUE, LIGHTGREEN, LIGHTYELLOW, LIGHTRED]
assert len(COLORS) == len(LIGHTCOLORS)

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = [
    S_SHAPE_TEMPLATE,
    Z_SHAPE_TEMPLATE,
    J_SHAPE_TEMPLATE,
    L_SHAPE_TEMPLATE,
    I_SHAPE_TEMPLATE,
    O_SHAPE_TEMPLATE,
    T_SHAPE_TEMPLATE
]

class Piece:
    def __init__(self, shape, x, y, rotation, color):
        self.shape = shape
        self.x = x
        self.y = y
        self.rotation = rotation
        self.color = color


# instantiates a new piece
def new_piece():
    shape = random.choice(PIECES)
    rotation = random.randrange(len(shape))
    x = 2
    y = -3
    color = random.randrange(len(COLORS))
    piece = Piece(shape, x, y, rotation, color)
    return piece


# uninitialize pygame and close the current window
def terminate():
    pygame.quit()
    sys.exit()


# draws box with color=color at x,y
def draw_box(x, y, color):
    x, y = get_coords(x, y)
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (x + 1, y + 1, CELL_SIZE - 1, CELL_SIZE - 1))
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (x + 1, y + 1, CELL_SIZE - 1, CELL_SIZE - 1), 3)


# draws the piece passed in by the piece argument
def draw_piece(piece, drawX=12, drawY=6):
    for x in range(TEMPLATE_WIDTH):
        for y in range(TEMPLATE_HEIGHT):
            if piece.shape[piece.rotation][y][x] != '.' and not above_board(drawY + y):
                draw_box(drawX + x, drawY + y, piece.color)


# draws the board
def draw_board(board):
    pygame.draw.rect(DISPLAYSURF, BLUE,
        (SCREEN_WIDTH / 2 - CELL_SIZE * BOARD_WIDTH / 2 - 3,
         SCREEN_HEIGHT - CELL_SIZE * BOARD_HEIGHT - 3,
         CELL_SIZE * BOARD_WIDTH + 6, CELL_SIZE * BOARD_HEIGHT + 3), 3)
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            if board[y][x] != '.':
                draw_box(x, y, board[y][x])


# converts x,y position into coordinates on the screen
def get_coords(x, y):
    x = (x * CELL_SIZE) + SCREEN_WIDTH / 2 - CELL_SIZE * BOARD_WIDTH / 2
    y = (y * CELL_SIZE) + SCREEN_HEIGHT - CELL_SIZE * BOARD_HEIGHT
    return x, y


# add current piece to the board
def add_to_board(board, currentpiece):
    for x in range(TEMPLATE_WIDTH):
        for y in range(TEMPLATE_HEIGHT):
            if currentpiece.shape[currentpiece.rotation][y][x] != '.':
                board[currentpiece.y + y][currentpiece.x + x] = currentpiece.color


# returns true if piece is above board
def above_board(y):
    return y < 0


# returns true if piece is on board
def on_board(x, y):
    if x < 0 or \
        x >= BOARD_WIDTH or \
        y >= BOARD_HEIGHT:
        return False
    return True


# returns true if piece is in a valid position
def valid_position(currentpiece, board, adjX=0, adjY=0):
    for x in range(TEMPLATE_WIDTH):
        for y in range(TEMPLATE_HEIGHT):
            if currentpiece.shape[currentpiece.rotation][y][x] != '.':
                if above_board(currentpiece.y + y):
                    continue
                if not on_board(currentpiece.x + x + adjX, currentpiece.y + y + adjY):
                    return False
                elif board[currentpiece.y + y + adjY][currentpiece.x + x + adjX] != '.':
                    return False

    return True


# return true if row is full
def completed_row(board, row):
    for x in range(BOARD_WIDTH):
        if board[row][x] == '.':
            return False
    return True


# draws text to the screen
def draw_text(font, text, color, x, y, antialising=True):
    textsurf = font.render(text, antialising, color)
    DISPLAYSURF.blit(textsurf, (x, y))


# load the main menu
def menu():
    image = pygame.image.load('media/title.png').convert()
    imagesurf = pygame.transform.rotozoom(image, 0, 0.25)
    DISPLAYSURF.blit(imagesurf, (SCREEN_WIDTH / 2 - imagesurf.get_width() / 2, 20,
                                imagesurf.get_width(), imagesurf.get_height()))

    pygame.display.update()

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                return

# load game over screen
def game_over():
    image = pygame.image.load('media/game_over.png').convert()
    #imagesurf = pygame.transform.rotozoom(image, 0, 0.25)
    DISPLAYSURF.blit(image, (SCREEN_WIDTH / 2 - image.get_width() / 2, 20,
                                image.get_width(), image.get_height()))

    pygame.display.update()

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == K_RETURN:
                    break
    run_game()


# starts a new game
def run_game():
    clock = pygame.time.Clock()
    basicfont = pygame.font.Font('freesansbold.ttf', 28)
    score = 0
    level = 0
    fallfreq = 1
    movefreq = 0.15
    board = [['.' for x in range(BOARD_WIDTH)]for y in range(BOARD_HEIGHT)]
    currentpiece = new_piece()
    nextpiece = new_piece()
    lastfalltime = time.time()
    lastmovetime = time.time()

    while 1:

        for x in range(BOARD_WIDTH):
            if board[0][x] != '.':
                game_over()

        # if a row is filled, delete that row
        for y in range(BOARD_HEIGHT):
            if completed_row(board, y):
                del board[y]
                blankrow = ['.'] * BOARD_WIDTH
                board.insert(0, blankrow)
                score += 100
                if fallfreq > 0.05: fallfreq -= 0.05
                level = score % 100

        key = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if (event.key == K_UP or event.key == K_w):
                    currentpiece.rotation = (currentpiece.rotation + 1) % len(currentpiece.shape)
                    if not valid_position(currentpiece, board):
                        currentpiece.rotation = (currentpiece.rotation - 1) % len(currentpiece.shape)
                elif (event.key == K_SPACE):
                    for y in range(currentpiece.y, BOARD_HEIGHT):
                        if not valid_position(currentpiece, board, adjY=(y - currentpiece.y)):
                            currentpiece.y = y - 1
                            break


        if time.time() - lastmovetime >= movefreq:
            # move if player is holding move key
            if (key[K_RIGHT] or key[K_d]) and \
                valid_position(currentpiece, board, adjX=1):
                        currentpiece.x += 1
                        lastmovetime = time.time()
            elif (key[K_LEFT] or key[K_a]) and \
                  valid_position(currentpiece, board, adjX=-1):
                        currentpiece.x -= 1
                        lastmovetime = time.time()
            elif (key[K_DOWN] or key[K_s]) and \
                  valid_position(currentpiece, board, adjY=1):
                        currentpiece.y += 1
                        lastmovetime = time.time()

        if time.time() - lastfalltime >= fallfreq:
            # if no space below, add piece to board and get new piece
            if not valid_position(currentpiece, board, adjY=1):
                add_to_board(board, currentpiece)
                currentpiece = nextpiece
                nextpiece = new_piece()
                lastfalltime = time.time()
            else:
                currentpiece.y += 1
                lastfalltime = time.time()

        DISPLAYSURF.fill(BLACK)

        draw_board(board)
        draw_piece(currentpiece, drawX=currentpiece.x, drawY=currentpiece.y)
        draw_piece(nextpiece)
        draw_text(basicfont, 'Score: %s' % score, WHITE, SCREEN_WIDTH / 2 + BOARD_WIDTH / 2 + 110, SCREEN_HEIGHT / 2 - 55)
        pygame.display.update()
        clock.tick(25 - (fallfreq / 1000))


def main():
    pygame.init()
    pygame.font.init()
    menu()
    run_game()


if __name__ == '__main__':
    main()