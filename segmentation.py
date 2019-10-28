import cv2
import numpy as np


def segment_hand_with_background(picture):
    hsv_img = cv2.cvtColor(picture, cv2.COLOR_BGR2HSV)
    lower = (40, 60, 50)
    higher = (100, 255, 255)
    mask = cv2.inRange(hsv_img, lower, higher)
    masked = cv2.bitwise_and(hsv_img, hsv_img, mask=mask)

    binary_image = to_binary(masked)
    binary_image = change_binary_image_colors(binary_image)

    kernel = np.ones((5, 5), np.uint8)
    return rotate_while_not_aligned(morphology_filter(binary_image, kernel))


def segment_hand_with_skin(picture):
    # needs some improvement
    min_YCrCb = (0, 100, 50)
    max_YCrCb = (250, 180, 160)

    imageYCrCb = cv2.cvtColor(picture, cv2.COLOR_BGR2YCR_CB)
    skinRegionYCrCb = cv2.inRange(imageYCrCb, min_YCrCb, max_YCrCb)
    masked = cv2.bitwise_and(picture, picture, mask=skinRegionYCrCb)

    binary_image = to_binary(masked)
    kernel = np.ones((5, 5), np.uint8)
    return rotate_while_not_aligned(morphology_filter(binary_image, kernel))


def to_binary(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary_image = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    return binary_image


def morphology_filter(img, kernel):
    img = cv2.dilate(img, kernel)
    img = cv2.erode(img, kernel, iterations=2)
    return cv2.dilate(img, kernel)


def change_binary_image_colors(binary_image):
    h = binary_image.shape[0]
    w = binary_image.shape[1]
    # loop over the image, pixel by pixel
    for y in range(0, h):
        for x in range(0, w):
            # threshold the pixel
            if binary_image[y, x] == 255:
                binary_image[y, x] = 0
            else:
                binary_image[y, x] = 255
    return binary_image


def rotate_while_not_aligned(segmented):
    last_column = 0
    h = segmented.shape[0]
    w = segmented.shape[1]

    for y in range(0, h):
        if segmented[y, w - 1] == 255:
            last_column += 1

    while last_column < 50:
        last_column = 0
        segmented = np.rot90(segmented)
        h = segmented.shape[0]
        w = segmented.shape[1]
        cv2.imshow("rotated", segmented)
        for y in range(0, h):
            if segmented[y, w - 1] == 255:
                last_column += 1
    return segmented
