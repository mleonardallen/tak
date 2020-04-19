"""
Tak - A Beautiful Game
"""
import gym
import numpy as np
from tak_env.space import ActionSpace
import tak_env.board as Board
from tak_env.types import Player
from tak_env.viewer import Viewer
import copy

class TakEnv(gym.Env):
    """ TAK environment loop """

    metadata = {
        'render.modes': ['human'],
        'video.frames_per_second' : 50
    }

    def __init__(self, board_size, scoring, pieces, capstones, height):

        """
        Args:
            board_size: size of the TAK board
            pieces: number of regular pieces per player
            capstones: number of capstones per player
        """
        assert isinstance(board_size, int) and board_size >= 3 and board_size <= 8, 'Invalid board size: {}'.format(board_size)
        assert isinstance(pieces, int) and pieces >= 10 and pieces <= 50, 'Invalid number of pieces: {}'.format(pieces)
        assert isinstance(capstones, int) and capstones >= 0 and capstones <= 2, 'Invalid number of capstones: {}'.format(capstones)

        # set board properties
        self.board_size = board_size
        self.height = height
        self.capstones = capstones
        self.pieces = pieces

        self.action_space = ActionSpace(env=self)
        self.scoring = scoring
        self.viewer = Viewer(env=self)

        self.reset()

    def seed(self):
        pass

    def reset(self):

        self.done = False
        self.turn = np.random.choice([1, -1])
        self.reward = 0
        
        self.available_pieces = {}
        self.available_pieces[Player.WHITE.value] = {'pieces': self.pieces, 'capstones': self.capstones}
        self.available_pieces[Player.BLACK.value] = {'pieces': self.pieces, 'capstones': self.capstones}

        self.state = np.zeros((self.board_size, self.board_size, self.height))

        # multipart moves keep track of previous action
        self.continued_action = None

        return self.state

    def step(self, action):

        if self.done:
            return self.__feedback(action, reward=0, done=True)

        Board.act(self.state, action, self.available_pieces, self.turn)

        # game ends when road is connected
        if Board.is_road_connected(self.state, self.turn):
            score = self.__get_score(self.turn)
            return self.__feedback(action, reward=score, done=True)

        # game ends if no open spaces or if any player runs out of pieces
        if (
            (not Board.has_open_spaces(self.state)) or
            (len(Board.get_available_piece_types(self.available_pieces, self.turn)) == 0)
        ):
            winner = Board.get_flat_winner(self.state)
            score = self.__get_score(winner)
            return self.__feedback(action, reward=score, done=True)

        # update player turn
        if action.get('terminal'):
            self.turn *= -1
            self.continued_action = None
        else:
            self.continued_action = action

        # game still going
        return self.__feedback(action, reward=0, done=False)

    def render(self, mode='human', close=False):
        if close:
            return
        self.viewer.render(self.state)


    def __feedback(self, action, reward, done):

        self.done = done
        self.reward = reward

        return self.state, reward, self.done

    def __get_score(self, winner):
        if self.scoring == 'wins':
            return 1 if self.turn == winner else -1

        return Board.get_points(self.board_size, self.available_pieces, self.turn, winner)
