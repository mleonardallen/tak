"""
Tak - A Beautiful Game
"""
import gym
import numpy as np
from env.space import ActionSpace
from env.board import Board
import copy

class TakEnv(gym.Env):
    """ TAK environment loop """

    def __init__(self, board_size, scoring, pieces, capstones):
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
        self.board = Board(size=board_size, pieces=pieces, capstones=capstones)
        self.action_space = ActionSpace(env=self)
        self.scoring = scoring
        self._reset()

    def _reset(self):
        self.done = False
        self.turn = 1
        self.board.reset()
        # multipart moves keep track of previous action
        self.continued_action = None

        return self._state()

    def _state(self):
        return {
            'board': copy.copy(self.board.state),
            'turn': self.turn,
            'black': self.board.get_available_pieces(Board.BLACK),
            'white': self.board.get_available_pieces(Board.WHITE)
        }

    def _step(self, action):

        if self.done:
            return self._feedback(action, reward=0, done = True)

        # if hallucinating action, make a copy to keep board pristine
        board = self.board
        if action.get('hallucinate'):
            board = copy.copy(self.board)

        board.act(action, self.turn)

        # game ends when road is connected
        if board.is_road_connected(self.turn):
            score = self.get_score(self.turn)
            return self._feedback(action, reward=score, done = True)

        # game ends if no open spaces or if any player runs out of pieces
        if (
            (not board.has_open_spaces()) or
            (len(board.get_available_piece_types(self.turn)) == 0)
        ):
            winner = board.get_flat_winner()
            score = self.get_score(winner)
            return self._feedback(action, reward=score, done = True)

        # update player turn
        if action.get('terminal'):
            self.turn *= -1
            self.continued_action = None
        else:
            self.continued_action = action

        # game still going
        return self._feedback(action, reward=0, done = False)

    def _feedback(self, action, reward, done):
        state = self._state()

        if not action.get('hallucinate') == True:
            self.done = done

        return state, reward, self.done, {}

    def _render(self, mode='human', close=False):
        if close:
            return

    def get_score(self, winner):
        if self.scoring == 'wins':
            return 1 if self.turn == winner else -1
        return self.board.get_points(self.turn, winner)
