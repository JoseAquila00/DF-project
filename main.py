import tkinter as tk


class ImageFilterApp:

    def __init__(self, root):

        self.root = root

        self.root.title("DF Project - OpenCV")

        self.root.geometry("1200x800")


if __name__ == "__main__":

    root = tk.Tk()

    app = ImageFilterApp(root)

    root.mainloop()