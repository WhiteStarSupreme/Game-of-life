import tkinter as tk
from tkinter import messagebox

class ParametreMenu(tk.Frame):
    def __init__(self, parent, show_game_screen):
        super().__init__(parent, bg="#242121")
        self.parent = parent
        self.show_game_screen = show_game_screen
        self.create_widgets()

    def create_widgets(self):
        # Button to resume the simulation
        self.resume_button = tk.Button(self, text="Resume", command=self.show_game_screen, fg="white", bg="#3a3a3a", font=("Arial", 14, "bold"))
        self.resume_button.pack(pady=10)

        # Button to view controls
        self.controls_button = tk.Button(self, text="Controls", command=self.show_controls, fg="white", bg="#3a3a3a", font=("Arial", 14, "bold"))
        self.controls_button.pack(pady=10)

        # Button to quit the application
        self.quit_button = tk.Button(self, text="Quit", command=self.quit_application, fg="white", bg="#3a3a3a", font=("Arial", 14, "bold"))
        self.quit_button.pack(pady=10)

    def show_controls(self):
        self.pack_forget()
        ControlsMenu(self.parent, self.show_game_screen, self.show_parametre_menu).pack(fill="both", expand=True)

    def quit_application(self):
        self.parent.quit()

    def show_parametre_menu(self):
        self.pack(fill="both", expand=True)


class ControlsMenu(tk.Frame):
    def __init__(self, parent, show_game_screen, show_parametre_menu):
        super().__init__(parent, bg="#242121")
        self.parent = parent
        self.show_game_screen = show_game_screen
        self.show_parametre_menu = show_parametre_menu
        self.create_widgets()

    def create_widgets(self):
        # Label to display the controls
        self.controls_label = tk.Label(self, text="Controls:\n\n"
                                                  "Space: Start/Stop simulation\n"
                                                  "F11: Fullscreen\n"
                                                  "Escape: Open settings menu\n"
                                                  "R: Reset simulation\n"
                                                  "Left Click: Toggle cell to alive\n"
                                                  "Right Click: Toggle cell to dead\n"
                                                  "Mouse Wheel: Zoom\n"
                                                  "Mouse Wheel Click: Pan grid", fg="white", bg="#242121", font=("Arial", 14))
        self.controls_label.pack(pady=10)

        # Button to go back to the parameter menu
        self.back_button = tk.Button(self, text="Back", command=self.back_to_parametre_menu, fg="white", bg="#3a3a3a", font=("Arial", 14, "bold"))
        self.back_button.pack(pady=10)

    def back_to_parametre_menu(self):
        self.pack_forget()
        self.show_parametre_menu()

