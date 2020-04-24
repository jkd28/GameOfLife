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
        self.tick_delay_ms = 500
        self.max_ticks = 10
        self.num_ticks = 0

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
        self.disable_all_cells()
        # Run simulation if not already run
        if self.num_ticks < self.max_ticks:
            self.tick()
        else:
            print('Simulation already ran. Aborted launch.')

    def tick(self):
        print('Ticking: tick {}'.format(self.num_ticks))
        self.num_ticks += 1
        for current_row_index, row in enumerate(self.game_grid_cells):
            for current_column_index, cell in enumerate(row):
                live_neighbors = self.get_live_neighbors(current_row_index, current_column_index)
                if self.cell_is_live(current_row_index, current_column_index):
                    # print('Live cell at ({0},{1})'.format(current_column_index,current_row_index))
                    if live_neighbors < 2 or live_neighbors > 3:
                        self.kill_cell(current_row_index, current_column_index)
                else:
                    # print('Dead cell at ({0},{1})'.format(current_column_index,current_row_index))
                    if live_neighbors == 3:
                        self.revive_cell(current_row_index,current_column_index)
        if self.num_ticks <= self.max_ticks:
            self.master.after(self.tick_delay_ms, self.tick)

    def get_live_neighbors(self, row, column):
        # Calculate surrounding indices, including wrap-around
        up_row_index = row - 1
        if up_row_index < 1:
            up_row_index = self.size_y

        left_column_index = column - 1
        if left_column_index < 0:
            left_column_index = self.size_x

        down_row_index = row + 1
        if down_row_index > self.size_y:
            down_row_index = 0

        right_column_index = column + 1
        if right_column_index > self.size_x:
            right_column_index = 0

        # Get cells in neighboring locations
        neighbors = [
            self.game_grid_cells[up_row_index][left_column_index],
            self.game_grid_cells[up_row_index][column],
            self.game_grid_cells[up_row_index][right_column_index],
            self.game_grid_cells[row][left_column_index],
            self.game_grid_cells[row][right_column_index],
            self.game_grid_cells[down_row_index][left_column_index],
            self.game_grid_cells[down_row_index][column],
            self.game_grid_cells[down_row_index][right_column_index]
        ]
        live_count = 0
        for neighbor in neighbors:
            if neighbor['bg'] == Application.LIVE:
                live_count += 1
        return live_count

    def reset(self):
        print('RESET')
        self.num_ticks = 0

        if self.is_running_simulation:
            print('Stopping simulation.')
            self.is_running_simulation = False

        for row in self.game_grid_cells:
            for cell in row:
                if cell['bg'] == Application.LIVE:
                    cell['bg'] = Application.DEAD
        print('All cells reset to DEAD.')
        self.enable_all_cells()
        return

    def toggle_cell_state(self, row, column):
        to_toggle = self.game_grid_cells[row][column]
        initial_state = to_toggle['bg']
        new_state = ""
        if initial_state == Application.DEAD:
            new_state = Application.LIVE
        elif initial_state == Application.LIVE:
            new_state = Application.DEAD

        to_toggle['bg'] = new_state
        print('grid_cell at ' + str(column) + " : " + str(row) + ' toggle ' + initial_state + '-->' + new_state)
        return

    def disable_all_cells(self):
        print('Disabling all cells...')
        for row in self.game_grid_cells:
            for cell in row:
                cell.config(state=tk.DISABLED)
        print('All cells disabled.')
        return

    def enable_all_cells(self):
        print('Enabling all cells...')
        for row in self.game_grid_cells:
            for cell in row:
                cell['state'] = tk.NORMAL
        print('All cells enabled.')
        return

    def cell_is_live(self, row, col):
        return self.game_grid_cells[row][col]['bg'] == Application.LIVE

    def kill_cell(self, row, col):
        print('DEATH :: ({0},{1})'.format(col, row))
        self.game_grid_cells[row][col]['bg'] = Application.DEAD
        return

    def revive_cell(self, row, col):
        print('REVIVAL :: ({0},{1})'.format(col, row))
        self.game_grid_cells[row][col]['bg'] = Application.LIVE
        return


def start_application():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    start_application()
