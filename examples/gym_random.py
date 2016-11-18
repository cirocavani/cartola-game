import gym
from cartola_game.gym import gym_init
from cartola_game.strategy import random_team

gym_init()

env = gym.make('Cartola-v0')

# Load Season data
env.configure('2015')

total_reward = 0.0

# Initialize the Environment
observation = env.reset()

done = False
while not done:

    # Select a Team
    players = observation.data
    budget = observation.total_money
    action = random_team(players, budget)

    # Run one Round
    observation, reward, done, _ = env.step(action)
    total_reward += reward

    # Print stats from Last Round
    env.render()

print('...\n')
print('Total reward: {:.2f}'.format(total_reward))
