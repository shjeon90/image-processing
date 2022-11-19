import numpy as np
import cv2
import qimage2ndarray


def recarray_to_ndarray(recarry):
    r = recarry['r']
    g = recarry['g']
    b = recarry['b']
    a = recarry['a']

    data = np.concatenate((
        r[..., np.newaxis],
        g[..., np.newaxis],
        b[..., np.newaxis],
        a[..., np.newaxis]
    ), -1)

    return data

def ndarray_to_qimage(array):
    qimage = qimage2ndarray.array2qimage(array, normalize=False)
    return qimage

def gray_to_rgb(gray):
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)