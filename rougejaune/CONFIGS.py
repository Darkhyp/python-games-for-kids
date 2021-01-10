# networt paramenters
SERVER_ADDRESS = '192.168.1.28'
SERVER_PORT = 5555

# French messages and player names
PLAYERS = ('rouge', 'jaune')
MESSAGE = lambda: ()
MESSAGE.YOULOST = 'Vous aver perdu en {} tours'
MESSAGE.YOUWON = 'Vous aver gagné en {} tours'
MESSAGE.WON = 'Le joueur {} a gagné en {} tours'
MESSAGE.AGAIN = 'Rejouer'
# English messages and player names
# PLAYERS = ('red', 'yellow')
# MESSAGE.WON = 'Player {} won in {} turns'
# MESSAGE.AGAIN = 'Play again'

# defining the background grid
GRID = lambda: ()
GRID.STEP = (60, 60)
# the number of grids along the x and y axes
GRID.NXY = (8, 6)
GRID.COLOR = (60, 155, 40)
GRID.BACKGROUND = (25, 25, 45)
GRID.THICKNESS = 10

# set display size
DISPLAY_SIZE = (GRID.STEP[0] * GRID.NXY[0], GRID.STEP[1] * (GRID.NXY[1] + 1))

# set background color
BACKGROUND_COLOR = (0, 0, 0)  # black

# external images for balls
BALL_RED_IMAGE = r'rougejaune\red-ball.png'
BALL_YELLOW_IMAGE = r'rougejaune\yellow-ball.png'
