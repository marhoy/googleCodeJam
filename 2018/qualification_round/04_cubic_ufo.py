import logging
import numpy as np
import scipy.spatial
import scipy.optimize

logging.basicConfig(level=logging.ERROR)
LOG = logging.getLogger(__name__)

# See https://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions
# For an explanation on rotation matrices


def getint():
    return int(input())


def getfloat():
    return float(input())


def roll_matrix(angle):
    # Rotation around x-axis
    R = np.array([
        [1, 0, 0],
        [0, np.cos(angle), -np.sin(angle)],
        [0, np.sin(angle), np.cos(angle)]
    ])
    return R


def pitch_matrix(angle):
    # Rotation around y-axis
    R = np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [0, 1, 0],
        [-np.sin(angle), 0, np.cos(angle)]
    ])
    return R


def yaw_matrix(angle):
    # Rotation around z-axis
    R = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])
    return R


def rotation_matrix(roll, pitch, yaw):
    R = np.dot(np.dot(yaw_matrix(yaw), pitch_matrix(pitch)), roll_matrix(roll))
    return R


def rotate_points(points, roll, pitch, yaw):
    R = rotation_matrix(roll, pitch, yaw)
    rotated_points = np.dot(points, R)
    return rotated_points


def project_points(points):
    # plane = np.array([[1, 0, 0], [0, 0, 1]])  # The xz-plane
    # projected_corners = np.dot(corners, plane.T)
    projected_points = points[:, [0, 2]]  # Simplify, since the plane is the xz-plane
    return projected_points


def hull_area(points):
    # Find area of convex hull
    hull = scipy.spatial.ConvexHull(points)
    return hull.volume


def func_min(angles, corners, specified_area):
    # No need to rotate yaw, since we project onto y-plane and just ignore the z-coordinates
    rotated_corners = rotate_points(corners, angles[0], angles[1], 0)
    area = hull_area(project_points(rotated_corners))
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


