import cv2
import numpy as np


def skeleton_of_shape(img):
    thn = cv2.ximgproc.thinning(img, None, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)
    return thn


def skeleton_endpoints(skel):
    skel = skel.copy()
    skel[skel != 0] = 1
    skel = np.uint8(skel)

    kernel = np.uint8([[1,  1, 1],
                       [1, 10, 1],
                       [1,  1, 1]])
    src_depth = -1
    filtered = cv2.filter2D(skel, src_depth, kernel)

    out = np.zeros_like(skel)
    out[filtered >= 11] = 255
    out[filtered == 12] = 0
    cv2.imshow('out', out)

    out2 = out.copy()
    out2[out2 != 0] = 1
    kernel = np.uint8([[0, 1, 0],
                       [1, 10, 1],
                       [0, 1, 0]])
    filtered = cv2.filter2D(out2, src_depth, kernel)
    filtered[filtered > 12] = 255
    filtered[filtered == 10] = 255
    out = cv2.bitwise_and(out, filtered)

    out2 = out.copy()
    cv2.imshow('out2', out2)
    out2[out2 != 0] = 1
    kernel = np.uint8([[1, 0, 1],
                       [0, 10, 0],
                       [1, 0, 1]])
    filtered = cv2.filter2D(out2, src_depth, kernel)
    filtered[filtered == 10] = 255
    cv2.imshow('filtered', filtered)

    return out
    # return np.where(filtered==11) - végpontok koordinátái
