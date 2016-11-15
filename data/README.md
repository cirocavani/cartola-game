# Data Dictionary

`game.json`

(object)

* `game_name` (text)
* `game_season` (text)
* `num_rounds` (integer)

`players.csv`

1. `player_id` (primary key)
2. `player_name` (text)
3. `player_position` (categorical)

`season.csv`

1. `player_id` (foreign key)
2. `round` (integer)
3. `status` (categorical)
4. `price` (decimal)
5. `score` (decimal)

`player_position`

* `Goleiro` (*GOALKEEPER*)
* `Lateral` (*WINGER*)
* `Zagueiro`, (*DEFENDER*)
* `Meia` (*MIDFIELDER*)
* `Atacante` (*FORWARD*)
* `Técnico` (*COACH*)

`status`

* `Provável` (*POSSIBLE*)
* `Contundido` (*INJURED*)
* `Nulo` (*NULL*)
* `Dúvida` (*DOUBT*)
* `Suspenso` (*SUSPENDED*)
* `Desconhecido` (*UNKNOWN*)
