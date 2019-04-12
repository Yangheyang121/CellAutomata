import random

from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from CellAutomaton import CellularAutomaton,generate_empty_2d_list_of_list
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
import kivy.uix.button as kb
from kivy.core.window import Window
kivy.require('1.9.0')


class CellAutomatonWidget(Widget):
    def __init__(self, ellipse_size, ellipse_offset, window_width=640, window_height=400, rule=90):
        super(CellAutomatonWidget, self).__init__()
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (window_width, window_height)

        self.automaton_mode = 2

        self.menu_item_width = 100
        self.menu_item_height = 50

        self.ellipse_offset = ellipse_offset
        self.ellipse_size = ellipse_size
        self.ellipse_box_size = self.ellipse_size + self.ellipse_offset

        self.current_canvas_graphic_items = []
        self.auto_iterations = None

        self.graphic_columns = int((Window.size[0] - self.menu_item_width) / self.ellipse_box_size)
        self.graphic_rows = int(Window.size[1]/self.ellipse_box_size)
        self.data_frame = generate_empty_2d_list_of_list(size=self.graphic_rows)

        self.cell_automaton = CellularAutomaton(
            mode=self.automaton_mode,
            size=self.graphic_rows,
            rule=rule,
            number_of_ones=int(self.graphic_rows*self.graphic_rows*0.3)
        )

        self.set_initial_display()

    def set_initial_display(self):
        self._draw_menu()

    def draw_graphics(self):
        self._draw_graphic_rows()

    def _draw_graphic_rows(self):
        for row in range(0, len(self.data_frame)):
            if row % 3 is 0:
                self.canvas.add(Color(0, 1, 0))
            if row % 3 is 1:
                self.canvas.add(Color(0, 0, 0))
            if row % 3 is 2:
                self.canvas.add(Color(1, 0, 0))

            self._draw_graphic_columns(row)

    def _draw_graphic_columns(self, row):
        for column in range(0, len(self.data_frame[row])):
            if self.data_frame[row][column] is 1:
                self._draw_graphic_cell(row, column)

    def _draw_graphic_cell(self, row, column):
        ellipse = Ellipse(
            pos=(
                self._get_graphic_cell_x_pos(column),
                self._get_graphic_cell_y_pos(row)
            ),
            size=(
                self.ellipse_size,
                self.ellipse_size
            )
        )
        self.canvas.add(ellipse)
        self.current_canvas_graphic_items.append(ellipse)

    def get_menu_item_pos_y(self, position):
        return Window.size[1]-(self.menu_item_height*position)

    def _get_graphic_cell_y_pos(self, row):
        return Window.size[1] - (row + 1) * self.ellipse_box_size

    def _get_graphic_cell_x_pos(self, column):
        return self.menu_item_width + column * self.ellipse_box_size

    def clear_graphic(self):
        for item in self.current_canvas_graphic_items:
            self.canvas.remove(item)
        self.current_canvas_graphic_items = []

    def create_graphics(self):
        self.clear_graphic()
        self.fetch_data_frame()
        self.draw_graphics()

    def _draw_graphic_controller(self, instance=None):
        self.auto_iterations.cancel()
        self.create_graphics()

    def _add_10_rule_and_draw_controller(self, instance):
        self.cell_automaton.set_rule((self.cell_automaton.rule+10) % 255)
        self.rule_label.text = "Rule: " + self.cell_automaton.rule.__str__()
        self.create_graphics()

    def _sub_10_rule_and_draw_controller(self, instance):
        self.cell_automaton.set_rule((self.cell_automaton.rule-10) % 255)
        self.rule_label.text = "Rule: " + self.cell_automaton.rule.__str__()
        self.create_graphics()

    def _draw_next_iteration_controller(self, instance):
        self.cell_automaton.calculate_next_iteration()
        self.cell_automaton.print_current_state()
        self.create_graphics()

    def _play_iterations_controller(self, instance):
        self.create_graphics()
        self.auto_iterations = Clock.schedule_interval(self._draw_next_iteration_controller, 0.5)

    def _stop_iterations_controller(self, instance):
        self.auto_iterations.cancel()

    def size_text_input_controller(self, instance, value):
        if value is not "":
            try:
                if int(value) > 1:
                    self.graphic_columns = int(value)
                    self.cell_automaton.size = int(value)
                    self.cell_automaton.set_initial_state()
                    self.size_label.text = "Size: " + self.graphic_columns.__str__()
            except ValueError:
                self.size_label.text = "Size:\nOnly positive\nintegers."

    def iterations_text_input_controller(self, instance, value):
        if value is not "":
            try:
                if int(value) > 1:
                    self.graphic_rows = int(value)
                    self.cell_automaton.set_initial_state()
                    self.iterations_label.text = "Iterations: " + self.graphic_rows.__str__()
            except ValueError:
                self.iterations_label.text = "Iterations:\nOnly positive\nintegers."

    def rule_text_input_controller(self, instance, value):
        if value is not "":
            try:
                if 1 < int(value) < 255:
                    self.cell_automaton.set_rule(int(value))
                    self.cell_automaton.set_initial_state()
                    self.rule_label.text = "Rule: " + self.cell_automaton.rule.__str__()
            except ValueError:
                self.rule_label.text = "Rule:\nOnly positive\nintegers."

    def _draw_menu(self):
        # todo refactor cuz ugly as hell
        draw_btn = kb.Button(
            text="Draw",
            pos=(0, self.get_menu_item_pos_y(2)),
            size=(self.menu_item_width, self.menu_item_height * 2)
        )
        draw_btn.bind(on_press=self._draw_graphic_controller)
        self.add_widget(draw_btn)

        rule_sub10_btn = kb.Button(
            text="Rule\n-10",
            pos=(0, self.get_menu_item_pos_y(4)),
            size=(int(self.menu_item_width / 2), self.menu_item_height * 2)
        )
        rule_sub10_btn.bind(on_press=self._sub_10_rule_and_draw_controller)
        self.add_widget(rule_sub10_btn)

        rule_plus10_btn = kb.Button(
            text="Rule\n+10",
            pos=(int(self.menu_item_width / 2), self.get_menu_item_pos_y(4)),
            size=(int(self.menu_item_width / 2), self.menu_item_height * 2)
        )
        rule_plus10_btn.bind(on_press=self._add_10_rule_and_draw_controller)
        self.add_widget(rule_plus10_btn)

        self.rule_label = Label(
            text="Rule: " + self.cell_automaton.rule.__str__(),
            pos=(0, self.get_menu_item_pos_y(5)),
            size=(self.menu_item_width, self.menu_item_height)
        )
        self.rule_label.color = [1, 0, 0, 1]
        self.add_widget(self.rule_label)

        rule_input = TextInput(
            pos=(0, self.get_menu_item_pos_y(6)),
            size=(self.menu_item_width, self.menu_item_height)
        )
        rule_input.bind(text=self.rule_text_input_controller)
        self.add_widget(rule_input)

        self.size_label = Label(
            text="Size: " + self.graphic_columns.__str__(),
            pos=(0, self.get_menu_item_pos_y(7)),
            size=(self.menu_item_width, self.menu_item_height)
        )
        self.size_label.color = [1, 0, 0, 1]
        self.add_widget(self.size_label)

        size_input = TextInput(
            pos=(0, self.get_menu_item_pos_y(8)),
            size=(self.menu_item_width, self.menu_item_height)
        )
        size_input.bind(text=self.size_text_input_controller)
        self.add_widget(size_input)

        self.iterations_label = Label(
            text="Iterations: " + self.graphic_rows.__str__(),
            pos=(0, self.get_menu_item_pos_y(9)),
            size=(self.menu_item_width, self.menu_item_height)
        )
        self.iterations_label.color = [1, 0, 0, 1]
        self.add_widget(self.iterations_label)

        iterations_input = TextInput(
            pos=(0, self.get_menu_item_pos_y(10)),
            size=(self.menu_item_width, self.menu_item_height)
        )
        iterations_input.bind(text=self.iterations_text_input_controller)
        self.add_widget(iterations_input)

        next_iteration_btn = kb.Button(
            text="Next\niteration",
            pos=(0, self.get_menu_item_pos_y(12)),
            size=(self.menu_item_width, self.menu_item_height * 2)
        )
        next_iteration_btn.bind(on_press=self._draw_next_iteration_controller)
        self.add_widget(next_iteration_btn)

        play_btn = kb.Button(
            text='Play',
            pos=(0, self.get_menu_item_pos_y(14)),
            size=(int(self.menu_item_width/2), self.menu_item_height * 2)
        )
        play_btn.bind(on_press=self._play_iterations_controller)
        self.add_widget(play_btn)

        stop_btn = kb.Button(
            text='Stop',
            pos=(int(self.menu_item_width/2), self.get_menu_item_pos_y(14)),
            size=(int(self.menu_item_width/2), self.menu_item_height * 2)
        )
        stop_btn.bind(on_press=self._stop_iterations_controller)
        self.add_widget(stop_btn)

    def _reset_data_frame(self):
        self.data_frame = generate_empty_2d_list_of_list(size=self.graphic_rows)

    def fetch_data_frame(self):
        if self.automaton_mode is CellularAutomaton.modes["1D"]:
            for iteration in range(0,self.graphic_rows):
                self.data_frame[iteration] = self.cell_automaton.get_current_state()
                self.cell_automaton.calculate_next_iteration()
            self.cell_automaton.set_initial_state()

        if self.automaton_mode is CellularAutomaton.modes["2D"]:
            self.data_frame=self.cell_automaton.get_current_state()
            self.cell_automaton.calculate_next_iteration()


class CellAutomatonApp(App):
    def build(self):
        return CellAutomatonWidget(4, 1, window_width=800, window_height=700)

