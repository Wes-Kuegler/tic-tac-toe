import pygame

# pygame setup
pygame.init()
screen_width = 640
screen_height = 640
screen_center = screen_width / 2, screen_height / 2
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
dt = 0

# Board setup
tile_size = 200 # Length of each side of each tile in the board
tile_count = 3 # Number of tiles in a row/column of the board
tile_border_width = 4
board = [[]]

def draw_board():
    board_square = pygame.Rect(0, 0, tile_size * tile_count, tile_size * tile_count)
    board_square.center = screen_center
    pygame.draw.rect(screen, "white", board_square) 
    for row in range(tile_count):
        for column in range(tile_count): 
            tile = pygame.Rect(column * tile_size, row * tile_size, tile_size, tile_size)
            tile.top += board_square.top
            tile.left += board_square.left
            tile.inflate_ip(-tile_border_width, -tile_border_width)
            pygame.draw.rect(screen, "black", tile) 

while running: # each frame
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    draw_board()
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
