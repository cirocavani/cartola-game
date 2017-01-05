# Cartola Game

Cartola FC Environment for [OpenAI Gym](https://gym.openai.com/).

[Cartola FC](https://cartolafc.globo.com/) is a fantasy game based on Brazilian National Soccer Championship.

**Requirements**

* [Python 3](https://www.python.org/)
* [OpenAI Gym](https://gym.openai.com/)
* [Pyomo](http://www.pyomo.org/)
* [Coin-or Cbc](http://www.coin-or.org/projects/Cbc.xml)

**Setup**

```sh
pip install gym
pip install pyomo

git clone https://github.com/cirocavani/cartola-game.git
export PYTHONPATH=$(pwd)/cartola-game
```

Coin-or Cbc:

```
(Ubuntu / Debian)
sudo apt-get install coinor-cbc

(Arch Linux)
sudo pacman --sync coin-or-cbc

(macOS)
brew tap coin-or-tools/coinor
brew install cbc

Static:
http://ampl.com/products/solvers/open-source/#cbc
```


**Usage**

[ [Code](examples/gym_random.py) ] [ [Output](examples/gym_random_out.txt) ]

```python
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
```

Output:

```text
[ Round 1 ]

4-3-3

Goleiro -> Ederaldo Antônio de Oliveira
Lateral -> João Lucas Lima Silva
Lateral -> Luis Felipe Dias do Nascimento
Zagueiro -> Joemison Santos Barbosa
Zagueiro -> Rafael Thyere Albuquerque Marques
Meia -> Cleber Santana Loureiro
Meia -> Luiz Fernando Ferreira Maximiliano
Meia -> Thiago Henrique Mendes Ribeiro
Atacante -> Carlos Henrique Alves Pereira
Atacante -> Tauã Ferreira dos Santos
Atacante -> Vinícius Vasconcelos Araújo
Técnico -> Vanderlei Luxemburgo da Silva

Team Price: 46.76
Unused Money: 53.24

Score: 14.36

[ Round 2 ]

(...)

Total reward: 435.16
```
