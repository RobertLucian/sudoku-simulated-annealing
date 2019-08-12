# sudoku-simulated-annealing

## Intro

This is a sudoku solver implemented using the simulated annealing algorithm. 
It is far from being a fast algorithm, but can instead be used as a learning tool
to show others what can be done with it. 

## Installing

This can be installed with pip by running it this way:
```bash
pip install github.com/RobertLucian/sudoku-simulated-annealing@v0.1.0
```
Or if you want to install it in editable mode, then clone the repo, 
navigate to its root directory and run these:
```bash
virtualenv -p python .venv
source .venv/bin/activate
pip install --editable .
```

## Running It

Once the package is installed, you can run its `sasudoku` CLI tool:
```bash
(.venv) (base) Roberts-MacBook-2:sudoku-simulated-annealing robert$ sasudoku --help
Usage: sasudoku [OPTIONS] FILENAME

Options:
  --initial-temp FLOAT   Initial temperature of the simulated annealing
                         algorithm  [default: 0.05]
  --stop-temp FLOAT      The temperature at which the algorithm hard stops
                         [default: 1e-05]
  --cooldown-rate FLOAT  The rate at which the temperature drops  [default:
                         5e-06]
  --help                 Show this message and exit.
```
The default values for each option seem to be enough for the sudoku to converge to a solution,
albeit in quite a long time - think minutes.

The file that has to be provided to the CLI tool is a JSON file containing the 
state of the sudoku problem. This is one such example (the empty strings represent
the missing values that have to be completed):
```json
[
  [5, 3, "", "", 7, "", "", "", ""],
  [6, "", "", 1, 9, 5, "", "", ""],
  ["", 9, 8, "", "", "", "", 6, ""],
  [8, "", "", "", 6, "", "", "", 3],
  [4, "", "", 8, "", 3, "", "", 1],
  [7, "", "", "", 2, "", "", "", 6],
  ["", 6, "", "", "", "", 2, 8, ""],
  ["", "", "", 4, 1, 9, "", "", 5],
  ["", "", "", "", 8, "", "", 7, 9]
]
```

If the repo is cloned you can also run the above example by running the CLI tool this way:
```bash
sasudoku test/sudoku.json
```