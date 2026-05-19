import tkinter as tk
import customtkinter as ctk
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

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.root.configure(fg_color="#ECEEF2")

        self.bg_color = self.root.cget("bg")

        # immagine originale
        self.original_image = None
        
        #frame superiore x bottone e riquadro immagine
        self.top_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.top_frame.pack(pady=20)

        #bottone carica
        self.load_button = ctk.CTkButton(self.top_frame,text="Carica immagine",width=180,height=45,corner_radius=18,command=self.load_image)
        self.load_button.grid(row=0,column=0,padx=20)

        #riquadro immagine
            # contenitore immagine originale
        self.original_frame = ctk.CTkFrame(self.top_frame,width=400,height=300,corner_radius=25,fg_color="#F5F6FA")
        self.original_frame.grid(row=0,column=1,padx=20)
        self.original_frame.grid_propagate(False)

        # label immagine
        self.original_image_label = tk.Label(self.original_frame,text="Nessuna immagine caricata",bg=self.bg_color,fg="gray",font=("Arial", 14))
        self.original_image_label.place(relx=0.5,rely=0.5,anchor="center")

        #frame per i filtri
        self.filters_frame = tk.Frame(self.root)
        self.filters_frame.pack(pady=20)
        
        #bottone filtro 1
        self.fourier_button = ctk.CTkButton(self.filters_frame,text="Spettro di Fourier",width=200,height=40, corner_radius=20,fg_color="#4A90E2",hover_color="#357ABD",command=self.on_fourier_click)
        self.fourier_button.grid(row=0,column=0,padx=20, pady=10)
        #riquadro output filtro 1
        self.fourier_frame = ctk.CTkFrame(self.filters_frame,width=300,height=220,corner_radius=20,fg_color="#DDE1E7")
        self.fourier_frame.grid(row=1, column=0, padx=20)
        self.fourier_frame.grid_propagate(False)

        self.fourier_output = ctk.CTkLabel(self.fourier_frame,text="Fourier non applicato",text_color="#555555", font=("Arial", 18))
        self.fourier_output.place(relx=0.5, rely=0.5, anchor="center")

        #bottone filtro 2
        self.canny_button = ctk.CTkButton(self.filters_frame,text="Canny",width=200,height=40, corner_radius=20,fg_color="#4A90E2",hover_color="#357ABD",command=self.on_canny_click)
        self.canny_button.grid(row=0,column=1,padx=20, pady=10)
        #riquadro output filtro 2
        self.canny_frame = ctk.CTkFrame(self.filters_frame,width=300,height=220,corner_radius=20,fg_color="#DDE1E7")
        self.canny_frame.grid(row=1, column=1, padx=20)
        self.canny_frame.grid_propagate(False)

        self.canny_output = ctk.CTkLabel(self.canny_frame,text="Canny non applicato",text_color="#555555", font=("Arial", 18))
        self.canny_output.place(relx=0.5, rely=0.5, anchor="center")

        #bottone filtro 3
        self.contrast_button = ctk.CTkButton(self.filters_frame,text="Miglioramento Contrasto",width=200,height=40, corner_radius=20,fg_color="#4A90E2",hover_color="#357ABD",command=self.on_contrast_slider_change)
        self.contrast_button.grid(row=0,column=2,padx=20, pady=10)
        #riquadro output filtro 3
        self.contrast_frame = ctk.CTkFrame(self.filters_frame,width=300,height=220,corner_radius=20,fg_color="#DDE1E7")
        self.contrast_frame.grid(row=1, column=2, padx=20)
        self.contrast_frame.grid_propagate(False)
        #slider filtro 3
        self.contrast_label = ctk.CTkLabel(self.filters_frame,text="Contrasto",font=("Arial", 14))
        self.contrast_label.grid(row=2,column=2,pady=(10, 0))
        self.contrast_slider = ctk.CTkSlider(self.filters_frame,from_=-100,to=100,width=180,orientation="horizontal",command=self.on_contrast_slider_change)
        self.contrast_slider.set(0)
        self.contrast_slider.grid(row=3, column=2, pady=(10, 0))

        self.contrast_output = ctk.CTkLabel(self.contrast_frame,text="Miglioramento\nContrasto",text_color="#555555", font=("Arial", 18))
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

        label.configure(image=image_tk, text="")
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

    def on_contrast_slider_change(self, value=None):
        if self.original_image is None:
            return

        slider_value = self.contrast_slider.get()

        alpha = max(0.1, 1 + (slider_value / 100))
        
        result = improve_contrast(
            self.original_image,
            alpha
        )

        self.show_image(
            result,
            self.contrast_output,
            size=(300, 220)
        )