import unittest

from first_time import FirstTime


class TestFirstTime(unittest.TestCase):

    def test_to_string(self):

        try:
            time = FirstTime(hours=2, minutes=15, seconds=12)
            self.assertEqual('2:15:12', str(time))
        except ValueError as ex:
            self.fail(str(ex))

        try:
            time = FirstTime()
            self.assertEqual('0:00:00', str(time))
        except ValueError:
            self.fail('Should not fail')

        try:
            _ = FirstTime(minutes=-2, seconds=120)
            self.fail('FirstTime should not accept negative values')
        except ValueError as ex:
            self.assertEqual('negative values are invalid', str(ex))

    def test_from_string(self):

        try:
            time = FirstTime.from_string(string='2:03:23')
            self.assertEqual('2:03:23', str(time))
        except ValueError:
            self.fail('test_from_string should not fail for valid string')

        try:
            _ = FirstTime.from_string(string='abc')
            self.fail('FirstTime is expected to fail with "abc"')
        except ValueError as ex:
            self.assertEqual('(\'Unknown string format:\', \'abc\')', str(ex))

        try:
            time = FirstTime.from_string(string='3:45')
            self.assertEqual('3:45:00', str(time))
        except ValueError:
            self.fail('test_from_string should not fail for valid string')

        try:
            _ = FirstTime.from_string(string='3')
            self.fail('test_from_string should not pass for "3"')
        except ValueError as ex:
            self.assertEqual('unknown string format for "3"', str(ex))

        try:
            time = FirstTime.from_string(string='4/15/2015')
            self.assertEqual('test_from_string should not pass for "4/15/2015"', time)
        except ValueError as ex:
            self.assertEqual('unknown string format for "4/15/2015"', str(ex))


if __name__ == '__main__':
    unittest.main()
