import logging
logger = logging.getLogger(__name__)

import gym

from .data import load_season
from .engine import GameEngine, GameInstance

def gym_init():
    if 'Cartola-v0' in gym.envs.registry.env_specs:
        return
    gym.envs.registration.register(
        id='Cartola-v0',
        entry_point='cartola_game.gym:CartolaEnv',
    )

class CartolaEnv(gym.Env):
    metadata = {
        'configure.required': True,
        'render.modes': ['human'],
    }

    def __init__(self):
        self.action_space = None
        self.observation_space = None

    def _configure(self, season, initial_money=100.0):
        season_data = load_season(season)
        self.game_engine = GameEngine(season_data)
        self.initial_money = initial_money

    def _reset(self):
        x = self.game_engine
        money = self.initial_money
        self.game_instance = GameInstance(x, money)
        return self.game_instance

    def _step(self, action):
        observation = self.game_instance
        reward = self.game_instance.run(action)
        done = self.game_instance.done
        return observation, reward, done, dict()

    def _render(self, mode='human', close=False):
        if close:
            return

        if not self.game_instance.states:
            print('(empty)')
            return

        s = self.game_instance.states[-1]
        print(s, '\n')

    def _seed(self, seed=None):
        return []
