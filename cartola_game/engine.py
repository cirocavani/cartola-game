from collections import namedtuple

PlayerState = namedtuple('PlayerState', ['player', 'status', 'price', 'price_var', 'score'])

class RoundEngine:

    def __init__(self, round_number, players_data):
        self.round_number = round_number
        self.players_data = players_data

    def price(self, players):
        return sum(self.players_data[p].price for p in players)

class ScoreEngine:

    def __init__(self, players_score):
        self.players_score = players_score

    def score(self, players):
        return sum(self.players_score[p] for p in players)

class GameEngine:

    def __init__(self, season_data):
        rounds = []
        scores = []

        for i in range(season_data.num_rounds):
            round_players = {}
            score_players = {}
            for player_data in season_data.players:
                p = player_data.player
                round_players[p] = self._round_player(player_data, i)
                score_players[p] = self._score_player(player_data, i)
            rounds.append(RoundEngine(i + 1, round_players))
            scores.append(ScoreEngine(score_players))

        self.rounds = rounds
        self.scores = scores

    def _round_player(self, player_data, i):
        player = player_data.player
        status = player_data.status[i]
        price = player_data.prices[i]
        price_var = 0.0 if i == 0 else price - player_data.prices[i - 1]
        score = 0.0 if i == 0 else player_data.scores[i - i]
        return PlayerState(player, status, price, price_var, score)

    def _score_player(self, player_data, i):
        return player_data.scores[i]

    @property
    def num_rounds(self):
        return len(self.rounds)

    def round_engine(self, round_number):
        return self.rounds[round_number - 1]

    def score_engine(self, round_number):
        return self.scores[round_number - 1]

class GameState(namedtuple('GameState', ['round_number', 'team', 'team_price', 'team_score', 'money'])):
    __slots__ = ()

    def __str__(self):
        out = '[ Round {} ]\n\n'.format(self.round_number)
        out += str(self.team)
        out += '\n\nTeam Price: {:.2f}\n'.format(self.team_price)
        out += 'Unused Money: {:.2f}\n\n'.format(self.money)
        out += 'Score: {:.2f}'.format(self.team_score)
        return out

class GameInstance:

    def __init__(self, engine, initial_money=100.0):
        self.engine = engine
        self.initial_money = initial_money
        self.states = []

    @property
    def done(self):
        return len(self.states) == self.engine.num_rounds

    @property
    def round_number(self):
        return len(self.states) + 1

    @property
    def data(self):
        return self.engine.round_engine(self.round_number - int(self.done))

    @property
    def total_money(self):
        if self.round_number == 1:
            return self.initial_money
        s = self.states[-1]
        return s.money + self.data.price(s.team.players)

    def run(self, team):
        if self.done:
            raise Exception('Game is done!')

        running_round = self.round_number

        budget = self.total_money
        team_price = self.data.price(team.players)
        free_money = budget - team_price
        if free_money < 0.0:
            raise Exception('Invalid team: insufficient budget!')

        team_score = self.engine.score_engine(running_round).score(team.players)

        s = GameState(running_round, team, team_price, team_score, free_money)
        self.states.append(s)

        return team_score
