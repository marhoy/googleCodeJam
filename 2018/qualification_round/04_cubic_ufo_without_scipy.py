import logging
import math
from itertools import starmap
from operator import mul

logging.basicConfig(level=logging.ERROR)
LOG = logging.getLogger(__name__)

# See https://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions
# For an explanation on rotation matrices

ordered_corners = [
    [-.5, +.5, -.5],
    [+.5, +.5, -.5],
    [+.5, +.5, +.5],
    [+.5, -.5, +.5],
    [-.5, -.5, +.5],
    [-.5, -.5, -.5],
    [+.5, -.5, -.5],
    [-.5, +.5, +.5],
]

faces = [
    [.5, 0, 0],
    [0, .5, 0],
    [0, 0, .5]
]


def getint():
    return int(input())


def getfloat():
    return float(input())


def matrix_mul(A, B):
    return [[sum(starmap(mul, zip(row, col))) for col in zip(*B)] for row in A]


def roll_matrix(angle):
    R = [
        [1, 0, 0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ]
    return R


def pitch_matrix(angle):
    R = [
        [math.cos(angle), 0, math.sin(angle)],
        [0, 1, 0],
        [-math.sin(angle), 0, math.cos(angle)]
    ]
    return R


def yaw_matrix(angle):
    R = [
        [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ]
    return R


def rotation_matrix(roll, pitch, yaw):
    R = matrix_mul(matrix_mul(yaw_matrix(yaw), pitch_matrix(pitch)), roll_matrix(roll))
    return R


def rotate_points(points, roll, pitch, yaw):
    R = rotation_matrix(roll, pitch, yaw)
    rotated_points = matrix_mul(points, R)
    return rotated_points


def project_points(points):
    plane = [[1, 0], [0, 0], [0, 1]]  # The x- and z- unit vector, transposed
    projected_points = matrix_mul(points, plane)
    # projected_points = points[:, [0, 2]]  # Simplify, since the plane is the xz-plane
    return projected_points


def hull_area(points):
    # This only works for a simple polygon where the points are ordered nicely
    # https://en.wikipedia.org/wiki/Shoelace_formula
    n = len(points)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    area = abs(area) / 2.0
    return area


def get_area(angle):
    points = project_points(rotate_points(ordered_corners, angle, 0, 45 / 180 * math.pi))
    return hull_area(points[:6])


def binary_search(specified_area):
    area_resolution = 1e-10
    max_guesses = 100
    left = .5 * math.atan(2 * math.sqrt(2))
    right = .5 * math.pi
    angle_resolution = (right - left) / 10

    for guess in range(max_guesses):
        middle = (left + right) / 2
        area = get_area(middle)

        if abs(area - specified_area) < area_resolution:
            break
        elif area < specified_area:
            # Need to move the right boundary
            while (get_area(middle - angle_resolution) > specified_area) or ((middle - angle_resolution) < left):
                # Moving middle with resolution would take us to the other side of the optimum.
                angle_resolution = angle_resolution / 10
            right = middle - angle_resolution
        elif area > specified_area:
            # Need to move the left boundary
            while (get_area(middle + angle_resolution) < specified_area) or ((middle + angle_resolution) > right):
                # Moving middle with resolution would take us to the other side of the optimum.
                angle_resolution = angle_resolution / 10
            left = middle + angle_resolution
    else:
        LOG.error("Didn't find solution with requested presicion, after %d iterations", guess)

    return middle


def main():
    # Read in the number of cases
    cases = getint()

    for case in range(1, cases + 1):
        # Read in the requested area
        requested_area = getfloat()

        # Find the roll-angle that gives this area
        # Keep pitch = 0 and yaw = 45
        roll_angle = binary_search(requested_area)

        # Rotate the faces with the same angles
        rotated_faces = rotate_points(faces, roll_angle, 0, 45/180*math.pi)

        # Print resulting faces
        print("Case #{}:".format(case))
        for face in rotated_faces:
            print("{} {} {}".format(face[0], face[1], face[2]))


if __name__ == '__main__':
    main()


