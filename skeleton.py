import cv2
import numpy as np


def skeleton_of_shape(img):
    thn = cv2.ximgproc.thinning(img, None, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)
    return thn


def endpoints(img):
    skel = img.copy()
    skel[skel != 0] = 1
    skel = np.uint8(skel)

    kernel = np.uint8([[1, 1, 1],
                       [1, 10, 1],
                       [1, 1, 1]])
    src_depth = -1
    filtered = cv2.filter2D(skel, src_depth, kernel)

    out = np.zeros_like(skel)
    out[filtered == 11] = 255

    cv2.imshow('out', out)
    return out


def inner_nodes(img):
    skel = img.copy()
    skel[skel != 0] = 1
    skel = np.uint8(skel)

    kernel = np.uint8([[1, 5, 0],
                       [0, 10, 0],
                       [1, 5, 0]])
    src_depth = -1
    filtered = cv2.filter2D(skel, src_depth, kernel)

    out = np.zeros_like(skel)
    out[filtered == 12] = 255
    out[filtered == 17] = 255
    out[filtered == 22] = 255

    cv2.imshow('out2', out)
    return out


def skeleton_nodes(skel):
    skel = skel.copy()
    skel[skel != 0] = 1
    skel = np.uint8(skel)

    end = endpoints(skel)
    inner = inner_nodes(skel)
    res = cv2.bitwise_or(end, inner)

    return res
    # return np.where(filtered==11) - végpontok koordinátái
