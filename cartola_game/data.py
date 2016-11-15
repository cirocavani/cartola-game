import csv
import json
import os

from .model import SeasonData, PlayerData, Player, Position, PlayerStatus

CARTOLA_DATA = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data')

def load_season(season_name, data_path=CARTOLA_DATA):
    season_path = os.path.join(data_path, season_name)
    game_file = os.path.join(season_path, 'game.json')
    players_file = os.path.join(season_path, 'players.csv')
    season_file = os.path.join(season_path, 'season.csv')

    if not os.path.isfile(game_file):
        raise Exception('file not found: ' + game_file)
    if not os.path.isfile(players_file):
        raise Exception('file not found: ' + players_file)
    if not os.path.isfile(season_file):
        raise Exception('file not found: ' + season_file)

    game_title, season_name, num_rounds = load_game(game_file)
    players = load_players(players_file)
    players_data = load_data(players, season_file, num_rounds)

    return SeasonData(season_name, num_rounds, players_data)

def load_game(game_file):
    with open(game_file) as f:
        g = json.load(f)
    return g['game_name'], g['game_season'], g['num_rounds']

def load_players(players_file):
    players = dict()
    with open(players_file, newline='') as f:
        reader = csv.reader(f)
        next(reader) # spkip header
        for row in reader:
            id, name, position_name = row
            try:
                position = Position(position_name)
            except ValueError:
                print('[{}] Invalid position: {}'.format(i, position_name))
                continue
            players[id] = Player(name, position)
    return players

def load_data(players, season_file, num_rounds):
    players_data = dict()

    with open(season_file, newline='') as f:
        reader = csv.reader(f)
        next(reader) # skip header
        for i, row in enumerate(reader):
            player_id = row[0]
            round_i = row[1]
            status_name = row[2]
            price = row[3]
            score = row[4]

            if player_id not in players:
                print('[{}] Player not found: {}'.format(i, player_id))
                continue
            try:
                round_i = int(round_i) - 1
            except ValueError:
                print('[{}] Invalid round: {}'.format(i, round_i))
                continue
            if round_i < 0 or round_i >= num_rounds:
                print('[{}] Round out of bounds: {} ({})'.format(i, round_i + 1, num_rounds))
                continue
            try:
                status = PlayerStatus(status_name)
            except ValueError:
                print('[{}] Invalid status: {}'.format(i, status_name))
                continue
            try:
                price = float(price)
            except ValueError:
                print('[{}] Invalid price: {}'.format(i, price))
                continue
            try:
                score = float(score)
            except ValueError:
                print('[{}] Invalid score: {}'.format(i, score))
                continue

            if player_id not in players_data:
                _player = players[player_id]
                _prices = [0.0] * num_rounds
                _scores = [0.0] * num_rounds
                _status = [PlayerStatus.UNKNOWN] * num_rounds
                players_data[player_id] = PlayerData(_player,
                                                     _prices,
                                                     _scores,
                                                     _status)

            player_data = players_data[player_id]
            player_data.prices[round_i] = price
            player_data.scores[round_i] = score
            player_data.status[round_i] = status

    return list(players_data.values())
