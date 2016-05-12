import unittest

from data_classes import Frame, Press
from classify import detect_frame_type, detect_press_type


class TestFrameExpertSys(unittest.TestCase):
    """
    Test frame expert system to detect classes on corner-cases
    """
    def test_circle(self):
        pass

    def test_point(self):
        pass

    def test_line(self):
        str1 = "    44    110    108    255    255    255    112     49    255" \
               "    255    255    101     67    255    255    255     28     83     66 "
        missed_high_press = Frame(list(map(int, str1.strip().split())))
        self.assertEqual(detect_frame_type(missed_high_press), 1)

        str2 = "    72    183    185    255    255    255    191     83    255" \
               "    255    255    167    120    255    255    255     50    150    106 "
        missed_high_press_2 = Frame(list(map(int, str2.strip().split())))
        self.assertEqual(detect_frame_type(missed_high_press_2), 1)

        str3 = "    29     87     84    255    255    224     88     32    255" \
               "    255    255     82     44    255    255    255     18     57     43 "
        missed_high_press_3 = Frame(list(map(int, str3.strip().split())))
        self.assertEqual(detect_frame_type(missed_high_press_3), 1)

        str4 = "   156     65    101     67    255    255     99     30    197" \
               "    255    255     81     65    255    255    255     28     87     93 "
        missed_high_press_4 = Frame(list(map(int, str4.strip().split())))
        self.assertEqual(detect_frame_type(missed_high_press_4), 1)

        str5 = "    11     27     56     24     79    255     35     21     54" \
               "    255     95     14     22    255     73     18     16     24      8 "
        strict_high_press = Frame(list(map(int, str5.strip().split())))
        self.assertEqual(detect_frame_type(strict_high_press), 1)

        str6 = "    50     54     23    255    255    227     28     57    212" \
               "    255    255     19     73    168    153    177     36     50     16 "
        strict_high_press_2 = Frame(list(map(int, str6.strip().split())))
        self.assertEqual(detect_frame_type(strict_high_press_2), 1)

        str7 = "    14     23     21     25     80     86     45     20    109" \
               "    255    255     42    176    135     93     29      9     21     12 "
        strict_high_press_3 = Frame(list(map(int, str7.strip().split())))
        self.assertEqual(detect_frame_type(strict_high_press_3), 1)





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
