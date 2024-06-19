import tkinter as tk
from parametre import ParametreMenu

class InfiniteGrid(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window title
        self.title("Infinite 2D Grid - Game of Life")
        self.geometry("800x600")

        # Frame for the game
        self.game_frame = tk.Frame(self)
        self.game_frame.pack(fill="both", expand=True)

        # Create a canvas to draw the grid
        self.canvas = tk.Canvas(self.game_frame, bg="#242121")
        self.canvas.pack(fill="both", expand=True)

        # Grid configuration
        self.grid_size = 20  # Size of one grid cell
        self.zoom_level = 1.0  # Initial zoom level

        # Scroll position of the grid
        self.offset_x = 0
        self.offset_y = 0

        # Set to track live cells
        self.live_cells = set()

        # Simulation running status
        self.running = False

        # Simulation turn count
        self.turn_count = 0

        # Menu open status
        self.param_menu_open = False

        # Add event listeners
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.on_mouse_click)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag_left)  # Left click to make cell alive
        self.canvas.bind("<Button-3>", self.on_mouse_click_right)
        self.canvas.bind("<B3-Motion>", self.on_mouse_drag_right)  # Right click to make cell dead
        self.canvas.bind("<B2-Motion>", self.on_mouse_drag)  # Middle click to move the grid
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Button-2>", self.start_drag)  # Define the start of mouse wheel drag

        # Add keyboard shortcuts
        self.bind("<Escape>", self.toggle_parametre_menu)
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<space>", self.toggle_simulation)  # Shortcut to start/stop the simulation
        self.bind("r", self.reset_simulation)  # Shortcut to reset the simulation

        # Add a label to start/stop the simulation
        self.start_label = tk.Label(self.game_frame, text="To start/stop the simulation, press SPACE", fg="white", bg="#242121", font=("Arial", 14, "bold"))
        self.start_label.place(relx=0.5, rely=0.95, anchor="center")  # Center the label at the bottom

        # Add a label to display the turn count at the top left, overlaying the grid
        self.turn_count_label = tk.Label(self.game_frame, text="0", fg="white", bg="#242121", font=("Arial", 18, "bold"))
        self.turn_count_label.place(x=10, y=10)  # Position the label in absolute coordinates

        # Draw the initial grid
        self.draw_grid()

    def draw_grid(self):
        # Clear the entire canvas
        self.canvas.delete("grid")

        # Adjust the size of the cells based on the zoom level
        adjusted_grid_size = self.grid_size * self.zoom_level

        # Draw the live cells
        for cell in self.live_cells:
            x, y = cell
            cell_x = (x - self.offset_x) * adjusted_grid_size
            cell_y = (y - self.offset_y) * adjusted_grid_size
            self.canvas.create_rectangle(
                cell_x, cell_y,
                cell_x + adjusted_grid_size, cell_y + adjusted_grid_size,
                fill="#DED0D0", outline="#DED0D0", tags="grid"
            )

    def on_resize(self, event):
        # Redraw the grid when the window is resized
        self.draw_grid()

    def get_cell_position(self, event):
        # Calculate the position of the cell in the grid
        adjusted_grid_size = self.grid_size * self.zoom_level
        grid_x = int((event.x / adjusted_grid_size) + self.offset_x)
        grid_y = int((event.y / adjusted_grid_size) + self.offset_y)
        return (grid_x, grid_y)

    def on_mouse_click(self, event):
        # Do nothing if the simulation is running
        if self.running:
            return

        cell = self.get_cell_position(event)
        if cell in self.live_cells:
            # The cell is alive, make it dead
            self.live_cells.remove(cell)
        else:
            # The cell is dead, make it alive
            self.live_cells.add(cell)

        # Redraw the grid to reflect the updated state
        self.draw_grid()

    def on_mouse_drag_left(self, event):
        # Do nothing if the simulation is running
        if self.running:
            return

        cell = self.get_cell_position(event)
        # Make the cell alive
        self.live_cells.add(cell)
        # Redraw the grid to reflect the updated state
        self.draw_grid()

    def on_mouse_click_right(self, event):
        # Do nothing if the simulation is running
        if self.running:
            return

        cell = self.get_cell_position(event)
        if cell in self.live_cells:
            # The cell is alive, make it dead
            self.live_cells.remove(cell)
        # Redraw the grid to reflect the updated state
        self.draw_grid()

    def on_mouse_drag_right(self, event):
        # Do nothing if the simulation is running
        if self.running:
            return

        cell = self.get_cell_position(event)
        # Make the cell dead
        if cell in self.live_cells:
            self.live_cells.remove(cell)
        # Redraw the grid to reflect the updated state
        self.draw_grid()

    def start_drag(self, event):
        # Record the initial position of the mouse when the wheel is clicked
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_drag(self, event):
        # Move the grid based on the mouse movement (wheel click)
        dx = event.x - self.start_x
        dy = event.y - self.start_y

        self.offset_x -= dx / (self.grid_size * self.zoom_level)
        self.offset_y -= dy / (self.grid_size * self.zoom_level)

        # Update the starting positions
        self.start_x = event.x
        self.start_y = event.y

        # Redraw the grid
        self.draw_grid()

    def on_mouse_wheel(self, event):
        # Adjust the zoom level based on mouse wheel scrolling
        if event.delta > 0:
            self.zoom_level *= 1.1
        else:
            self.zoom_level *= 0.9

        # Redraw the grid after zooming
        self.draw_grid()

    def start_simulation(self):
        # Toggle the simulation state between running and stopped
        self.running = not self.running
        
        # Update the button text to reflect the current state
        if self.running:
            self.start_label.config(text="Simulation running... Press SPACE to stop")
            # Start the simulation
            self.simulate()
        else:
            self.start_label.config(text="To start/stop the simulation, press SPACE")

    def toggle_simulation(self, event):
        # Shortcut to start/stop the simulation
        self.start_simulation()

    def simulate(self):
        # Check if the simulation is running
        if not self.running:
            return

        # Apply the rules of the Game of Life
        new_live_cells = set()
        
        # Calculate the neighboring cells of all cells (both live and dead) in the set of live cells
        cells_to_check = self.live_cells | {
            (x + dx, y + dy)
            for x, y in self.live_cells
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
            if dx != 0 or dy != 0
        }
        
        for cell in cells_to_check:
            x, y = cell
            live_neighbors = 0
            
            # Count the live neighbors
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    neighbor = (x + dx, y + dy)
                    if neighbor in self.live_cells:
                        live_neighbors += 1

            # Apply the rules of the Game of Life
            if cell in self.live_cells:
                # A live cell with fewer than 2 or more than 3 live neighbors dies
                if live_neighbors < 2 or live_neighbors > 3:
                    continue
                # A live cell with 2 or 3 live neighbors stays alive
                new_live_cells.add(cell)
            else:
                # A dead cell with exactly 3 live neighbors becomes alive
                if live_neighbors == 3:
                    new_live_cells.add(cell)
        
        # Update the set of live cells
        self.live_cells = new_live_cells
        
        # Redraw the grid
        self.draw_grid()
        
        # Update the turn count and the label
        self.turn_count += 1
        self.turn_count_label.config(text=str(self.turn_count))
        
        # Schedule the next simulation cycle after 100 milliseconds
        self.after(100, self.simulate)

    def exit_fullscreen(self, event):
        # Exit fullscreen mode when the Escape key is pressed
        self.attributes("-fullscreen", False)

    def toggle_fullscreen(self, event):
        # Toggle between fullscreen and normal window mode
        self.attributes("-fullscreen", not self.attributes("-fullscreen"))

    def toggle_parametre_menu(self, event):
        if self.param_menu_open:
            self.show_game_screen()
        else:
            self.open_parametre_menu()

    def open_parametre_menu(self):
        # Open the settings menu
        self.running = False
        self.param_menu_open = True
        self.game_frame.pack_forget()
        ParametreMenu(self, self.show_game_screen).pack(fill="both", expand=True)

    def show_game_screen(self):
        self.param_menu_open = False
        for widget in self.winfo_children():
            widget.pack_forget()
        self.game_frame.pack(fill="both", expand=True)

    def reset_simulation(self, event):
        # Reset the simulation
        self.live_cells.clear()
        self.turn_count = 0
        self.turn_count_label.config(text="0")
        self.draw_grid()

# Code to launch the application
if __name__ == "__main__":
    try:
        app = InfiniteGrid()
        app.mainloop()
    except Exception as e:
        print(f"Error creating InfiniteGrid instance: {e}")
