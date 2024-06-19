import tkinter as tk

class ParametreMenu(tk.Frame):
    def __init__(self, parent, show_game_screen):
        super().__init__(parent, bg="#242121")
        self.show_game_screen = show_game_screen
        self.create_widgets()

    def create_widgets(self):
        # Button to resume the simulation
        self.resume_button = tk.Button(self, text="Resume", command=self.show_game_screen, fg="white", bg="#3a3a3a", font=("Arial", 14, "bold"))
        self.resume_button.pack(pady=10)

        # Button to view the controls
        self.controls_button = tk.Button(self, text="Controls", command=self.show_controls, fg="white", bg="#3a3a3a", font=("Arial", 14, "bold"))
        self.controls_button.pack(pady=10)

        # Button to quit the application
        self.quit_button = tk.Button(self, text="Quit", command=self.quit_application, fg="white", bg="#3a3a3a", font=("Arial", 14, "bold"))
        self.quit_button.pack(pady=10)

    def show_controls(self):
        self.pack_forget()
        ControlsMenu(self.master, self.show_game_screen, self.pack).pack(fill="both", expand=True)

    def quit_application(self):
        self.master.quit()

class ControlsMenu(tk.Frame):
    def __init__(self, parent, show_game_screen, show_parametre_menu):
        super().__init__(parent, bg="#242121")
        self.show_game_screen = show_game_screen
        self.show_parametre_menu = show_parametre_menu
        self.create_widgets()

    def create_widgets(self):
        # Label to display the controls
        self.controls_label = tk.Label(self, text="Controls:\n\n"
                                                  "Space: Start/Stop the simulation\n"
                                                  "F11: Fullscreen\n"
                                                  "Escape: Open the settings menu\n"
                                                  "R: Reset the simulation\n"
                                                  "Click to toggle cell state\n"
                                                  "Mouse wheel: Zoom\n"
                                                  "Mouse wheel click: Move the grid", fg="white", bg="#242121", font=("Arial", 14))
        self.controls_label.pack(pady=10)

        # Button to close the controls menu
        self.back_button = tk.Button(self, text="Back", command=self.show_parametre_menu, fg="white", bg="#3a3a3a", font=("Arial", 14, "bold"))
        self.back_button.pack(pady=10)
