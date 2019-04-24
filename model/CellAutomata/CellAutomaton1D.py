import random

from model.Cells.CellFactory import CellFactory
from model.Cells.CellFactory import CellFactory
from model.RuleSets.RuleSet import RuleSet


class CellAutomaton1D:

    def __init__(self, rule_set, columns, percent_of_alive_cells=None, initial_state=None):
        self._set_rule_set(rule_set)
        self.cell_factory = CellFactory(rule_set.get_cell_type())
        self.columns = None
        self._set_columns(columns)
        
        self.percentage_of_alive_cells = None
        self.set_percent_of_alive_cells(percent_of_alive_cells)
        
        self.initial_state = initial_state
        self.previous_state = None
        self.current_state = None
        
        if initial_state is None:
            self._create_random_initial_state()
        self.set_to_initial_state()

    def calculate_next_iteration(self):
        self.previous_state = self.current_state
        self._reset_current_state()
        self._set_cells()

    def _set_cells(self):
        for cell_index in range(0, self.columns):
            self._append_cell(cell_index)

    def _set_rule_set(self, rule_set):
        if not isinstance(rule_set, RuleSet):
            raise TypeError
        self.rule_set = rule_set

    def _create_random_initial_state(self):
        self._prepare_initial_dead_cells()
        self._prepare_initial_alive_cells()

    def _prepare_initial_alive_cells(self):
        self._set_number_of_alive_cells()
        for i in range(0, self._number_of_alive_cells):
            while True:
                y = random.randrange(0, self.columns)
                if self.initial_state[y].is_dead():
                    self.initial_state[y] = self.cell_factory.create_random_alive_cell()
                    break

    def _prepare_initial_dead_cells(self):
        self.initial_state = [self.cell_factory.create_dead_cell()] * self.columns

    def _reset_current_state(self):
        self.current_state = self.create_empty_state()

    def create_empty_state(self):
        return []

    def set_to_initial_state(self):
        self.current_state = self.initial_state

    def get_current_state(self):
        return self.current_state

    def get_previous_state(self):
        return self.previous_state

    def print_current_state(self):
            print([cell.get_value() for cell in self.current_state])

    def reset_to_random_state(self):
        self._create_random_initial_state()
        self.set_to_initial_state()

    def print_iterations(self, iterations):
        print(iterations)
        print("Iteration: 0")
        self.print_current_state()
        for i in range(1, iterations):
            print("Iteration: " + i.__str__())
            self.calculate_next_iteration()
            self.print_current_state()

    def iterations_to_list(self, iterations):
        list = generate_empty_2d_list_of_list(iterations)
        list[0] = self.current_state
        for i in range(1, iterations):
            self.calculate_next_iteration()
            list[i] = self.current_state
        return list

    def __str__(self):
        return "Rule Set: " + self.rule_set.__str__() + "Columns: " + self.columns.__str__()

    def print_stats(self):
        print("Rule Set: ", self.rule_set.__str__())
        print("Columns: ", self.columns.__str__())

    def _set_number_of_alive_cells(self):
        self._number_of_alive_cells = int(self.cell_count() * self.percentage_of_alive_cells)

    def set_percent_of_alive_cells(self, percent):
        if percent is None or percent < 0:
            self.percentage_of_alive_cells = 0
        else:
            self.percentage_of_alive_cells = percent
        self._set_number_of_alive_cells()

    def _set_columns(self, columns):
        if columns < 0:
            raise ValueError
        self.columns = columns

    def get_columns(self):
        return self.columns

    def cell_count(self):
        return self.columns

    # todo change so that it fits old data not creates new
    def _fit_to_size(self):
        self._create_random_initial_state()

    def _append_cell(self, cell_index):
        self.current_state.append(self.rule_set.apply(self.previous_state, cell_index))

    def change_columns(self, columns):
        self._set_columns(columns)
        self._fit_to_size()
        self.set_to_initial_state()

    def get_rule_set(self):
        return self.rule_set

    def change_alive_cells_percentage(self, percentage_of_alive_cells):
        self.set_percent_of_alive_cells(round(percentage_of_alive_cells, 2))
        self._set_number_of_alive_cells()
        self.reset_to_random_state()

    def get_percent_of_alive_cells(self):
        return self.percentage_of_alive_cells
