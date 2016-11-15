import random

from .model import Team, Formation

def filter_players(players, position, max_price):
    return [p for p in players if p.player.position == position and p.price < max_price]

def sample_players(players, formation, budget):
    selected_players = []
    for pos, n in formation.positions:
        candidates = filter_players(players, pos, budget)
        if len(candidates) < n:
            return None
        for player in random.sample(candidates, n):
            budget -= player.price
            if budget < 0.0:
                return None
            selected_players.append(player.player)
    return selected_players

def random_team(data, budget, max_iterations=1000000):
    players_list = list(data.players_data.values())
    for _ in range(max_iterations):
        formation = random.choice(list(Formation))
        players = sample_players(players_list, formation, budget)
        if not players:
            continue
        return Team(formation, players)
    return None
