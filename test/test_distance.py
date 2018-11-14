import unittest

from first_distance import FirstDistance


class TestFirstDistance(unittest.TestCase):

    def test_to_string(self):

        try:
            d1 = FirstDistance(distance=300, unit='mm')
            self.fail('FirstDistance is expected to fail for wrong length unit')
        except ValueError as ex:
            self.assertEqual('FirstDistance.__init__ - "mm" is not a valid unit', str(ex))

        try:
            d1 = FirstDistance(distance=-300, unit='m')
            self.fail('FirstDistance is expected to fail for negative length')
        except ValueError as ex:
            self.assertEqual('FirstDistance.__init__ - -300 is not a positive number', str(ex))

        try:
            d1 = FirstDistance(distance=300, unit='m')
            self.assertEqual('300 m', str(d1))
        except ValueError as ex:
            self.fail(ex)

        try:
            d1 = FirstDistance(distance=5, unit='km')
            self.assertEqual('5 km', str(d1))
        except ValueError as ex:
            self.fail(ex)

        try:
            d1 = FirstDistance(distance=26.2, unit='mile')
            self.assertEqual('26.2 mile', str(d1))
        except ValueError as ex:
            self.fail(ex)

        try:
            d1 = FirstDistance(distance=5280, unit='ft')
            self.assertEqual('5280 ft', str(d1))
        except ValueError as ex:
            self.fail(ex)

    def test_convert_to(self):

        try:
            d1 = FirstDistance(distance=5, unit='km')
        except ValueError as ex:
            self.fail(ex)

        try:
            result = d1.convert_to(unit='mm')
            self.fail('convert_to is expected to fail with unknown unit')
        except ValueError as ex:
            self.assertEqual('FirstDistance.convert_to - mm is not a valid unit', str(ex))

        try:
            result = d1.convert_to(unit='km')
            self.assertEqual(5, result)
        except ValueError as ex:
            self.fail(ex)

        try:
            result = d1.convert_to(unit='m')
            self.assertEqual(5000, result)
        except ValueError as ex:
            self.fail(ex)

        try:
            result = d1.convert_to(unit='ft')
            self.assertEqual('16404.20', '{:.2f}'.format(result))
        except ValueError as ex:
            self.fail(ex)

        try:
            result = d1.convert_to(unit='mile')
            self.assertEqual('3.11', '{:.2f}'.format(result))
        except ValueError as ex:
            self.fail(ex)

    def test_from_string(self):

        try:
            d1 = FirstDistance.from_string('1 mile')
            self.assertEqual('1.0 mile', str(d1))
        except ValueError as ex:
            self.fail(ex)

        try:
            d2 = FirstDistance.from_string('onlyonetoken')
            self.fail('from_string is expected to fail with only one token')
        except ValueError as ex:
            self.assertEqual('FirstDistance.from_string - from_string() ' +
                             'expects 2 tokens, number and unit, but got "onlyonetoken"', str(ex))

        try:
            d3 = FirstDistance.from_string('34t papa')
            self.fail('from_string is expected to fail if the first token is not a number')
        except ValueError as ex:
            message = ('FirstDistance.from_string - ' +
                       'expects the first token to be a number but invalid literal for float(): 34t')
            self.assertEqual(message, str(ex))

        try:
            d4 = FirstDistance.from_string('-35.2 papa')
            self.fail('FirstDistance is expected to fail if the number is negative')
        except ValueError as ex:
            self.assertEqual('FirstDistance.__init__ - -35.2 is not a positive number', str(ex))

        try:
            d5 = FirstDistance.from_string('42.2 papa')
            self.fail('FirstDistance is expected to fail for invalid unit')
        except ValueError as ex:
            self.assertEqual('FirstDistance.__init__ - "papa" is not a valid unit', str(ex))


if __name__ == '__main__':
    unittest.main()
