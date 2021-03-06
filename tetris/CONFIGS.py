# snake parameters
from pygame import K_p, K_LEFT, K_RIGHT, K_UP, K_DOWN

WHITE = (255, 255, 255)
GREY = (120, 120, 120)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 50, 0)
BLUE = (0, 0, 255)
PURPLE = (120, 0, 120)
SKYBLUE = (0, 186, 255)
YELLOW = (120, 120, 0)


# object definition
BLOCK_SPEED = 0.5
#  index | sub-block coordinates | color
BLOCK_LIST = ((0, {(0, 0), (1, 0), (2, 0), (3, 0)}, RED),
              (1, {(0, 0), (1, 0), (2, 0), (1, 1)}, GREEN),
              (2, {(0, 0), (1, 0), (1, 1), (2, 1)}, BLUE),
              (3, {(0, 1), (1, 1), (1, 0), (2, 0)}, PURPLE),
              (4, {(0, 0), (1, 0), (1, 1), (1, 2)}, YELLOW),
              (5, {(0, 0), (1, 0), (0, 1), (0, 2)}, SKYBLUE),
              (6, {(0, 0), (1, 0), (0, 1), (1, 1)}, GREY),
              )


# play region
# grid numbers
N_COLS = 10
N_ROWS = 20
# grid size
GRID_DX = 30
GRID_DY = GRID_DX
# grid i_color
GRID_COLOR = WHITE


# next panel (right)
NEXT_PANEL_WIDTH = 5*GRID_DX
NEXT_PANEL_HEIGHT = NEXT_PANEL_WIDTH


TOP_PANEL = 100
RIGHT_PANEL = NEXT_PANEL_WIDTH + 2*10
LEFT_PANEL = RIGHT_PANEL

# grid position
GRID_POS = (LEFT_PANEL, TOP_PANEL)

# left panel position
LEFT_PANEL_TEXT_POS = (10, TOP_PANEL + 10)

# right panel position
RIGHT_PANEL_TEXT_POS = (LEFT_PANEL + N_COLS * GRID_DX, TOP_PANEL + 5)
RIGHT_PANEL_POS = (LEFT_PANEL + N_COLS * GRID_DX + 10, TOP_PANEL + 50)

# display
DISPLAY_WIDTH = LEFT_PANEL + N_COLS * GRID_DX + RIGHT_PANEL
DISPLAY_HEIGHT = TOP_PANEL + N_ROWS * GRID_DY + 20
# display background
BACKGROUND_COLOR = BLACK




# pause key
PAUSE_KEY       = K_p
PLAYER_LEFT     = K_LEFT
PLAYER_RIGHT    = K_RIGHT
PLAYER_UP       = K_UP
PLAYER_DOWN     = K_DOWN