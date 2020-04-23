import tkinter as tk
from tkinter import font


class Application(tk.Frame):
    DEAD = "white"
    LIVE = "black"

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # Initialize UI settings
        self.grid(row=0, column=0)
        self.size_x = 20
        self.size_y = 20
        self.title_font = font.Font(family="Helvetica", size=14)

        # Initialize game state
        self.game_grid_cells = []
        self.intro_frame = None
        self.game_frame = None
        self.start_button = None
        self.reset_button = None
        self.is_running_simulation = False

        self.initialize_ui()

    def initialize_ui(self):
        self.master.title("Conway's Game of Life")

        # Setup introduction frame for instructions/start button
        self.intro_frame = tk.Frame(self.master)
        self.intro_frame.grid(row=0, column=0, columnspan=4)
        title = tk.Label(self.intro_frame, text="Conway's Game of Life", font=self.title_font)
        title.pack(side=tk.TOP)
        prompt = tk.Label(self.intro_frame, text="Click the cells to create the configuration, then press Start Game:")
        prompt.pack(side=tk.BOTTOM)

        # Setup buttons to kick off and reset the simulation
        self.start_button = tk.Button(self.master, text="Start Game", command=self.launch)
        self.start_button.grid(row=1, column=1, sticky=tk.E)
        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset)
        self.reset_button.grid(row=1, column=2, sticky=tk.W)

        # initialize the board grid
        self.create_game_grid()

    def create_game_grid(self):
        self.game_frame = tk.Frame(
            self.master,
            width=self.size_x + 2,
            height=self.size_y + 2,
            borderwidth=1,
            relief=tk.GROOVE
        )
        self.game_frame.grid(row=2, column=0, columnspan=4)
        self.game_grid_cells = [[tk.Button(self.game_frame, bg="white", width=2, height=1) for i in range(self.size_x + 2)] for j in range(self.size_y + 2)]
        # creates 2d array of buttons for grid
        for i in range(1, self.size_y + 1):
            for j in range(1, self.size_x + 1):
                self.game_grid_cells[i][j].grid(row=i, column=j, sticky=tk.W + tk.E)
                self.game_grid_cells[i][j]['command'] = lambda i=i, j=j: self.toggle_cell_state(i, j)

    def launch(self):
        # Setup
        print('LAUNCHING SIMULATION....')
        self.is_running_simulation = True
        print('Simulation running: ' + str(self.is_running_simulation))
        print('Disabling all cells...')
        self.disable_all_cells()
        print('All cells disabled.')

        # TODO: Game implementation

    def reset(self):
        print('RESET')
        if self.is_running_simulation:
            print('Stopping simulation.')
            self.is_running_simulation = False

        for row in self.game_grid_cells:
            for cell in row:
                if cell['bg'] == Application.LIVE:
                    cell['bg'] = Application.DEAD
        print('All cells reset to DEAD. Enabling all cells...')
        self.enable_all_cells()
        print('All cells enabled.')

    def toggle_cell_state(self, row, column):
        to_toggle = self.game_grid_cells[row][column]
        initial_state = to_toggle['bg']
        new_state = ""
        if initial_state == Application.DEAD:
            new_state = Application.LIVE
        elif initial_state == Application.LIVE:
            new_state = Application.DEAD

        to_toggle['bg'] = new_state
        print('grid_cell at ' + str(row) + " : " + str(column) + ' toggle ' + initial_state + '-->' + new_state)

    def disable_all_cells(self):
        for row in self.game_grid_cells:
            for cell in row:
                cell['state'] = tk.DISABLED

    def enable_all_cells(self):
        for row in self.game_grid_cells:
            for cell in row:
                cell['state'] = tk.NORMAL


def start_application():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    start_application()
