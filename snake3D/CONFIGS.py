# snake parameters
from ursina import color

SNACK_COLOR = color.red

# map grid size
MAP_SIZE_X = 20
MAP_SIZE_Y = 15

# make snake more smooth
IS_SNAKE_SMOOTH = True
# start position of the snake
SNAKE_POS0 = (MAP_SIZE_X//2, MAP_SIZE_Y//2, 0)
# snake head color
SNAKE_COLOR = color.green
# snake tail color
SNAKE_TAIL_COLOR = color.blue
# snake speed
SNAKE_DT = 0.15 # sleep in seconds
# snake eyes color
EYE_COLOR = color.black

# display
DISPLAY_WIDTH = 1920
DISPLAY_HEIGHT = 1080


# pause key
KEY_PAUSE = 'p'
# KEY_LEFT = 'a'
# KEY_RIGHT = 'd'
# KEY_UP = 'w'
# KEY_DOWN = 's'
KEY_LEFT = 'arrow_left'
KEY_RIGHT = 'arrow_right'
KEY_UP = 'arrow_up'
KEY_DOWN = 'arrow_down'
