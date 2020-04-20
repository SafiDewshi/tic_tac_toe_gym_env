import gym
from gym import spaces
import numpy as np


class TicTacToe(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, **kwargs):
        super(TicTacToe, self).__init__()

        # Define action and observation space
        # They must be gym.spaces objects    # Example when using discrete actions:
        # self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        # Example for using image as input:
        # self.observation_space = spaces.Box(
        #     low=0,
        #     high=255,
        #     shape=(HEIGHT, WIDTH, N_CHANNELS),
        #     dtype=np.uint8
        # )
        self.reward_range = (-10, 1)
        self.board = np.zeros((3, 3))
        self.turn = 0
        self.active_player = self.turn % 2

        self.action_space = spaces.Box(
            low=np.array([0, 0]),
            high=np.array([2, 2]),
            dtype=int
        )

        self.observation_space = spaces.Box(
            low=np.array([0, 0]),
            high=np.array([2, 2]),
            dtype=int
        )

    def step(self, action):
        # execute one timestep
        done = False
        reward = 0

        self._take_action(action)
        self.step += 1

        if self._invalid_move(action):
            done = True
            reward = -10

        if self._game_over():
            done = True

        return self.board, reward, done

    def reset(self):
        # reset environment to initial state
        self.board = np.zeros((3, 3))
        self.turn = 0

    def render(self, mode='human'):
        # render environment to screen
        self._draw_board()

        pass

    def close(self):
        pass

    def _take_action(self, action):
        #
        pass

    def _invalid_move(self, action):
        return self.board[action] != 0

    def _game_over(self):
        """ checks if the game is over and returns the winning player or -1 if there is no winner"""
        for i in range(len(self.board)):
            if self.board[i, 0] != 0:
                if all([x == self.board[i, 0] for x in self.board[i]]):
                    return self.board[i, 0]
            if self.board[0, i] != 0:
                if all([x == self.board[0, i] for x in self.board[:, i]]):
                    return self.board[0, i]

        if self.board[0, 0] != 0:
            diag = np.diagonal(self.board)
            if all(x == diag[0] for x in diag):
                return self.board[0, 0]
        if self.board[0, 2] != 0:
            invdiag = np.diagonal(np.fliplr(self.board))
            if all(x == invdiag[0] for x in invdiag):
                return self.board[0, 2]
        if np.count_nonzero(self.board) == 9:
            return -1
        return False

        pass

    def _draw_board(self):
        """renders the board"""
        d = {0: " ", 1: "X", 2: "O"}
        # dict to translate ints to X and O

        b = np.vectorize(d.get)(self.board.astype(int))
        print(
            f"{b[0, 0]}|{b[0, 1]}|{b[0, 2]}\n"
            "-+-+-\n"
            f"{b[1, 0]}|{b[1, 1]}|{b[1, 2]}\n"
            "-+-+-\n"
            f"{b[2, 0]}|{b[2, 1]}|{b[2, 2]}\n"
        )
