# snake parameters
from pygame import K_p

SNAKE_COLOR = (255,0,0)
SNAKE_POS0 = (10,10)

SNACK_COLOR = (0,255,0)
SNAKETAIL_COLOR = (0,0,255)
# to change the snake speed
SNAKE_DT = 0.15 # sleep in seconds
# snake eyes i_color
EYE_COLOR = (0,0,0)

# grid numbers
N_ROWS = 20
N_COLS = 20
# grid size
GRID_DX = 25
GRID_DY = 25
# grid i_color
GRID_COLOR = (150, 200, 150)

# display
DISPLAY_WIDTH = GRID_DX*N_ROWS
DISPLAY_HEIGHT = GRID_DY*N_COLS
# display background
BACKGROUND_COLOR = (0,30,0)


# pause key
PAUSE_KEY = K_p