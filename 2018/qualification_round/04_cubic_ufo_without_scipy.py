import logging
import math
from itertools import starmap
from operator import mul

logging.basicConfig(level=logging.ERROR)
LOG = logging.getLogger(__name__)

# See https://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions
# For an explanation on rotation matrices


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
    # plane = np.array([[1, 0, 0], [0, 0, 1]])  # The xz-plane
    # projected_corners = np.dot(corners, plane.T)
    projected_points = points[:, [0, 2]]  # Simplify, since the plane is the xz-plane
    return projected_points


def hull_area_without_scipy(points):
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


def func_min(angles, corners, specified_area):
    # No need to rotate yaw, since we project onto y-plane and just ignore the z-coordinates
    rotated_corners = rotate_points(corners, angles[0], angles[1], 0)
    area = hull_area_without_scipy(project_points(rotated_corners))
    return abs(area - specified_area)


def main():
    corners = np.array([
        [-.5, -.5, -.5],
        [+.5, -.5, -.5],
        [+.5, +.5, -.5],
        [-.5, +.5, -.5],
        [-.5, -.5, +.5],
        [+.5, -.5, +.5],
        [+.5, +.5, +.5],
        [-.5, +.5, +.5],
    ])

    faces = np.array([
        [.5, 0, 0],
        [0, .5, 0],
        [0, 0, .5]
    ])

    # Initial guess for roll and pitch
    x0 = np.array([0, 0])
    # x0 = np.array([90/180*np.pi, 90/180*np.pi])

    # Read in the number of cases
    cases = getint()

    for case in range(1, cases + 1):
        # Read in the requested area
        requested_area = getfloat()

        # Run a numeric optimization to find roll and pitch
        result = scipy.optimize.minimize(func_min, x0, args=(corners, requested_area),
                                         method='Nelder-Mead', options={'ftol': 1e-14})
        roll, pitch = result.x

        # Rotate the faces with the same angles
        rotated_faces = rotate_points(faces, roll, pitch, 0)

        # Print resulting faces
        print("Case #{}:".format(case))
        for face in rotated_faces:
            print("{} {} {}".format(face[0], face[1], face[2]))


if __name__ == '__main__':
    main()


