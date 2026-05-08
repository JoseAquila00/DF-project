import cv2
import numpy as np

import cv2
import numpy as np


def apply_fourier(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)

    magnitude = 20 * np.log(np.abs(fshift) + 1)

    magnitude = cv2.normalize(
        magnitude,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    return np.uint8(magnitude)


def apply_canny(image, t1, t2):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, t1, t2)

    return edges


def improve_contrast(image, alpha):
    beta = 0

    contrast_image = cv2.convertScaleAbs(
        image,
        alpha=alpha,
        beta=beta
    )

    return contrast_image