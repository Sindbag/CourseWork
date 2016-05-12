import unittest

from data_classes import Frame, Press
from classify import detect_frame_type, detect_press_type


class TestFrameExpertSys(unittest.TestCase):
    """
    Test frame expert system to detect classes on corner-cases
    """
    def test_circle(self):
        # self.assertEqual(a, b)
        pass

    def test_point(self):
        pass

    def test_line(self):
        pass


class TestPressExpertSys(unittest.TestCase):
    """
    Test press expert system to detect classes on corner-cases
    """

    def test_circle(self):
        pass

    def test_point(self):
        pass

    def test_line(self):
        pass


if __name__ == "__main__":
    unittest.main()
