import tkinter as tk
from tkinter import simpledialog

class PatternList(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#3a3a3a")
        self.patterns = []
        self.create_widgets()

    def create_widgets(self):
        self.pattern_listbox = tk.Listbox(self, bg="#3a3a3a", fg="white", font=("Arial", 14), selectmode=tk.SINGLE)
        self.pattern_listbox.pack(fill="both", expand=True)
        self.pattern_listbox.bind("<Double-1>", self.show_pattern_options)

    def add_pattern(self, name, cells):
        self.patterns.append({"name": name, "cells": cells})
        self.pattern_listbox.insert(tk.END, name)

    def show_pattern_options(self, event):
        selected_index = self.pattern_listbox.curselection()
        if not selected_index:
            return

        selected_index = selected_index[0]
        pattern = self.patterns[selected_index]

        option_window = tk.Toplevel(self)
        option_window.title(pattern["name"])
        option_window.geometry("300x150")

        tk.Label(option_window, text=f"Pattern: {pattern['name']}", font=("Arial", 14)).pack(pady=10)

        tk.Button(option_window, text="Rename", command=lambda: self.rename_pattern(selected_index)).pack(pady=5)
        tk.Button(option_window, text="Delete", command=lambda: self.delete_pattern(selected_index)).pack(pady=5)

    def rename_pattern(self, index):
        new_name = simpledialog.askstring("Rename Pattern", "Enter new name:")
        if new_name:
            self.patterns[index]["name"] = new_name
            self.pattern_listbox.delete(index)
            self.pattern_listbox.insert(index, new_name)

    def delete_pattern(self, index):
        del self.patterns[index]
        self.pattern_listbox.delete(index)
