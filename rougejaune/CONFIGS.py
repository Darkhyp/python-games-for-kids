# networt paramenters
SERVER_ADDR = '192.168.1.28'
SERVER_PORT = 5555


# French
PLAYERS = ('rouge','jaune')
MESSAGE = lambda: ()
MESSAGE.YOULOST = 'Vous aver perdu en {} tours'
MESSAGE.YOUWON = 'Vous aver gagné en {} tours'
MESSAGE.WON = 'Le joueur {} a gagné en {} tours'
MESSAGE.AGAIN = 'Rejouer'
#English
# MESSAGE.WON = 'Player {} won in {} turns'
# MESSAGE.AGAIN = 'Play again'

GRID_STEP = (60,60)
GRID_NXY = (8,6)
GRID_COLOR = (60,155,40)
GRID_BACKGROUND = (25,25,45)
GRID_THICKNESS = 10

DISPLAY_SIZE = (GRID_STEP[0]*GRID_NXY[0],GRID_STEP[1]*(GRID_NXY[1]+1))

BACKGROUND_COLOR = (0,0,0)

BALL_RED_IMAGE = r'rougejaune\red-ball.png'
BALL_YELLOW_IMAGE = r'rougejaune\yellow-ball.png'
