import tkinter as tk
from tkinter import font

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # Initialize UI settings
        self.grid(row=0, column=0)
        self.size_x = 40
        self.size_y = 40
        self.game_grid_cells = []
        self.intro_frame = None
        self.start_button = None
        self.reset_button = None
        self.title_font = font.Font(family="Helvetica", size=14)

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
        self.start_button = tk.Button(self.master, text="Start Game", command=self.launch())
        self.start_button.grid(row=1, column=1, sticky=tk.E)

        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset)
        self.reset_button.grid(row=1, column=2, sticky=tk.W)



    def launch(self):
        print("LAUNCH")

    def reset(self):
        print("RESET")


def start_application():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    start_application()
