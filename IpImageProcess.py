import cv2
import qimage2ndarray
from utils import *
from PyQt5.QtGui import QPixmap

class IpImageProcess:
    def __init__(self, *args, **kwargs):
        self.parent = args[0]

    def clear(self):
        self.parent.img = self.parent.img_orig.copy()
        self.parent.update()

    def set_threshold(self, thr):
        img_orig = self.parent.img_orig.toImage()
        img_orig_rec = qimage2ndarray.recarray_view(img_orig)
        img_orig_nd = recarray_to_ndarray(img_orig_rec)

        alpha = img_orig_nd[:,:,-1]
        img_gray = np.mean(img_orig_nd[:,:,:-1], -1)
        _, img_th = cv2.threshold(img_gray, thr, 255, cv2.THRESH_BINARY)
        img_th = img_th.astype(np.uint8)
        img_rgb = gray_to_rgb(img_th)
        img_rgba = np.concatenate((
            img_rgb, alpha[..., np.newaxis]
        ), -1)

        self.parent.img = QPixmap.fromImage(qimage2ndarray.array2qimage(img_rgba, normalize=False))

        self.parent.update()