import unittest

from first_time import FirstTime


class TestFirstTime(unittest.TestCase):

    def test_to_string(self):

        try:
            t1 = FirstTime(hours=2, minutes=15, seconds=12)
            self.assertEqual('2:15:12', str(t1))
        except ValueError as ex:
            self.fail('Should not fail')

        try:
            t2 = FirstTime()
            self.assertEqual('0:00:00', str(t2))
        except ValueError:
            self.fail('Should not fail')

        try:
            t3 = FirstTime(minutes=-2, seconds=120)
            self.fail('FirstTime should not accept negative values')
        except ValueError as ex:
            self.assertEqual('FirstTime.__init__ - does not allow negative values', str(ex))

    def test_from_string(self):

        try:
            t1 = FirstTime.from_string('2:03:23')
            self.assertEqual('2:03:23', str(t1))
        except ValueError:
            self.fail('test_from_string hould not fail for valid string')

        try:
            t2 = FirstTime.from_string('abc')
            self.fail('FirstTime is expected to fail with "abc"')
        except ValueError as ex:
            self.assertEqual('FirstTime.from_string - unknown string format - "abc"', str(ex))

        try:
            t3 = FirstTime.from_string('3:45')
            self.assertEqual('3:45:00', str(t3))
        except ValueError:
            self.fail('test_from_string should not fail for valid string')

        try:
            t4 = FirstTime.from_string('3')
            self.fail('test_from_string should not pass for "3"')
        except ValueError as ex:
            self.assertEqual('FirstTime.from_string - unknown string format for "3"', str(ex))

        try:
            t5 = FirstTime.from_string('4/15/2015')
            self.assertEqual('test_from_string should not pass for "4/15/2015"')
        except ValueError as ex:
            self.assertEqual('FirstTime.from_string - unknown string format for "4/15/2015"', str(ex))

if __name__ == '__main__':
    unittest.main()
