import unittest

from first_pace import FirstPace


class TestFirstPace(unittest.TestCase):

    def test_to_string(self):

        try:
            p1 = FirstPace(minutes=10, seconds=2)
            self.assertEqual('0:10:02 min per mile', str(p1))
        except ValueError as ex:
            self.fail(str(ex))

        try:
            p2 = FirstPace(minutes=5, seconds=23, length_unit='km')
            self.assertEqual('0:05:23 min per km', str(p2))
        except ValueError as ex:
            self.fail(str(ex))

        try:
            p3 = FirstPace(minutes=7)
            self.assertEqual('0:07:00 min per mile', str(p3))
        except ValueError as ex:
            self.fail(str(ex))

        try:
            p4 = FirstPace(minutes=3, length_unit='lulu')
            self.fail('Should not get here with unit = lulu')
        except ValueError as ex:
            self.assertEqual('FirstPace.__init__ - "lulu" is not a valid length unit', str(ex))

    def test_from_string(self):

        try:
            p1 = FirstPace.from_string('0:06:23 min per mile')
            self.assertEqual('0:06:23 min per mile', str(p1))
        except ValueError as ex:
            self.fail(str(ex))
