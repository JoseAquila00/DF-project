import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from filters import apply_fourier, apply_canny, improve_contrast

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
        self.fourier_button = tk.Button(self.filters_frame,text="Spettro di Fourier",width=22,height=2, command=self.on_fourier_click)
        self.fourier_button.grid(row=0,column=0,padx=20, pady=10)
        #riquadro output filtro 1
        self.fourier_frame = tk.Frame(self.filters_frame,width=300,height=220,bg="lightgray")
        self.fourier_frame.grid(row=1, column=0, padx=20)
        self.fourier_frame.grid_propagate(False)

        self.fourier_output = tk.Label(self.fourier_frame,text="Output Fourier",bg="lightgray")
        self.fourier_output.place(relx=0.5, rely=0.5, anchor="center")

        #bottone filtro 2
        self.canny_button = tk.Button(self.filters_frame,text="Canny",width=22,height=2, command=self.on_canny_click)
        self.canny_button.grid(row=0,column=1,padx=20, pady=10)
        #riquadro output filtro 2
        self.canny_frame = tk.Frame(self.filters_frame,width=300,height=220,bg="lightgray")
        self.canny_frame.grid(row=1, column=1, padx=20)
        self.canny_frame.grid_propagate(False)

        self.canny_output = tk.Label(self.canny_frame,text="Output Canny",bg="lightgray")
        self.canny_output.place(relx=0.5, rely=0.5, anchor="center")

        #bottone filtro 3
        self.contrast_button = tk.Button(self.filters_frame,text="Miglioramento Contrasto",width=22,height=2, command=self.on_contrast_click)
        self.contrast_button.grid(row=0,column=2,padx=20, pady=10)
        #riquadro output filtro 3
        self.contrast_frame = tk.Frame(self.filters_frame,width=300,height=220,bg="lightgray")
        self.contrast_frame.grid(row=1, column=2, padx=20)
        self.contrast_frame.grid_propagate(False)

        self.contrast_output = tk.Label(self.contrast_frame,text="Output Miglioramento\nContrasto",bg="lightgray")
        self.contrast_output.place(relx=0.5, rely=0.5, anchor="center")

            
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

    def on_fourier_click(self):
        if self.original_image is None:
            return

        result = apply_fourier(self.original_image)

        self.show_image(
            result,
            self.fourier_output,
            size=(300, 220)
        )

    def on_canny_click(self):
        if self.original_image is None:
            return

        t1 = 50
        t2 = 150

        result = apply_canny(self.original_image, t1, t2)

        self.show_image(
            result,
            self.canny_output,
            size=(300, 220)
        )

    def on_contrast_click(self):
        if self.original_image is None:
            return

        alpha = 1.5

        result = improve_contrast(self.original_image, alpha)

        self.show_image(
            result,
            self.contrast_output,
            size=(300, 220)
        )
