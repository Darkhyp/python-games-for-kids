"""
main class for "make 4 inline" classical game using pygame module
20/11/2020
Author A.V.Korovin [a.v.korovin73@gmail.com]
"""
import sys
import numpy as np
import pygame

from common import message_box, make_sound
from .CONFIGS import *
from .grid import Grid
from .tools import placer_pion, coordinate
from rougejaune.network import Network

pygame.font.init()
myfont = pygame.font.SysFont('monospace', 22)


class Players:
    _isReady = False
    _moves = [-1, -1]
    _isPlayerConnected = [False, False]

    def __init__(self, id_game):
        self.id_game = id_game

    def connected(self):
        return self._isReady

    def set_connection(self,p,val:bool=False):
        self._isPlayerConnected[p] = val
        self._isReady = self._isPlayerConnected[0] and self._isPlayerConnected[1]

    def get_connection(self,p):
        return self._isPlayerConnected[p]

    def reset_moves(self):
        self._moves = [-1, -1]

    def get_move(self, player):
        return self._moves[player]

    def set_move(self, player, move):
        self._moves[player] = move


def print_central_text(surface, message):
    surface.fill(BACKGROUND_COLOR)
    font = pygame.font.SysFont("comicsans", 28)
    text = font.render(message, True, (255, 255, 255))
    surface.blit(text, ((DISPLAY_SIZE[0] - text.get_width()) / 2, (DISPLAY_SIZE[1] - text.get_height()) / 2))
    pygame.display.update()


def put_ball(surface,ball,coordinate, isLimited=False):
    x, y = coordinate
    x -= ball.get_width() / 2
    if isLimited:
        y = (GRID_STEP[1]-ball.get_height())/2
        x = 0 if x<0 else x
        x = x if x<DISPLAY_SIZE[0]-ball.get_width() else DISPLAY_SIZE[0]-ball.get_width()
    else:
        y -= ball.get_height() / 2
    surface.blit(ball, (x, y))


class Game:
    game_over = True
    id_player = None

    def __init__(self):
        # init pygame display
        self.surface = pygame.display.set_mode(DISPLAY_SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
        pygame.display.set_caption('rouge contre jaune')

        # load ball images
        ball_red = pygame.image.load(BALL_RED_IMAGE).convert_alpha()
        ball_yellow = pygame.image.load(BALL_YELLOW_IMAGE).convert_alpha()
        ball_red = pygame.transform.scale(ball_red, (GRID_STEP[0]-GRID_THICKNESS,GRID_STEP[1]-GRID_THICKNESS))
        ball_yellow = pygame.transform.scale(ball_yellow, (GRID_STEP[0]-GRID_THICKNESS,GRID_STEP[1]-GRID_THICKNESS))
        self.balls = (ball_red,ball_yellow)

        self.clock = pygame.time.Clock()

        # initialize background class
        self.grid = Grid(self.surface, GRID_NXY, GRID_STEP)

        # initialize game data
        self.restart()
        pygame.init()

    def restart(self):
        # number of turns in the game
        self.game_turn = 0
        # lines for visualisation of successful combinations
        self.winner = []
        # initialize matrix for the game
        self.game_matrix = -np.ones(GRID_NXY,dtype=int)
        # test only
        # self.game_matrix = np.array(
        #       [[-1, -1, -1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1],
        #        [ 0, -1, -1, -1, -1, -1],
        #        [ 1,  0, -1, -1, -1, -1],
        #        [ 1,  1,  0, -1, -1, -1],
        #        [ 0,  1,  1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1]])
        #
        # self.game_matrix = np.array(
        #       [[-1, -1, -1, -1, -1, -1],
        #        [ 1,  1,  0,  0, -1, -1],
        #        [ 0,  0,  0,  1, -1, -1],
        #        [ 1,  0,  1, -1, -1, -1],
        #        [ 1,  1,  0, -1, -1, -1],
        #        [ 0,  1,  1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1]])

    def wait_server_connection(self):
        wait = True

        # wait for game start
        while wait:
            self.clock.tick(60)
            print_central_text(self.surface,"Click to Play!")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    wait = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    wait = False

        # create Network instance and run main game loop
        self.net = Network((SERVER_ADDR,SERVER_PORT))
        recived_data = self.net.get_player()
        if recived_data is None:
            print("Network did not found. Run common loop")
        else:
            self.id_player = int(recived_data)
            print(f"You are player{self.id_player}")

            is_opponent = False
            while not is_opponent:
                self.clock.tick(60)
                print_central_text(self.surface,"Wait another player connection")

                try:
                    players = self.net.send("reset")
                    is_opponent = players.connected()
                except Exception as e:
                    print("Couldn't get game: ", e)

                pygame.time.delay(150)

        pygame.event.clear()
        # start game loop for network game
        self.mainloop()

    def mainloop(self):
        """
        main loop
        """
        while self.game_over:
            self.clock.tick(10)
            pygame.time.delay(150)

            # redraw game objects
            self.redraw()

            # define which player is in this turn
            player = self.game_turn % 2

            # ball position ('-1' means incorrect position )
            col_placed_ball = -1
            if self.id_player is not None and player!=self.id_player: # show opponent move if exist
                # try to get data from the server
                try:
                    players = self.net.send("get")
                    col_placed_ball = players.get_move(player)
                    if col_placed_ball!=-1:
                        # reset move in server
                        self.net.send('reset')
                except Exception as e:
                    self.game_over = False
                    print("Couldn't get game: ", e)
                pygame.event.clear()
            else:
                # show new unplaced ball
                x,y = pygame.mouse.get_pos()
                col = int(x // GRID_STEP[0])
                put_ball(self.surface, self.balls[player], (x,y), isLimited=True)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # pygame.quit()
                        sys.exit()
                    if event.type==pygame.MOUSEMOTION:
                        pass
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        col_placed_ball = col

            # refresh image
            pygame.display.flip()
            pygame.display.update()

            # ball is placed, check winner
            if col_placed_ball!=-1:
                isPlaced,self.game_matrix,self.winner = placer_pion(player, col_placed_ball, self.game_matrix)
                if isPlaced:
                    if player == self.id_player:
                        # send to server
                        self.net.send(str(col_placed_ball))
                    if self.winner:
                        make_sound(2)

                        # redraw game objects to show winner combinations
                        self.redraw()

                        # add text
                        self.surface.blit(myfont.render(MESSAGE.WON.format(PLAYERS[player],self.game_turn),True, ((255,0,0),(255,255,0))[player]),(10,10))

                        # refresh image
                        pygame.display.flip()
                        pygame.display.update()

                        if self.id_player is not None:  # network game
                            if player==self.id_player:
                                message_box(MESSAGE.YOUWON.format(self.game_turn), MESSAGE.AGAIN)
                            else:
                                message_box(MESSAGE.YOULOST.format(self.game_turn), MESSAGE.AGAIN)
                            # reset game
                            self.net.send('reset')
                        else:
                            message_box(MESSAGE.WON.format(PLAYERS[player],self.game_turn), MESSAGE.AGAIN)

                        self.restart()
                    else:
                        self.game_turn += 1


    def redraw(self):  # redraw game objects
        # draw background image
        self.grid.draw()

        # draw placed balls
        for ix in range(self.game_matrix.shape[0]):
            for iy in range(self.game_matrix.shape[1]):
                player = self.game_matrix[ix,iy]
                if player!=-1:
                    put_ball(self.surface, self.balls[player], coordinate((ix, iy)))

        # draw lines for the winner combinations
        for line in self.winner:
            pygame.draw.line(self.surface, (255, 0, 0), coordinate(line[0]), coordinate(line[1]), 5)
