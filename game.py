import pygame
import random
from pygame import MOUSEBUTTONDOWN
from pygame import Rect
from enum import Enum

# pygame setup
pygame.init()
screen_width = 1000
screen_height = 640
screen_center = screen_width / 2, screen_height / 2
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
framerate = 60 # FPS
dt = 0 # Elapsed time in millis since last frame

class BoardState(Enum):
    EMPTY = 0,
    X = 1,
    O = 2
    
# Board setup
tile_size = 200 # Length of each side of each tile in the board (minus the border width)
tile_border_width = 3
tile_count = 3 # Number of tiles in a row/column of the board
board = [] # Game state
board_tiles = [] # For the actual rects being drawn to screen (for click detection)

# Board image setup (for drawing icons on the board)
font = pygame.font.SysFont(None, 326)
icon_x = font.render("X", True, "white")
icon_o = font.render("O", True, "white")

# End state text images
winner = font.render("Winner!", True, "red")
loser = font.render("Loser!", True, "red")

# Game state
player_turn = True
player_shape = BoardState.X
ai_shape = BoardState.O
player_victory = False
ai_victory = False

def setup_board():
    for row in range(tile_count):
        board.append([])
        board_tiles.append([])
        for column in range(tile_count): 
            board[row].append(BoardState.EMPTY)
            board_tiles[row].append(None)

def draw_board():
    board_square = Rect(0, 0, tile_size * tile_count, tile_size * tile_count)
    board_square.center = screen_center

    for row in range(tile_count):
        for column in range(tile_count): 
            tile = Rect(column * tile_size, row * tile_size, tile_size, tile_size)
            tile.top += board_square.top # Adjust by board position
            tile.left += board_square.left
            tile.inflate_ip(-tile_border_width * 2, -tile_border_width * 2) # Shrink tile to show border
            board_tiles[row][column] = tile # Store rect for click detection later
            pygame.draw.rect(screen, "black", tile) 

            icon = None
            if board[row][column] == BoardState.X:
                icon = icon_x
            elif board[row][column] == BoardState.O:
                icon = icon_o

            if icon is not None:
                icon_rect = icon.get_rect()
                icon_rect.center = tile.center # Unsure why this produces an off-center image; font issue?
                icon_rect.top += 13 # Adjust for the off-centeredness
                screen.blit(icon, icon_rect)
                
    if player_victory:
        screen.blit(winner, winner.get_rect(center = screen_center))
    elif ai_victory:
        screen.blit(loser, loser.get_rect(center = screen_center))

def move_and_check(position:tuple, move:BoardState): # Make a move and check for a winner
    board[position[0]][position[1]] = move
    victory_check()

def is_legal_move(position:tuple) -> bool:
    return board[position[0]][position[1]] == BoardState.EMPTY

def make_ai_move() -> bool: # Return true if a move was made, else false(no legal moves)
    legal_moves = []
    for row in range(tile_count):
        for column in range(tile_count): 
            move = (row, column)
            if is_legal_move(move):
                legal_moves.append(move)
    
    if len(legal_moves) == 0:
        return False
    else:
        random_move = legal_moves[random.randrange(0, len(legal_moves))]
        move_and_check(random_move, ai_shape)
        return True

# Return the row,column index of the tile at position (if any), else None
def find_tile(position) -> tuple:
    for row in range(tile_count):
        for column in range(tile_count): 
            if board_tiles[row][column].collidepoint(position):
                return row,column
    return None

def get_column(index, matrix:list = board) -> list:
    column = []
    for row in matrix:
        column.append(row[index])
    return column

def victory_check() -> bool: # Is the game over?
    global player_victory
    global ai_victory
    for row in board:
        if row.count(player_shape) == tile_count: #3 in a row!
            player_victory = True
        elif row.count(ai_shape) == tile_count:
            ai_victory = True
    
    for column in range(tile_count): 
        if get_column(column).count(player_shape) == tile_count:
            player_victory = True
        elif get_column(column).count(ai_shape) == tile_count: 
            ai_victory = True
    
    # still need to check diagonals
    return player_victory or ai_victory


# Game setup
setup_board()

# Game start
running = True
while running: # each frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if player_turn and not ai_victory:
                pressed_buttons = pygame.mouse.get_pressed()
                if pressed_buttons[0]: # left mouse click
                    clicked_tile = find_tile(pygame.mouse.get_pos())
                    if clicked_tile is not None: # If a tile was clicked on
                        if is_legal_move(clicked_tile):
                            move_and_check(clicked_tile, BoardState.X)
                            player_turn = False
    
    if not player_turn and not player_victory: # AI turn
        make_ai_move()
        player_turn = True

    screen.fill("white") # Color fill to remove last frame

    draw_board()
    pygame.display.flip() # Draw to screen

    # limit FPS by framerate
    dt = clock.tick(framerate) / 1000

pygame.quit()