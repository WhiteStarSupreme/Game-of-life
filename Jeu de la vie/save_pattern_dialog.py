import tkinter as tk
from tkinter import messagebox

class SavePatternDialog(tk.Toplevel):
    def __init__(self, parent, cells):
        super().__init__(parent)
        self.cells = cells
        self.parent = parent
        self.title("Save Pattern")
        self.geometry("300x200")
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Enter pattern name:", fg="white", bg="#242121", font=("Arial", 14))
        self.label.pack(pady=10)

        self.name_entry = tk.Entry(self, font=("Arial", 14))
        self.name_entry.pack(pady=10)

        self.button_frame = tk.Frame(self, bg="#242121")
        self.button_frame.pack(pady=10)

        self.save_button = tk.Button(self.button_frame, text="Save", command=self.save_pattern, fg="white", bg="#3a3a3a", font=("Arial", 14, "bold"))
        self.save_button.pack(side="left", padx=10)

        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.destroy, fg="white", bg="#3a3a3a", font=("Arial", 14, "bold"))
        self.cancel_button.pack(side="right", padx=10)

    def save_pattern(self):
        pattern_name = self.name_entry.get().strip()
        if pattern_name:
            self.parent.pattern_list.add_pattern(pattern_name, self.cells)
            messagebox.showinfo("Pattern Saved", f"Pattern '{pattern_name}' saved successfully.")
            self.destroy()
