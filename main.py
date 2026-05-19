import customtkinter as ctk
from manager import Manager


if __name__ == "__main__":
    root = ctk.CTk()
    app = Manager(root)
    root.mainloop()