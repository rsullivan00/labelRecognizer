import unittest
import numpy as np
from contours import corners, get_angle


class ContoursTest(unittest.TestCase):
    corners_tests = (
        (
            np.array([(0, 0), (1, 0), (1, 1), (0, 1)]),
            ((0, 0), (1, 0), (1, 1), (0, 1))
        ),
        (
            np.array([(1, 0), (1, 1), (0, 1), (0, 0)]),
            ((0, 0), (1, 0), (1, 1), (0, 1))
        )
    )

    def test_corners(self):
        for in_corners, out_corners in self.corners_tests:
            result = corners(in_corners)
            self.assertTrue((out_corners == result).all())

    get_angle_tests = (
        (6, -90),
        (8, 90),
        (3, 180),
        (1, 0)
    )

    def test_get_angle(self):
        for orientation, e_angle in self.get_angle_tests:
            result = get_angle(orientation)
            self.assertEqual(e_angle, result)

if __name__ == '__main__':
    unittest.main()
