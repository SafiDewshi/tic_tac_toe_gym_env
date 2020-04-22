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
        self.default_reward = 0
        self.invalid_move_reward = -10
        self.win_reward = 1
        self.loss_reward = -1
        self.active_player = 1

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
        """Execute one timestep.
        Args:
            action (coordinate to play piece

        Returns:
            Observation
            Reward
            Done
            Additional Information
            """

        done = False
        reward = self.default_reward
        invalid_move_reward = self.invalid_move_reward
        win_reward = self.win_reward
        loss_reward = self.loss_reward
        self.active_player = self.turn % 2 + 1

        # Check move is not invalid
        if self._invalid_move(action):
            return self.board, invalid_move_reward, True

        # update the board with provided move
        self._take_action(action)
        self.turn += 1

        # check move does not end the game
        if self._game_over():
            done = True
            winner = self._game_over()
            if winner == self.active_player:
                reward = win_reward
            else:
                reward = loss_reward

        return self.board, reward, done

    def reset(self):
        # reset environment to initial state
        self.board = np.zeros((3, 3))
        self.turn = 0
        return self.board

    def render(self, mode='human'):
        # render environment to screen
        self._draw_board()

        pass

    def close(self):
        pass

    def _take_action(self, action):
        """update the board with the provided action (n,n), 0=<n=<2"""
        self.board[action] = self.active_player

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
