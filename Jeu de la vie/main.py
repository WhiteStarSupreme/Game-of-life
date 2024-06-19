from infinite_grid import InfiniteGrid

try:
    app = InfiniteGrid()
    app.mainloop()
except Exception as e:
    print(f"Error creating InfiniteGrid instance: {e}")
