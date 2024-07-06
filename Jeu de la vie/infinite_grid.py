import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import threading

class InfiniteGrid(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Infinite 2D Grid - Game of Life")
        self.geometry("800x600")

        self.game_frame = tk.Frame(self)
        self.game_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.game_frame, bg="#242121")
        self.canvas.pack(fill="both", expand=True)

        # Ajout du bouton "Pattern" en overlay
        self.pattern_button = tk.Button(self, text="Patterns", command=self.toggle_pattern_sidebar, fg="white", bg="#3a3a3a", font=("Arial", 14, "bold"))
        self.pattern_button.place(relx=0.98, rely=0.02, anchor="ne")

        self.grid_size = 20
        self.zoom_level = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.live_cells = set()
        self.running = False
        self.turn_count = 0
        self.param_menu_open = False
        self.saved_patterns = {}

        self.selecting = False
        self.selection_start = None
        self.selection_end = None
        self.selection_rectangle = None
        self.sidebar_open = False
        self.sidebar = None

        self.dragging_pattern = False
        self.dragged_pattern = None

        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.on_mouse_click)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag_left)
        self.canvas.bind("<Button-3>", self.on_mouse_click_right)
        self.canvas.bind("<B3-Motion>", self.on_mouse_drag_right)
        self.canvas.bind("<B2-Motion>", self.on_mouse_drag)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Button-2>", self.start_drag)
        self.canvas.bind("<Control-Button-1>", self.start_selection)
        self.canvas.bind("<Control-B1-Motion>", self.update_selection)
        self.canvas.bind("<Control-ButtonRelease-1>", self.end_selection)

        self.bind("<Escape>", self.toggle_parametre_menu)
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<space>", self.toggle_simulation)
        self.bind("r", self.reset_simulation)

        self.start_label = tk.Label(self.game_frame, text="Press SPACE to start/stop the simulation", fg="white", bg="#242121", font=("Arial", 14, "bold"))
        self.start_label.place(relx=0.5, rely=0.95, anchor="center")

        self.turn_count_label = tk.Label(self.game_frame, text="0", fg="white", bg="#242121", font=("Arial", 18, "bold"))
        self.turn_count_label.place(x=10, y=10)

        self.draw_grid()

        # Charger les patterns sauvegardés à partir du fichier JSON
        self.load_saved_patterns()

    def draw_grid(self):
        self.canvas.delete("grid")
        adjusted_grid_size = self.grid_size * self.zoom_level

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
        self.draw_grid()

    def get_cell_position(self, event):
        adjusted_grid_size = self.grid_size * self.zoom_level
        grid_x = int((event.x / adjusted_grid_size) + self.offset_x)
        grid_y = int((event.y / adjusted_grid_size) + self.offset_y)
        return (grid_x, grid_y)

    def on_mouse_click(self, event):
        if self.running:
            return

        if self.dragging_pattern and self.dragged_pattern:
            self.place_pattern(event)
            return

        cell = self.get_cell_position(event)
        if cell in self.live_cells:
            self.live_cells.remove(cell)
        else:
            self.live_cells.add(cell)
        self.draw_grid()

    def on_mouse_drag_left(self, event):
        if self.running:
            return

        cell = self.get_cell_position(event)
        self.live_cells.add(cell)
        self.draw_grid()

    def on_mouse_click_right(self, event):
        if self.running:
            return

        cell = self.get_cell_position(event)
        if cell in self.live_cells:
            self.live_cells.remove(cell)
        self.draw_grid()

    def on_mouse_drag_right(self, event):
        if self.running:
            return

        cell = self.get_cell_position(event)
        if cell in self.live_cells:
            self.live_cells.remove(cell)
        self.draw_grid()

    def start_drag(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_drag(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y

        self.offset_x -= dx / (self.grid_size * self.zoom_level)
        self.offset_y -= dy / (self.grid_size * self.zoom_level)

        self.start_x = event.x
        self.start_y = event.y

        self.draw_grid()

    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.zoom_level *= 1.1
        else:
            self.zoom_level *= 0.9

        self.draw_grid()

    def start_simulation(self):
        self.running = not self.running

        if self.running:
            self.start_label.config(text="Simulation running... Press SPACE to stop")
            self.simulate()
        else:
            self.start_label.config(text="Press SPACE to start/stop the simulation")

    def toggle_simulation(self, event):
        self.start_simulation()

    def simulate(self):
        if not self.running:
            return

        new_live_cells = set()
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

            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    neighbor = (x + dx, y + dy)
                    if neighbor in self.live_cells:
                        live_neighbors += 1

            if cell in self.live_cells:
                if live_neighbors < 2 or live_neighbors > 3:
                    continue
                new_live_cells.add(cell)
            else:
                if live_neighbors == 3:
                    new_live_cells.add(cell)

        self.live_cells = new_live_cells
        self.draw_grid()
        self.turn_count += 1
        self.turn_count_label.config(text=str(self.turn_count))
        self.after(100, self.simulate)

    def exit_fullscreen(self, event):
        self.attributes("-fullscreen", False)

    def toggle_fullscreen(self, event):
        self.attributes("-fullscreen", not self.attributes("-fullscreen"))

    def toggle_parametre_menu(self, event):
        if self.param_menu_open:
            self.show_game_screen()
        else:
            self.open_parametre_menu()

    def open_parametre_menu(self):
        self.running = False
        self.param_menu_open = True
        self.game_frame.pack_forget()
        # Import du ParametreMenu ici
        ParametreMenu(self, self.show_game_screen).pack(fill="both", expand=True)

    def show_game_screen(self):
        self.param_menu_open = False
        for widget in self.winfo_children():
            widget.pack_forget()
        self.game_frame.pack(fill="both", expand=True)

    def reset_simulation(self, event):
        self.live_cells.clear()
        self.turn_count = 0
        self.turn_count_label.config(text="0")
        self.draw_grid()

    def start_selection(self, event):
        self.selecting = True
        self.selection_start = self.get_cell_position(event)
        self.selection_end = self.selection_start
        x, y = event.x, event.y
        self.selection_rectangle = self.canvas.create_rectangle(x, y, x, y, outline="white", dash=(2, 2))

    def update_selection(self, event):
        if not self.selecting:
            return

        x1, y1 = self.canvas.coords(self.selection_rectangle)[:2]
        x2, y2 = event.x, event.y
        self.canvas.coords(self.selection_rectangle, x1, y1, x2, y2)
        self.selection_end = self.get_cell_position(event)

    def end_selection(self, event):
        if not self.selecting:
            return

        self.selecting = False
        self.canvas.delete(self.selection_rectangle)
        self.selection_rectangle = None
        self.save_selection()

    def save_selection(self):
        x1, y1 = min(self.selection_start[0], self.selection_end[0]), min(self.selection_start[1], self.selection_end[1])
        x2, y2 = max(self.selection_start[0], self.selection_end[0]), max(self.selection_start[1], self.selection_end[1])

        selected_cells = {
            (x, y)
            for x in range(x1, x2 + 1)
            for y in range(y1, y2 + 1)
            if (x, y) in self.live_cells
        }

        if selected_cells:
            pattern_name = simpledialog.askstring("Pattern Name", "Enter a name for the pattern:")
            if pattern_name:
                self.save_pattern(pattern_name, selected_cells)

    def save_pattern(self, name, pattern):
        if name in self.saved_patterns:
            messagebox.showwarning("Pattern Exists", f"A pattern with the name '{name}' already exists.")
            return

        min_x = min(pattern, key=lambda cell: cell[0])[0]
        min_y = min(pattern, key=lambda cell: cell[1])[1]
        normalized_pattern = [(cell[0] - min_x, cell[1] - min_y) for cell in pattern]

        self.saved_patterns[name] = {
            "cells": normalized_pattern,
            "width": max(cell[0] for cell in normalized_pattern) + 1,
            "height": max(cell[1] for cell in normalized_pattern) + 1
        }

        # Sauvegarde au format JSON
        with open("saved_patterns.json", "w") as f:
            json.dump(self.saved_patterns, f, indent=4)

        print(f"Pattern saved: {name} with {len(pattern)} cells")

    def load_saved_patterns(self):
        try:
            with open("saved_patterns.json", "r") as f:
                self.saved_patterns = json.load(f)
        except FileNotFoundError:
            self.saved_patterns = {}

    def toggle_pattern_sidebar(self):
        if self.sidebar_open:
            self.close_pattern_sidebar()
        else:
            self.open_pattern_sidebar()

    def open_pattern_sidebar(self):
        self.sidebar_open = True
        self.sidebar = tk.Frame(self, bg="#3a3a3a", width=200)
        self.sidebar.place(relx=1.0, rely=0, anchor="ne", relheight=1.0)

        # Afficher les patterns sauvegardés
        pattern_label = tk.Label(self.sidebar, text="Saved Patterns", fg="white", bg="#3a3a3a", font=("Arial", 14, "bold"))
        pattern_label.pack(pady=10)

        for pattern_name in self.saved_patterns.keys():
            pattern_button = tk.Button(self.sidebar, text=pattern_name, command=lambda name=pattern_name: self.select_pattern(name), fg="white", bg="#3a3a3a", font=("Arial", 12, "bold"))
            pattern_button.pack(fill="x", pady=2)

        # Bouton pour fermer le sidebar
        close_button = tk.Button(self.sidebar, text="Close", command=self.close_pattern_sidebar, fg="white", bg="#3a3a3a", font=("Arial", 12, "bold"))
        close_button.pack(pady=10)

        # Bouton pour supprimer le pattern sélectionné
        delete_button = tk.Button(self.sidebar, text="Delete Pattern", command=self.delete_selected_pattern, fg="white", bg="red", font=("Arial", 12, "bold"))
        delete_button.pack(pady=10)

    def close_pattern_sidebar(self):
        if self.sidebar:
            self.sidebar.destroy()
        self.sidebar_open = False

    def select_pattern_to_drag(self, name):
        self.dragging_pattern = True
        self.dragged_pattern = name
        self.canvas.bind("<Motion>", self.show_pattern_preview)
        self.canvas.bind("<ButtonRelease-1>", self.on_pattern_drop)

    def show_pattern_preview(self, event):
        if not self.dragging_pattern or not self.dragged_pattern:
            return

        self.draw_grid()  # Clear previous preview
        pattern = self.saved_patterns[self.dragged_pattern]["cells"]
        grid_size = self.grid_size * self.zoom_level

        for cell in pattern:
            x, y = cell
            cell_x = (x + event.x / grid_size - self.offset_x)
            cell_y = (y + event.y / grid_size - self.offset_y)
            self.canvas.create_rectangle(
                cell_x * grid_size, cell_y * grid_size,
                (cell_x + 1) * grid_size, (cell_y + 1) * grid_size,
                fill="#DED0D0", outline="#DED0D0", tags="grid"
            )

    def on_pattern_drop(self, event):
        if not self.dragging_pattern or not self.dragged_pattern:
            return

        self.dragging_pattern = False
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.place_pattern(event)

    def place_pattern(self, event):
        pattern = self.saved_patterns[self.dragged_pattern]["cells"]
        grid_size = self.grid_size * self.zoom_level

        for cell in pattern:
            x, y = cell
            cell_x = int(x + event.x / grid_size - self.offset_x)
            cell_y = int(y + event.y / grid_size - self.offset_y)
            self.live_cells.add((cell_x, cell_y))

        self.dragged_pattern = None
        self.draw_grid()

    def select_pattern(self, name):
        self.selected_pattern = name
        print(f"Selected pattern: {name}")

    def delete_selected_pattern(self):
        pattern_to_delete = simpledialog.askstring("Delete Pattern", "Enter the name of the pattern to delete:", initialvalue=self.selected_pattern)
        if pattern_to_delete and pattern_to_delete in self.saved_patterns:
            # Exécute la suppression dans un thread séparé
            threading.Thread(target=self.perform_pattern_deletion, args=(pattern_to_delete,)).start()
        else:
            messagebox.showwarning("Pattern Not Found", f"No pattern named '{pattern_to_delete}' found.")

    def perform_pattern_deletion(self, pattern_to_delete):
        del self.saved_patterns[pattern_to_delete]
        # Sauvegarde les modifications
        with open("saved_patterns.json", "w") as f:
            json.dump(self.saved_patterns, f, indent=4)
        messagebox.showinfo("Pattern Deleted", f"Pattern '{pattern_to_delete}' has been deleted.")
        self.selected_pattern = None
        self.toggle_pattern_sidebar()  # Refresh the sidebar to reflect changes
