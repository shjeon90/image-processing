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

    def get_gray_alpha(self):
        img_orig = self.parent.img_orig.toImage()
        img_orig_rec = qimage2ndarray.recarray_view(img_orig)
        img_orig_nd = recarray_to_ndarray(img_orig_rec)
        img_orig_nd = img_orig_nd

        alpha = img_orig_nd[:, :, -1].astype(np.uint8)
        img_gray = np.mean(img_orig_nd[:, :, :-1], -1).astype(np.uint8)

        # return img_orig_nd
        return img_gray, alpha

    def do_postprocess(self, img, alpha):
        img = img.astype(np.uint8)
        img_rgb = gray_to_rgb(img)
        img_rgba = np.concatenate((
            img_rgb, alpha[..., np.newaxis]
        ), -1)

        self.parent.img = QPixmap.fromImage(qimage2ndarray.array2qimage(img_rgba, normalize=False))
        self.parent.update()

    def set_threshold(self, thr):
        img_gray, alpha = self.get_gray_alpha()

        _, img_th = cv2.threshold(img_gray, thr, 255, cv2.THRESH_BINARY)

        self.do_postprocess(img_th, alpha)


    def set_hist(self):
        img_gray, alpha = self.get_gray_alpha()

        img_hist = cv2.equalizeHist(img_gray)
        self.do_postprocess(img_hist, alpha)

    def set_gaussian_filter(self):
        img_gray, alpha = self.get_gray_alpha()

        img_gf = cv2.GaussianBlur(img_gray, ksize=(7, 7), sigmaX=10.)
        self.do_postprocess(img_gf, alpha)

    def set_laplacian_filter(self):
        img_gray, alpha = self.get_gray_alpha()

        img_lf = cv2.Laplacian(img_gray, -1)

        self.do_postprocess(img_lf, alpha)

    def set_bilateral_filter(self):
        img_gray, alpha = self.get_gray_alpha()

        img_bif = cv2.bilateralFilter(img_gray, d=-1, sigmaColor=10, sigmaSpace=10)

        self.do_postprocess(img_bif, alpha)

    def scale_image(self, p):

        p = p / 255. * 2.

        img_gray, alpha = self.get_gray_alpha()
        rows, cols = img_gray.shape[:2]

        T = np.array([
            [p, 0., 0.],
            [0., p, 0.]
        ]).astype(np.float32)
        img_sc = cv2.warpAffine(img_gray, T, (cols, rows))

        self.do_postprocess(img_sc, alpha)

    def rotate_image(self, r):
        img_gray, alpha = self.get_gray_alpha()
        rows, cols = img_gray.shape[:2]

        T = cv2.getRotationMatrix2D((cols // 2, rows // 2), -r, 1.0)
        img_rot = cv2.warpAffine(img_gray, T, (cols, rows))

        self.do_postprocess(img_rot, alpha)

    def reflect_image(self):
        img_gray, alpha = self.get_gray_alpha()
        rows, cols = img_gray.shape[:2]

        T = np.array([
            [-1., 0., cols-1],
            [0., 1., 0.]
        ])

        img_ref = cv2.warpAffine(img_gray, T, (cols, rows))

        self.do_postprocess(img_ref, alpha)

    def perspective_transformation(self, perspective_pts):
        pts1 = np.array(perspective_pts).astype(np.float32)
        w1 = np.abs(pts1[1, 0] - pts1[0, 0])
        w2 = np.abs(pts1[2, 0] - pts1[3, 0])
        h1 = np.abs(pts1[2, 1] - pts1[0, 1])
        h2 = np.abs(pts1[3, 1] - pts1[1, 1])

        width = int(np.max([w1, w2]))
        height = int(np.max([h1, h2]))

        pts2 = np.array([
            [0., 0.], [width - 1, 0.],
            [0., height - 1], [width - 1, height - 1]
        ]).astype(np.float32)

        img_gray, alpha = self.get_gray_alpha()

        T = cv2.getPerspectiveTransform(pts1, pts2)
        img_per = cv2.warpPerspective(img_gray, T, (width, height))
        cv2.imshow('perspective', img_per)