import pygame
from pygame import color
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
tile_count = 3 # Number of tiles in a row/column of the board
tile_border_width = 4
board = [[]]

# Board image setup (for drawing tile contents)
font = pygame.font.SysFont(None, 326)
icon_x = font.render("X", True, "blue")
icon_o = font.render("O", True, "blue")

def setup_board():
    for row in range(tile_count):
        board.append([])
        for column in range(tile_count): 
            board[row].append(BoardState.X)

def draw_board():
    board_square = pygame.Rect(0, 0, tile_size * tile_count, tile_size * tile_count)
    board_square.center = screen_center
    for row in range(tile_count):
        for column in range(tile_count): 
            tile = pygame.Rect(column * tile_size, row * tile_size, tile_size, tile_size)
            tile.top += board_square.top
            tile.left += board_square.left
            tile.inflate_ip(-tile_border_width, -tile_border_width) # Shrink tile to show border
            pygame.draw.rect(screen, "black", tile) 
            icon = None
            if board[row][column] == BoardState.X:
                icon = icon_x
            elif board[row][column] == BoardState.O:
                icon = icon_o

            if icon is not None:
                icon_centered = icon.get_rect()
                icon_centered = icon_centered.fit(tile)
                # icon_centered.center = tile.center
                screen.blit(icon, icon_centered)

setup_board()
while running: # each frame
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("white") # Color fill to remove last frame

    draw_board()
    pygame.display.flip() # Draw to screen

    # limit FPS by framerate
    dt = clock.tick(framerate) / 1000

pygame.quit()
