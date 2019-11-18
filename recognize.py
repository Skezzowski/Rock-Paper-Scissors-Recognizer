import cv2
import numpy as np
import math
import skeleton as sk

np.set_printoptions(threshold=np.inf)


def recognize(segmented, skeleton):
    edges = cv2.Canny(segmented, 100, 200)

    if check_if_scissors(edges):
        return "scissors"

    chance_of_paper = check_if_paper(skeleton)
    chance_of_rock = check_if_rock(skeleton)
    print("Chance of paper: " + str(chance_of_paper))
    print("Chance of rock: " + str(chance_of_rock))
    if chance_of_paper > 0 or chance_of_rock > 0:
        if chance_of_rock > chance_of_paper:
            return "rock"
        else:
            return "paper"
    return "dunno"


def check_if_paper(skeleton):
    w = skeleton.shape[1]
    h = skeleton.shape[0]
    endpoint_coordinates = points_to_coordinates(sk.endpoints(skeleton))
    innerpoint_coordinates = points_to_coordinates(sk.inner_nodes(skeleton))
    distence_between_firstandlast = calculate_distance(endpoint_coordinates[0],
                                                       endpoint_coordinates[len(endpoint_coordinates)-1])
    skeleton_array = np.zeros(shape=(h,))

    for y in range(0, h):
        for x in range(0, w):
            if skeleton[y, x] == 255:
                skeleton_array[y] = skeleton_array[y] + 1

    chance_of_paper = 0
    ## ha csak egy egyenes az egész valószínűleg papír
    if len(endpoint_coordinates) == 2:
        skeleton_length = 0
        for x in range(0, w):
            for y in range(0, h):
                if skeleton[y, x] == 255:
                    skeleton_length = skeleton_length + 1

        if distence_between_firstandlast < skeleton_length < distence_between_firstandlast + 15:
            chance_of_paper = 50

    ## a legbalodalibb csúcs és a második között nagy távolság van
    if endpoint_coordinates[1].x - endpoint_coordinates[0].x > 70 and len(endpoint_coordinates) > 2:
        chance_of_paper = chance_of_paper + 20

    ## Végpontok es inner pontok elhelyezkedésének vizsgálata
    k = 0
    i = 1
    close_endpoints_number = 0
    while i < len(endpoint_coordinates) and endpoint_coordinates[i].x - endpoint_coordinates[k].x < 40:
        k = k+1
        i = i+1
        close_endpoints_number = close_endpoints_number + 1

    if close_endpoints_number == 1 and len(innerpoint_coordinates) > 0:

        if innerpoint_coordinates[0].x - endpoint_coordinates[0].x > 40:
            chance_of_paper = chance_of_paper + 12
        if innerpoint_coordinates[0].x - endpoint_coordinates[1].x > 40:
            chance_of_paper = chance_of_paper + 12

    if close_endpoints_number == 2 and len(innerpoint_coordinates) > 0:
        if innerpoint_coordinates[0].x - endpoint_coordinates[0].x > 40 \
                or innerpoint_coordinates[0].x - endpoint_coordinates[1].x > 40 \
                or innerpoint_coordinates[0].x - endpoint_coordinates[2].x > 40:
            chance_of_paper = chance_of_paper + 25

        if innerpoint_coordinates[1].x - endpoint_coordinates[0].x > 40 \
                or innerpoint_coordinates[1].x - endpoint_coordinates[1].x > 40 \
                or innerpoint_coordinates[1].x - endpoint_coordinates[2].x > 40:
            chance_of_paper = chance_of_paper + 25

    return chance_of_paper


def check_if_rock(skeleton):
    w = skeleton.shape[1]
    h = skeleton.shape[0]
    skeleton_array = np.zeros(shape=(h,))
    skeleton_coordinates = []
    endpoint_coordinates = points_to_coordinates(sk.endpoints(skeleton))
    innerpoint_coordinates = points_to_coordinates(sk.inner_nodes(skeleton))

    chance_of_rock = 0

    for y in range(0, h):
        for x in range(0, w):
            if skeleton[y, x] == 255:
                skeleton_array[y] = skeleton_array[y] + 1
                skeleton_coordinates.append(Point(x,y))
                break

    max_x_distence = 0
    for i in range(0, len(skeleton_coordinates)):
        if i < len(skeleton_coordinates) - 1:
            temp_distence = math.fabs(skeleton_coordinates[i].x - skeleton_coordinates[i+1].x)
            if temp_distence > max_x_distence:
                max_x_distence = temp_distence

    ## kicsi marad a távolság egyes pontok között x tengelyen, és csontváz elnyúlik az y tengelyen
    if max_x_distence < 60 and skeleton_coordinates[len(skeleton_coordinates)-1].y - skeleton_coordinates[0].y > 40:
        chance_of_rock = chance_of_rock + 25


    ## Végpontok es inner pontok elhelyezkedésének vizsgálata
    k = 0
    i = 1
    close_endpoints_number = 0
    while i < len(endpoint_coordinates) and endpoint_coordinates[i].x - endpoint_coordinates[k].x < 40:
        k = k + 1
        i = i + 1
        close_endpoints_number = close_endpoints_number + 1

    if close_endpoints_number == 1 and len(innerpoint_coordinates) > 0:
        if innerpoint_coordinates[0].x - endpoint_coordinates[0].x < 40:
            chance_of_rock = chance_of_rock + 12
        if innerpoint_coordinates[0].x - endpoint_coordinates[1].x < 40:
            chance_of_rock = chance_of_rock + 12

    if close_endpoints_number == 2 and len(innerpoint_coordinates) > 0:
        if innerpoint_coordinates[0].x - endpoint_coordinates[0].x < 40 \
                and innerpoint_coordinates[0].x - endpoint_coordinates[1].x < 40 \
                and innerpoint_coordinates[0].x - endpoint_coordinates[2].x < 40:
            chance_of_rock = chance_of_rock + 12
        if innerpoint_coordinates[1].x - endpoint_coordinates[0].x < 40 \
                and innerpoint_coordinates[1].x - endpoint_coordinates[1].x < 40 \
                and innerpoint_coordinates[1].x - endpoint_coordinates[2].x < 40:
            chance_of_rock = chance_of_rock + 12

    if close_endpoints_number > 0 and len(innerpoint_coordinates) == 0:
        chance_of_rock = chance_of_rock + 12

    return chance_of_rock


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


def calculate_distance(a, b):
    return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)


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
