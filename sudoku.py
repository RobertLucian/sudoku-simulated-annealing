import json
import random
import math
import copy
import click

def read_sudoku(file):
    """
    Read from a file the sudoku board.

    :param file: The JSON file containing the sudoku board.
    :return: The sudoku board.
    """
    with open(file, 'r') as f:
        data = json.load(f)
    return data

def show_sudoku(sudoku, sasudoku=False):
    """
    Display the sudoku board as stdout.

    :param sudoku: The sudoku board.
    :param sasudoku: True if the sudoku param is a SASudoku.state object.
    False if it's just the object returned by read_sudoku function.
    :return: Nothing.
    """
    if sasudoku:
        sudoku = sudoku.state

    for row, x in zip(sudoku, range(9)):

        if x % 3 == 0 and x > 0 and x < 9:
            click.echo(21 * "-")

        string = ""
        for cell, y in zip(row, range(9)):
            if y % 3 == 0 and y > 0 and y < 9:
                string += "| "
            if cell == "":
                string += "x "
            else:
                if sasudoku:
                    cell = cell.value
                string += str(cell) + " "
        click.echo(string)

class Cell:
    def __init__(self, value, variable=False):
        """
        Initialize a cell.

        :param value: The value of the cell.
        :param variable: Whether the cell's value has to be determined or not.
        """
        self.value = value
        self.variable = variable

class SASudoku:
    def __init__(self, sudoku=None):
        """
        Initialize the sudoku by creating a 9x9 grid of cells.

        :param sudoku: The board's state. None if it's set later on.
        :param max_temp: Simulated Annealing's starting temperature.
        :param cooldown_rate: Simulated Annealing's cooldown rate.
        """

        if sudoku:
            # initialize the board
            self.state = []
            used_numbers = []
            for row in sudoku:
                self.state.append([])
                last = len(self.state) - 1
                for cell in row:
                    variable = True if cell == "" else False
                    self.state[last].append(
                        Cell(value=cell, variable=variable)
                    )
                    if not variable:
                        used_numbers.append(cell)

            # generate the remaining numbers for the current board
            available_numbers = []
            for num in range(1, 10):
                occurrences = used_numbers.count(num)
                available_slots = 9 - occurrences
                if available_slots > 0:
                    available_numbers += available_slots * [num]
            random.shuffle(available_numbers)

            # assign the remaining numbers to each variable on the board
            num = iter(available_numbers)
            for y, row in enumerate(self.state):
                for x, cell in enumerate(row):
                    if cell.variable:
                        self.state[y][x].value = next(num)
        else:
            self.state = None

    def determine_energy(self):
        """
        Calculate the energy (score) of a given configuration of the sudoku board. 0 for best or 1 for worst.
        """
        energy = 243
        state = self.state

        # factor in the unique elements on all rows
        for row in state:
            row = map(lambda cell: cell.value, row)
            unique = len(set(row))
            energy -= unique

        # factor in the unique elements on each column
        for col in zip(*state):
            col = map(lambda cell: cell.value, col)
            unique = len(set(col))
            energy -= unique

        # factor in the unique elements in each box
        for y in range(3):
            for x in range(3):
                box_set = set([])
                for cy in range(3):
                    for cx in range(3):
                        cell = state[3 * y + cy][3 * x + cx]
                        box_set.add(cell.value)
                unique = len(box_set)
                energy -= unique

        # scale to 0-1
        energy /= 243.0

        return energy

    def get_neighbour(self):
        """
        Generate a neighbour based on this instance's state.
        """
        # select 2 random cells
        while True:
            y1 = random.randint(0, 8)
            x1 = random.randint(0, 8)
            if self.state[y1][x1].variable:
                cell1 = self.state[y1][x1].value
                break

        while True:
            y2 = random.randint(0, 8)
            x2 = random.randint(0, 8)
            if self.state[y2][x2].variable and x2 != x1 and y2 != x1:
                cell2 = self.state[y2][x2].value
                break

        # create the new neighbour board
        new_board = copy.deepcopy(self.state)
        new_board[y1][x1].value = cell2
        new_board[y2][x2].value = cell1

        return new_board

def acceptance_probability(energy, new_energy, temperature):
    if new_energy < energy:
        return 1.0
    else:
        return math.exp((energy - new_energy) / temperature)

@click.command()
@click.option('--initial-temp', type=click.FLOAT, default=5.0e-2, show_default=True)
@click.option('--stop-temp', type=click.FLOAT, default=1.0e-5, show_default=True)
@click.option('--cooldown-rate', type=click.FLOAT, default=0.5e-5, show_default=True)
@click.argument('filename')
def main(initial_temp, stop_temp, cooldown_rate, filename):
    # read the sudoku board and display it
    state = read_sudoku(filename)
    show_sudoku(state)

    # create a sudoku board object
    sudoku = SASudoku(state)
    best = sudoku

    # premise
    random.seed()
    temperature = initial_temp
    low_temp_limit = stop_temp
    counter = 0

    # run the simulated annealing algorithm until it converges
    while temperature > low_temp_limit:

        # generate neighbour
        neighbour_state = sudoku.get_neighbour()
        neighbour = SASudoku()
        neighbour.state = neighbour_state

        # determine the current and neighbour's energy levels
        energy_old = sudoku.determine_energy()
        energy_new = neighbour.determine_energy()

        # accept the neighbour if it passes the probability function
        random_val = random.uniform(0, 1)
        if acceptance_probability(energy_old, energy_new, temperature) > random_val:
            sudoku = neighbour

        # check if we've set a new record
        if best.determine_energy() > sudoku.determine_energy():
            best = sudoku

        # print the new findings
        best_energy = best.determine_energy()
        current_energy = sudoku.determine_energy()
        if counter % 100 == 0:
            click.echo(f"Best energy: {int(best_energy * 243)}/243 | Current Energy: {int(current_energy * 243)}/243 | Temperature: {temperature}")
        # and stop it if a solution has been found
        if best_energy == 0.0:
            break

        # otherwise keep on lowering the temperature
        temperature *= (1 - cooldown_rate)
        counter += 1

    click.echo("Reached end of simulated annealing")
    if best_energy == 0.0:
        show_sudoku(best, sasudoku=True)
    else:
        click.echo("Haven't found a solution to the sudoku problem")

if __name__ == "__main__":
    main()