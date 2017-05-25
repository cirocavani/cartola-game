# Cartola Notebooks

Development code in notebooks.

## Setup

```sh
# PWD cartola-game
conda create -y -p cartola-env python=3.5
cartola-env/bin/pip install -r notebooks/requirements.txt
cartola-env/bin/jupyter notebook --notebook-dir=notebooks
```

## Notebooks

[Game Models](Game Models.ipynb) (draft)

Game data modeling.

[Game Engine](Game Engine.ipynb) (draft)

Game engine mechanics.

[Game MILP](Game MILP.ipynb) (draft)

Mixed Integer Linear Programming with Piomo.

[Gym Random](Gym Random.ipynb) (example)

Random Strategy Agent running with Gym.

[Gym MILP](Gym MILP.ipynb) (example)

MILP Strategy Agent (last round best) running with Gym.

[Charts](Charts.ipynb)

Run plots (Money, Score by round).
