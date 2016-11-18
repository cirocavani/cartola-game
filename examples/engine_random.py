from cartola_game.data import load_season
from cartola_game.engine import GameEngine, GameInstance
from cartola_game.strategy import random_team

season_data = load_season('2015')

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
