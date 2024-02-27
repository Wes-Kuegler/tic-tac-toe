import pygame
from pygame import MOUSEBUTTONDOWN
from pygame import Rect
from enum import Enum

# pygame setup
pygame.init()
screen_width = 640
screen_height = 640
screen_center = screen_width / 2, screen_height / 2
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
dt = 0 # Elapsed time in millis since last frame
framerate = 60 # FPS
running = True

class BoardState(Enum):
    EMPTY = 0,
    X = 1,
    O = 2
    
# Board setup
tile_size = 200 # Length of each side of each tile in the board (minus the border width)
tile_border_width = 3
tile_count = 3 # Number of tiles in a row/column of the board
board = []
board_tiles = [] # For the actual rects being drawn to screen (for click detection)

# Board image setup (for drawing tile contents)
font = pygame.font.SysFont(None, 326)
icon_x = font.render("X", True, "blue")
icon_o = font.render("O", True, "blue")

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
            board_tiles[row][column] = tile # Store rect for later
            pygame.draw.rect(screen, "black", tile) 

            icon = None
            if board[row][column] == BoardState.X:
                icon = icon_x
            elif board[row][column] == BoardState.O:
                icon = icon_o

            if icon is not None:
                icon_rect = icon.get_rect()
                icon_rect.center = tile.center # Unsure why this produces an off-center image; font issue?
                icon_rect.top += 13 # Adjust for font's center offset
                screen.blit(icon, icon_rect)

def make_move(tile_index:tuple, move:BoardState): 
    board[tile_index[0]][tile_index[1]] = move

# Return the row,column index of the clicked tile, else None
def find_clicked_tile(position) -> tuple:
    for row in range(tile_count):
        for column in range(tile_count): 
            if board_tiles[row][column].collidepoint(position):
                return row,column
            
    return None

# Game setup
setup_board()

while running: # each frame
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            pressed_buttons = pygame.mouse.get_pressed()
            if pressed_buttons[0]: # left mouse click
                clicked_tile = find_clicked_tile(pygame.mouse.get_pos())
                if clicked_tile is not None: # If a tile was clicked on
                    make_move(clicked_tile, BoardState.X)

    screen.fill("white") # Color fill to remove last frame

    draw_board()
    pygame.display.flip() # Draw to screen

    # limit FPS by framerate
    dt = clock.tick(framerate) / 1000

pygame.quit()