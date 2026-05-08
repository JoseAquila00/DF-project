import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

class Manager:

    def __init__(self, root):
        #finestra principale
        self.root = root
        self.root.title("DF Project")
        self.root.geometry("1200x800")

        self.bg_color = self.root.cget("bg")

        # immagine originale
        self.original_image = None
        
        #frame superiore x bottone e riquadro immagine
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(pady=20)

        #bottone carica
        self.load_button = tk.Button(self.top_frame,text="Carica immagine",width=20,height=2,command=self.load_image)
        self.load_button.grid(row=0,column=0,padx=20)

        #riquadro immagine
            # contenitore immagine originale
        self.original_frame = tk.Frame(self.top_frame,width=400,height=300,bg=self.bg_color)
        self.original_frame.grid(row=0,column=1,padx=20)
        self.original_frame.grid_propagate(False)

        # label immagine
        self.original_image_label = tk.Label(self.original_frame,text="Nessuna immagine caricata",bg=self.bg_color,fg="gray",font=("Arial", 14))
        self.original_image_label.place(relx=0.5,rely=0.5,anchor="center")

        #frame per i filtri
        self.filters_frame = tk.Frame(self.root)
        self.filters_frame.pack(pady=20)
        
        #bottone filtro 1
        self.fourier_button = tk.Button(self.filters_frame,text="Spettro di Fourier",width=22,height=2)
        self.fourier_button.grid(row=0,column=0,padx=20, pady=10)
        #riquadro output filtro 1
        self.fourier_output = tk.Label(self.filters_frame,text="Output Fourier",bg="lightgray",width=35,height=12)
        self.fourier_output.grid(row=1,column=0,padx=20)

        #bottone filtro 2
        self.canny_button = tk.Button(self.filters_frame,text="Canny",width=22,height=2)
        self.canny_button.grid(row=0,column=1,padx=20, pady=10)
        #riquadro output filtro 2
        self.canny_output = tk.Label(self.filters_frame,text="Output Canny",bg="lightgray",width=35,height=12)
        self.canny_output.grid(row=1,column=1,padx=20)

        #bottone filtro 3
        self.contrast_button = tk.Button(self.filters_frame,text="Miglioramento Contrasto",width=22,height=2)
        self.contrast_button.grid(row=0,column=2,padx=20, pady=10)
        #riquadro output filtro 3
        self.contrast_output = tk.Label(self.filters_frame,text="Output Miglioramento Contrasto",bg="lightgray",width=35,height=12)
        self.contrast_output.grid(row=1,column=2,padx=20)

            
    # CARICAMENTO IMMAGINE
    # =====================================
    def show_image(self, image, label, size=(400, 300)):
            # se immagine in scala di grigi
        if len(image.shape) == 2:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        else:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image_pil = Image.fromarray(image_rgb)
        image_pil.thumbnail(size)

        image_tk = ImageTk.PhotoImage(image_pil)

        label.config(image=image_tk, text="")
        label.image = image_tk

    def load_image(self):
        # apre finestra selezione file
        file_path = filedialog.askopenfilename(
            title="Seleziona immagine",
            filetypes=[
                ("Immagini", "*.jpg *.png *.jpeg *.bmp")
            ]
        )

        # se utente annulla
        if not file_path:
            return

        # legge immagine con OpenCV
        self.original_image = cv2.imread(file_path)

        if self.original_image is None:
            return

        self.show_image(
            self.original_image,
            self.original_image_label,
            size=(400, 300)
        )
