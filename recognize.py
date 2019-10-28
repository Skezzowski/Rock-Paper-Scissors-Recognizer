import cv2
import numpy as np

np.set_printoptions(threshold=np.inf)


def recognize(segmented):

    edges = cv2.Canny(segmented, 100, 200)
    cv2.imshow("edges", edges)

    h = edges.shape[0]
    w = edges.shape[1]
    edges_array = np.zeros(shape=(w,))

    for x in range(0, w):
        for y in range(0, h):
            if edges[y, x] == 255:
                edges_array[x] = edges_array[x] + 1
    fours = 0
    for x in range(0, w):
        if edges_array[x] == 4:
            fours += 1

    if fours > 50:
        return "scissors"
    else:
        return "i dunno yet"
