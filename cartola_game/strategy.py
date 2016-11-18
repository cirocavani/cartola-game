import math
import random

from pyomo.environ import *
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition

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

opt = SolverFactory('cbc')

def milp(players, opt_values, prices, budget, formation, show_model=False):
    model = ConcreteModel()

    model.PLAYERS = RangeSet(0,len(players)-1)
    model.x = Var(model.PLAYERS, within=Binary)

    model.objective = Objective(expr=sum(opt_values[i] * model.x[i] for i in model.PLAYERS), sense=maximize)

    model.budget = Constraint(expr=sum(prices[i] * model.x[i] for i in model.PLAYERS) <= math.floor(budget))

    N = 0
    for pos, n in formation.positions:
        players_position = [i for i, p in enumerate(players) if p.position == pos]
        model.add_component(pos.name, Constraint(expr=sum(model.x[i] for i in players_position) == n))
        N += n
    model.team_size = Constraint(expr=sum(model.x[i] for i in model.PLAYERS) == N)

    results = opt.solve(model)
    if results.solver.status != SolverStatus.ok \
        or results.solver.termination_condition != TerminationCondition.optimal:
        raise Exception('No optimal solution!\n\n' + str(results.solver))

    if show_model:
        model.display()

    opt_value = model.objective()

    selected_players = list()
    for i in model.x:
        if model.x[i].value:
            selected_players.append(players[i])

    return opt_value, Team(formation, selected_players)

def milp_team(players, opt_values, prices, budget, formation=None, verbose=False):
    if formation:
        return milp(players, opt_values, prices, budget, formation, verbose)

    team = None
    opt_value = None
    for f in Formation:
        try:
            _opt, _team = milp(players, opt_values, prices, budget, f)
            if not opt_value or _opt > opt_value:
                opt_value = _opt
                team = _team
        except Exception as err:
            if verbose:
                print(err)

    if verbose:
        print('opt_value: {:.2f}'.format(opt_value))

    return team
