# run_app.py

import tkinter as tk
from main import WatercolorArtistTool

if __name__ == '__main__':
    root = tk.Tk()
    app = WatercolorArtistTool(root)
    root.mainloop()