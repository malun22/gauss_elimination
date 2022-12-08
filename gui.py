import PySimpleGUI as sg
from gauss_elimination import GaussElimination
import time

# Events
# - Number of unknowns changed
# - Increase number of rows
# - Decrease number of rows
# - Submit for calculation
# - Quit the window


class GUI:
    title = "Gauss Elimination"
    MAX_UNKNOWNS = 10
    MAX_ROWS = 10

    current_matrix = [[3, 0, 1], [1, 2, 0], [0, 1, 1]]
    current_matrix = [[-3, -33, -1], [0, 0, 2], [-2, 0, -2]]
    current_solutions = [5] * len(current_matrix)
    current_solutions = [-38, -11, -3]

    current_rows = len(current_matrix)

    def __init__(self) -> None:
        self.layout = [
            [sg.Text("Welcome to the Gauss Elimination program!",
                     size=(80, 2), justification='center', )],
            [sg.Text("Please enter the number of unknowns: "),
             sg.Input(len(self.current_matrix[0]), size=(5, 1), key='-UNKNOWNSINPUT-', justification="r"), sg.Button("Ok", key="-UNKNOWNSOK-")],
            [sg.Text("", text_color='red', key='-UNKNOWNSERROR-')],
        ]

        for row in range(self.MAX_ROWS):
            row_elements = []
            for col in range(self.MAX_UNKNOWNS):
                row_elements.append(sg.Input(self.current_matrix[row][col] if row < len(self.current_matrix) and col < len(
                    self.current_matrix[0]) else "0", size=(4, 1), justification="r", visible=(
                    row < len(self.current_matrix) and col < len(self.current_matrix[0])), key=f"-matrix_{row}_{col}-"))

            row_elements.append(sg.Input(self.current_solutions[row] if row < len(self.current_solutions) else "0", justification="r", size=(4, 1),
                                         key=f"-solution_{row}-", background_color="yellow", visible=(row < len(self.current_matrix))))

            self.layout.append(row_elements)

        self.layout += [
            [sg.Text("", text_color='red', key='-CHANGEERROR-')],
            [sg.Text("", key='-SOLUTION-')],
            [sg.Button('Submit')],
            [sg.Button('Quit')]
        ]

        self.window = sg.Window(self.title, self.layout)

    def update_matrix(self):
        for row in range(self.MAX_ROWS):
            self.window[f"-solution_{row}-"].update(visible=False)

            for col in range(self.MAX_UNKNOWNS):
                self.window[f"-matrix_{row}_{col}-"].update(self.current_matrix[row][col] if row < len(self.current_matrix) and col < len(self.current_matrix[0]) else "0", visible=(
                    row < len(self.current_matrix) and col < len(self.current_matrix[0])))

            self.window[f"-solution_{row}-"].update(
                self.current_solutions[row] if row < len(self.current_solutions) else "0", visible=(row < len(self.current_matrix)))

    def run(self):
        while True:
            event, values = self.window.read()
            # See if user wants to quit or window was closed
            if event == sg.WINDOW_CLOSED or event == 'Quit':
                break

            self.window["-CHANGEERROR-"].update(visible=False)
            self.window["-SOLUTION-"].update("")

            if event == "Submit":
                # Transfer Data to algorithm
                self.save_data()

                st = time.time()

                GE = GaussElimination(
                    default_matrix=self.current_matrix, right_side=self.current_solutions)

                solution = GE.solve()

                exec_time = time.time() - st

                sol_text = f"The solution (obtained in {round(exec_time, 2)} seconds) is: "

                for i, s in enumerate(solution):
                    sol_text += f"x{i + 1} = {round(s, 3)} "

                self.window["-SOLUTION-"].update(sol_text)

            if event == '-ADDROW-':
                if self.current_rows >= self.MAX_ROWS:
                    self.window["-CHANGEERROR-"].update(visible=True)
                    self.window['-CHANGEERROR-'].update(
                        f"You can't add more rows than {self.MAX_ROWS}!")
                    continue
                self.change_row(1)
                self.update_matrix()
                continue
            if event == '-REMOVEROW-':

                if self.current_rows <= 1:
                    self.window["-CHANGEERROR-"].update(visible=True)
                    self.window['-CHANGEERROR-'].update(
                        "You can't remove any more rows!")
                    continue
                if self.current_rows == len(self.current_matrix[0]):
                    self.window["-CHANGEERROR-"].update(visible=True)
                    self.window['-CHANGEERROR-'].update(
                        "You can't have less rows than unknowns!")
                    continue
                self.change_row(-1)
                self.update_matrix()
                continue
            if event == "-UNKNOWNSOK-":
                unknowns = int(values["-UNKNOWNSINPUT-"])

                if unknowns == len(self.current_matrix[0]):
                    continue

                self.window["-UNKNOWNSERROR-"].update(visible=False)

                if unknowns <= 1:
                    self.window["-UNKNOWNSERROR-"].update(visible=True)
                    self.window["-UNKNOWNSERROR-"].update(
                        "Please select a number greater than 1.")
                    continue

                if unknowns > self.MAX_UNKNOWNS:
                    self.window["-UNKNOWNSERROR-"].update(visible=True)
                    self.window["-UNKNOWNSERROR-"].update(
                        f"We currently only support {self.MAX_UNKNOWNS} unknowns.")
                    continue

                if unknowns != len(self.current_matrix[0]):
                    self.change_column(unknowns - len(self.current_matrix[0]))
                    self.change_row(unknowns - len(self.current_matrix))

                self.update_matrix()

        # Finish up by removing from the screen
        self.window.close()

    def change_column(self, change):
        if change > 0:
            for row in self.current_matrix:
                row.extend([0] * change)
        else:
            for row in self.current_matrix:
                for i in range(abs(change)):
                    row.pop(len(row) - 1)

        self.save_data()

    def save_data(self):
        rows = len(self.current_matrix)
        columns = len(self.current_matrix[0])
        self.current_matrix = []
        self.current_solutions = []

        for row in range(rows):
            row_entries = []
            for col in range(columns):
                row_entries.append(self.window[f"-matrix_{row}_{col}-"].get())

            self.current_matrix.append(row_entries)

            self.current_solutions.append(
                self.window[f"-solution_{row}-"].get())

    def change_row(self, number: int):
        self.current_rows += number
        if number > 0:
            for i in range(number):
                self.current_matrix += [[0] * len(self.current_matrix[0])]
        else:
            for i in range(abs(number)):
                self.current_matrix.pop(len(self.current_matrix) - 1)

        self.save_data()
