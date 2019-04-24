from functools import partial

from kivy.core.window import Window
from kivy.uix.label import Label

from controler.GameOfLifeController import GameOfLifeController
from controler.MainController import BaseController
from model.CellAutomata.CellAutomaton1D import CellAutomaton1D
from model.RuleSets.BinaryRuleSet import BinaryRuleSet
from view.BaseView import BaseView
from view.BinaryRuleSetView import BinaryRuleSetView
from view.DrawingView import DrawingView


def generate_empty_2d_list_of_list(size):
    return [[] for i in range(0, size)]


class BinaryRuleSetController(BaseController):
    modes = {
        "Game of Life": GameOfLifeController,
    }
    rule_set = BinaryRuleSet

    def __init__(self, app, cell_size=9, cell_offset=1, rule=90):
        self.cell_size = cell_size
        self.cell_offset = cell_offset
        self.cell_box_size = cell_size + cell_offset
        super().__init__(app)
        self.update_labels()

    def set_initial_view(self):
        self.set_view(BinaryRuleSetView(self.modes, self.get_menu_width()))

    def bind_buttons(self):
        super().bind_buttons()
        self.bind_columns_buttons()
        self.bind_draw_button()
        self.bind_columns_buttons()
        self.bind_iterations_buttons()
        self.bind_rule_buttons()
        self.bind_alive_cells_buttons()

    def setup(self):
        self.max_graphic_columns = self.get_view_max_columns()
        self.max_graphic_rows = self.get_view_max_rows()
        self.iteration_speed = 8

        self.data_frame = generate_empty_2d_list_of_list(size=self.max_graphic_rows)

        self.iterations = self.get_view_max_rows()
        self.cell_automaton = None
        self.set_cell_automaton()

    def set_cell_automaton(self, columns=None, rule_set=None, p_of_alive=None):
        if self.cell_automaton is None:
            self.set_cell_automaton_to_starting_state()
        else:
            if columns is None:
                columns = self.cell_automaton.get_columns()
            if rule_set is None:
                rule_set = self.cell_automaton.get_rule_set()
            if p_of_alive is None:
                p_of_alive = self.cell_automaton.get_percent_of_alive_cells()

            self.cell_automaton = CellAutomaton1D(
                columns=columns,
                rule_set=rule_set,
                percent_of_alive_cells=p_of_alive
            )

    def get_view_max_columns(self):
        return int((Window.size[0] - self.menu_item_width) / self.cell_box_size)

    def get_view_max_rows(self):
        return int(Window.size[1] / self.cell_box_size)

    def get_columns(self):
        return self.cell_automaton.get_columns()

    def get_iterations(self):
        return self.iterations

    def add__columns_controller(self, btn_instance):
        self.cell_automaton.change_columns(self.cell_automaton.get_columns() + 10)
        self.update_columns_label()
        self.reset_canvas()


    def reset_canvas(self):
        pass

    def bind_draw_button(self):
        self.app.view.draw_btn.bind(on_press=partial(self.draw_graphic))

    def bind_columns_buttons(self):
        self.app.view.add_columns.bind(on_press=partial(self.add_columns_controller))
        self.app.view.sub_columns.bind(on_press=partial(self.sub_columns_controller))

    def bind_iterations_buttons(self):
        self.app.view.sub_iterations.bind(on_press=partial(self.sub_iterations_controller))
        self.app.view.add_iterations.bind(on_press=partial(self.add_iterations_controller))

    def bind_rule_buttons(self):
        self.app.view.add_rule.bind(on_press=partial(self.add_rule_controller))
        self.app.view.sub_rule.bind(on_press=partial(self.sub_rule_controller))

    def bind_alive_cells_buttons(self):
        self.app.view.sub_alive_cells.bind(on_press=partial(self.sub_alive_cells_controller))
        self.app.view.add_alive_cells.bind(on_press=partial(self.add_alive_cells_controller))

    def draw_graphic(self, button_instance):
        self.clear_canvas()
        self.fetch_data_frame()
        self.app.view.draw_data_frame(self.data_frame)
        # self.cell_automaton.print_iterations(self.iterations)

    def sub_columns_controller(self, button_instance):
        delta = -10
        current_value = self.cell_automaton.get_columns()
        if self.cell_automaton.get_columns() + delta > 0:
            self.cell_automaton.change_columns(current_value + delta)
            self.update_columns_label()

    def add_columns_controller(self, button_instance):
        delta = 10
        current_value = self.cell_automaton.get_columns()
        if current_value + delta > 0:
            self.cell_automaton.change_columns(current_value + delta)
            self.update_columns_label()

    def sub_iterations_controller(self, button_instance):
        delta = -10
        current_value = self.iterations
        if current_value + delta > 0:
            self.iterations = current_value + delta
            self.data_frame = generate_empty_2d_list_of_list(size=self.iterations)
            self.update_iterations_label()

    def add_iterations_controller(self, button_instance):
        delta = 10
        current_value = self.iterations
        if current_value + delta > 0:
            self.iterations = current_value + delta
            self.data_frame = generate_empty_2d_list_of_list(size=self.iterations)
            self.update_iterations_label()

    def sub_rule_controller(self, button_instance):
        delta = -5
        current_value = self.cell_automaton.get_rule_set().get_rule_base_10()
        self.set_cell_automaton(rule_set=BinaryRuleSet((current_value + delta) % 255))
        self.update_rule_label()

    def add_rule_controller(self, button_instance):
        delta = 5
        current_value = self.cell_automaton.get_rule_set().get_rule_base_10()
        self.set_cell_automaton(rule_set=BinaryRuleSet((current_value + delta) % 255))
        self.update_rule_label()

    def sub_alive_cells_controller(self, button_instance):
        delta = -0.05
        current_value = self.cell_automaton.get_percent_of_alive_cells()
        if current_value + delta > 0:
            self.cell_automaton.change_alive_cells_percentage(current_value + delta)
            self.update_alive_cells_label()

    def add_alive_cells_controller(self, button_instance):
        delta = 0.05
        current_value = self.cell_automaton.get_percent_of_alive_cells()
        if current_value + delta > 0:
            self.cell_automaton.change_alive_cells_percentage(current_value + delta)
            self.update_alive_cells_label()

    def fetch_data_frame(self):
        for iteration in range(0, self.iterations):
            self.data_frame[iteration] = self.cell_automaton.get_current_state()
            self.cell_automaton.calculate_next_iteration()
        self.cell_automaton.set_to_initial_state()


    def set_cell_automaton_to_starting_state(self):
        self.cell_automaton = CellAutomaton1D(
            columns=self.get_view_max_columns(),
            rule_set=self.rule_set(90),
            percent_of_alive_cells=0.2
        )

    def update_labels(self):
        self.update_columns_label()
        self.update_iterations_label()
        self.update_rule_label()
        self.update_alive_cells_label()

    def update_columns_label(self):
        self.app.view.columns_label.text = "Columns" + self.cell_automaton.get_columns().__str__()

    def update_rule_label(self):
        self.app.view.rule_label.text = self.cell_automaton.get_rule_set().__str__()

    def update_iterations_label(self):
        self.app.view.iterations_label.text = "Iterations: " + self.iterations.__str__()

    def update_alive_cells_label(self):
        self.app.view.alive_cells_label.text = "Alive cells:\n"+"{:.1f}%".format(self.cell_automaton.get_percent_of_alive_cells()*100)



