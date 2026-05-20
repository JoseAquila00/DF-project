import cv2
import numpy as np

def apply_fourier(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)#Converte l’immagine da colori BGR a scala di grigi, perché la trasformata di Fourier è più semplice da calcolare su immagini in scala di grigi (una sola matrice di valori).

    f = np.fft.fft2(gray)#Applica la trasformata di Fourier 2D all’immagine in scala di grigi, ottenendo una matrice di numeri complessi che rappresentano le frequenze dell’immagine.
    fshift = np.fft.fftshift(f)#Sposta le frequenze basse al centro dell’immagine

    magnitude = 20 * np.log(np.abs(fshift) + 1)#Calcola lintensità delle frequenze, prendendo il logaritmo per rendere i valori più gestibili e aggiungendo 1 per evitare problemi con il logaritmo di zero.

    magnitude = cv2.normalize(#Normalizza i valori di magnitude per portarli nell’intervallo 0-255, rendendoli adatti per la visualizzazione come immagine
        magnitude,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    return np.uint8(magnitude)#Converte il risultato in immagine a 8 bit, adatta per essere visualizzata


def apply_canny(image, t1, t2):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)#Converte l’immagine da colori BGR a scala di grigi, perché l’algoritmo di Canny lavora su immagini in scala di grigi (una matrice di valori) per identificare i bordi basandosi sui cambiamenti di intensità.
    edges = cv2.Canny(gray, t1, t2)#

    return edges


def improve_contrast(image, alpha):
    beta = 0#Il parametro beta è un valore di offset che viene aggiunto a ogni pixel dopo la moltiplicazione per alpha. In questo caso, è impostato a 0, il che significa che non viene aggiunto alcun offset. Se volessi aumentare ulteriormente la luminosità dell’immagine, potresti impostare beta a un valore positivo (ad esempio, 50), mentre se volessi scurire l’immagine, potresti impostarlo a un valore negativo (ad esempio, -50).

    contrast_image = cv2.convertScaleAbs(#applica la formula new_pixel = alpha * old_pixel + beta a ogni pixel dell’immagine, dove alpha è il fattore di contrasto e beta è l’offset di luminosità. La funzione restituisce un’immagine con i valori dei pixel scalati e convertiti in valori assoluti a 8 bit (0-255), adatta per essere visualizzata.
        image,
        alpha=alpha,
        beta=beta
    )

    return contrast_image