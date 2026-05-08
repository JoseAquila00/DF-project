import tkinter as tk
from manager import Manager


if __name__ == "__main__":
    root = tk.Tk()
    app = Manager(root)
    root.mainloop()