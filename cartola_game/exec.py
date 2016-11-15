import gym
import re
import sys

from .data import load_season
from .engine import GameEngine, GameInstance
from .gym import gym_init
from .strategy import random_team

def engine_random(season):
    season_data = load_season(season)

    print('Cartola', season_data, '\n')

    x = GameEngine(season_data)
    i = GameInstance(x)

    total_score = 0.0
    while not i.done:
        print('[ Round', i.round_number, ']\n')
        data = i.data
        budget = i.total_money
        team = random_team(data, budget)

        print(team)
        team_value = data.price(team.players)
        print('\nTeam Price: {:.2f}'.format(team_value))
        print('Unused Money: {:.2f}'.format(budget - team_value))

        score = i.run(team)
        total_score += score

        print('\nScore: {:.2f}'.format(score))
        after_money = i.total_money
        print('Money: {:.2f}'.format(after_money))
        print('Variation: {:.2f}\n'.format(after_money - budget))

    print('...\n')
    print('Total Score: {:.2f}'.format(total_score))

def gym_random(season):
    print('Cartola', season, '\n')
    gym_init()

    env = gym.make('Cartola-v0')
    env.configure(season)

    total_reward = 0.0

    observation = env.reset()

    done = False
    while not done:
        action = select_action(observation)

        observation, reward, done, _ = env.step(action)
        total_reward += reward

        env.render()

    print('...\n')
    print('Total reward: {:.2f}'.format(total_reward))

def select_action(observation):
    players = observation.data
    budget = observation.total_money
    return random_team(players, budget)

def main():
    main_funcs = {
        'engine_random': engine_random,
        'gym_random': gym_random,
    }
    if len(sys.argv) < 2 \
        or sys.argv[1] not in main_funcs \
        or len(sys.argv) == 3 and not re.match(r'\d{4}', sys.argv[2]):
        print('Usage: cartola_game.exec {} [ season_year ]'. format(' | '.join(main_funcs.keys())))
        return
    season = sys.argv[2] if len(sys.argv) == 3 else '2015'
    main_funcs[sys.argv[1]](season)

if __name__ == '__main__':
    main()
