import cv2
import numpy as np
import math
import skeleton as sk

np.set_printoptions(threshold=np.inf)


def recognize(segmented, main_points, skeleton):
    edges = cv2.Canny(segmented, 100, 200)

    if check_if_scissors(edges):
        return "scissors"

    coordinates = points_to_coordinates(main_points)

    print(check_if_paper(skeleton))

    return "dunno"


def check_if_paper(skeleton):
    w = skeleton.shape[1]
    h = skeleton.shape[0]
    endpoint_coordinates = points_to_coordinates(sk.endpoints(skeleton))
    innerpoint_coordinates = points_to_coordinates(sk.inner_nodes(skeleton))
    distence_between_firstandlast = calculate_distance(endpoint_coordinates[0],
                                                       endpoint_coordinates[len(endpoint_coordinates)-1])
    print(distence_between_firstandlast)
    if len(endpoint_coordinates) == 2:
        skeleton_length = 0
        for x in range(0, w):
            for y in range(0, h):
                if skeleton[y, x] == 255:
                    skeleton_length = skeleton_length + 1
        print(skeleton_length)
        if distence_between_firstandlast < skeleton_length < distence_between_firstandlast + 15:
            return "paper"

    print(innerpoint_coordinates)
    print(endpoint_coordinates)


def calculate_distance(a, b):
    return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)


def check_if_scissors(edges):
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

    return fours > 50


def points_to_coordinates(points):
    h = points.shape[0]
    w = points.shape[1]
    coordinates = []

    for x in range(0, w):
        for y in range(0, h):
            if points[y, x] == 255:
                coordinates.append(Point(x, y))
    return coordinates


class Point:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "x: " + str(self.x) + ", y: " + str(self.y)

    def __repr__(self):
        return "[x: " + str(self.x) + " y: " + str(self.y) + "]"
