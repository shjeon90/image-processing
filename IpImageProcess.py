import cv2
import qimage2ndarray
from utils import *
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPixmap, QPainter
from IpShape import *

class IpImageProcess:
    def __init__(self, *args, **kwargs):
        self.parent = args[0]

    def clear(self):
        self.parent.clear()
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

    def do_postprocess_mark(self, coords):
        for coord in coords:
            ellipse = IpEllipse()
            ellipse.init(QPoint(coord[0]-5, coord[1]-5))
            ellipse.update(QPoint(coord[0]+5, coord[1]+5))

            self.parent.shape_list.append(ellipse)
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

    def harris_corner_detect(self):
        img_gray, alpha = self.get_gray_alpha()

        corners = cv2.cornerHarris(img_gray, 2, ksize=7, k=0.04)    # ksize gets bigger when the image is big.
        coords = np.where(corners > 0.1 * corners.max())
        coords = np.stack((coords[1], coords[0]), -1).astype(np.int32)

        self.do_postprocess_mark(coords)

    def fast_feature_detect(self):
        img_gray, alpha = self.get_gray_alpha()

        fast = cv2.FastFeatureDetector_create(50)   # threshold
        keypoints = fast.detect(img_gray, None)
        if len(keypoints) > 0:
            coords = np.stack([kp.pt for kp in keypoints], 0).astype(np.int32)

            self.do_postprocess_mark(coords)

    def blob_detect(self):
        img_gray, alpha = self.get_gray_alpha()

        # when we need to set parameters
        # https://blog.knowblesse.com/34
        blob = cv2.SimpleBlobDetector_create()
        keypoints = blob.detect(img_gray)
        if len(keypoints) > 0:
            coords = np.stack([kp.pt for kp in keypoints], 0).astype(np.int32)

            self.do_postprocess_mark(coords)

    def orb_descriptor(self):
        img_gray, alpha = self.get_gray_alpha()

        orb = cv2.ORB_create()
        keypoints, descriptors = orb.detectAndCompute(img_gray, None)
        if len(keypoints) > 0:
            coords = np.stack([kp.pt for kp in keypoints], 0).astype(np.int32)

            self.do_postprocess_mark(coords)

    def feature_match(self, img_temp):
        img_gray, alpha = self.get_gray_alpha()

        detector = cv2.ORB_create()
        kp1, desc1 = detector.detectAndCompute(img_temp, None)
        kp2, desc2 = detector.detectAndCompute(img_gray, None)

        if len(kp1) > 0 and len(kp2) > 0:

            matcher = cv2.BFMatcher(cv2.NORM_HAMMING2)
            matches = matcher.knnMatch(desc1, desc2, 2)

            ratio = 0.75
            good_matches = [first for first, second in matches if first.distance < second.distance * ratio]

            src_pts = np.array([kp1[m.queryIdx].pt for m in good_matches]).astype(np.float32)
            dst_pts = np.array([kp2[m.trainIdx].pt for m in good_matches]).astype(np.float32)
            T, mask = cv2.findHomography(src_pts, dst_pts)
            h, w = img_temp.shape[:2]
            pts = np.float32([[[0, 0]], [[0, h - 1]], [[w - 1, h - 1]], [[w - 1, 0]]])
            dst = cv2.perspectiveTransform(pts, T)
            img_gray = cv2.polylines(img_gray, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
            res = cv2.drawMatches(img_temp, kp1, img_gray, kp2, good_matches, None,
                                       flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

            cv2.imshow('Feature Match + Homography', res)