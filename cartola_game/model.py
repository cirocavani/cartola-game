from collections import defaultdict, namedtuple
from enum import Enum

class Player(namedtuple('Player', ['name', 'position'])):
    __slots__ = ()

    def __str__(self):
        return '{} ({})'.format(*self)

class Position(Enum):

    GOALKEEPER = 'Goleiro'
    WINGER = 'Lateral'
    DEFENDER = 'Zagueiro'
    MIDFIELDER = 'Meia'
    FORWARD = 'Atacante'
    COACH = 'Técnico'

    def __str__(self):
        return self.value

GOALKEEPER = Position.GOALKEEPER
WINGER = Position.WINGER
DEFENDER = Position.DEFENDER
MIDFIELDER = Position.MIDFIELDER
FORWARD = Position.FORWARD
COACH = Position.COACH

class PlayerStatus(Enum):

    POSSIBLE = 'Provável'
    INJURED = 'Contundido'
    NULL = 'Nulo'
    DOUBT = 'Dúvida'
    SUSPENDED = 'Suspenso'
    UNKNOWN = 'Desconhecido'

    def __str__(self):
        return self.value

PLAYER_POSSIBLE = PlayerStatus.POSSIBLE
PLAYER_INJURED = PlayerStatus.INJURED
PLAYER_NULL = PlayerStatus.NULL
PLAYER_DOUBT = PlayerStatus.DOUBT
PLAYER_SUSPENDED = PlayerStatus.SUSPENDED
PLAYER_UNKNOWN = PlayerStatus.UNKNOWN

class PlayerData:

    def __init__(self, player, prices, scores, status):
        self.player = player
        self.prices = prices
        self.scores = scores
        self.status = status

    def __str__(self):
        return str(self.player)

class SeasonData:

    def __init__(self, season_name, num_rounds, players):
        self.season_name = season_name
        self.num_rounds = num_rounds
        self.players = players

    def __str__(self):
        return '{} (rounds {}, players {})'.format(self.season_name,
                                                   self.num_rounds,
                                                   len(self.players))


PositionSlot = namedtuple('PositionSlot', ['position', 'size'])

def f(text, *p): return text, list(map(PositionSlot._make, p))

class Formation(Enum):

    F343 = f('3-4-3',
             (GOALKEEPER, 1),
             (DEFENDER, 3),
             (MIDFIELDER, 4),
             (FORWARD, 3),
             (COACH, 1))

    F352 = f('3-5-2',
             (GOALKEEPER, 1),
             (DEFENDER, 3),
             (MIDFIELDER, 5),
             (FORWARD, 2),
             (COACH, 1))

    F433 = f('4-3-3',
             (GOALKEEPER, 1),
             (WINGER, 2),
             (DEFENDER, 2),
             (MIDFIELDER, 3),
             (FORWARD, 3),
             (COACH, 1))

    F442 = f('4-4-2',
             (GOALKEEPER, 1),
             (WINGER, 2),
             (DEFENDER, 2),
             (MIDFIELDER, 4),
             (FORWARD, 2),
             (COACH, 1))

    F451 = f('4-5-1',
             (GOALKEEPER, 1),
             (WINGER, 2),
             (DEFENDER, 2),
             (MIDFIELDER, 5),
             (FORWARD, 1),
             (COACH, 1))

    F532 = f('5-3-2',
             (GOALKEEPER, 1),
             (WINGER, 2),
             (DEFENDER, 3),
             (MIDFIELDER, 3),
             (FORWARD, 2),
             (COACH, 1))

    F541 = f('5-4-1',
             (GOALKEEPER, 1),
             (WINGER, 2),
             (DEFENDER, 3),
             (MIDFIELDER, 3),
             (FORWARD, 2),
             (COACH, 1))

    @property
    def label(self):
        return self.value[0]

    @property
    def positions(self):
        return self.value[1]

    def __str__(self):
        positions = [str(p.position) for p in self.positions for _ in range(p.size)]
        return '{}\n\n{}'.format(self.label, '\n'.join(positions))

F343 = Formation.F343
F352 = Formation.F352
F433 = Formation.F433
F442 = Formation.F442
F451 = Formation.F451
F532 = Formation.F532
F541 = Formation.F541

def team_is_valid(formation, players, verbose=False):
    if not isinstance(players, set):
        players = set(players) # unique
    count = defaultdict(int)
    for player in players:
        count[player.position] += 1
    valid = True
    for position, size in formation.positions:
        if size != count[position]:
            valid = False
            if not verbose:
                break
            print('Missing {} (expected {}): {}' \
                  .format(position, size, count[position]))
    return valid

class Team:

    def __init__(self, formation, players, validate=True):
        if validate and not team_is_valid(formation, players):
            raise Exception('Team is invalid!')
        self.formation = formation
        self.players = set(players)

    def __str__(self):
        formation = self.formation.label
        players = defaultdict(list)
        for player in self.players:
            players[player.position].append(player.name)
        team = ('{} -> {}'.format(pos, name)
                for pos, _ in self.formation.positions
                for name in sorted(players[pos]))
        return '{}\n\n{}'.format(formation, '\n'.join(team))
