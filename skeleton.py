import cv2


def skeleton_of_shape(img):
    thn = cv2.ximgproc.thinning(img, None, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)
    return thn
