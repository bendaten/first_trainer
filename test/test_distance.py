import unittest

from first_distance import FirstDistance


class TestFirstDistance(unittest.TestCase):

    def test_to_string(self):

        try:
            _ = FirstDistance(distance=300, unit='mm')
            self.fail('FirstDistance is expected to fail for wrong length unit')
        except ValueError as ex:
            self.assertEqual('"mm" is not a valid unit', str(ex))

        try:
            _ = FirstDistance(distance=-300, unit='m')
            self.fail('FirstDistance is expected to fail for negative length')
        except ValueError as ex:
            self.assertEqual('-300 is not a positive number', str(ex))

        try:
            distance = FirstDistance(distance=300, unit='m')
            self.assertEqual('300 m', str(distance))
        except ValueError as ex:
            self.fail(ex)

        try:
            distance = FirstDistance(distance=5, unit='km')
            self.assertEqual('5 km', str(distance))
        except ValueError as ex:
            self.fail(ex)

        try:
            distance = FirstDistance(distance=26.2, unit='mile')
            self.assertEqual('26.2 mile', str(distance))
        except ValueError as ex:
            self.fail(ex)

        try:
            distance = FirstDistance(distance=5280, unit='ft')
            self.assertEqual('5280 ft', str(distance))
        except ValueError as ex:
            self.fail(ex)

    def test_convert_to(self):

        try:
            distance = FirstDistance(distance=5, unit='km')
        except ValueError as ex:
            self.fail(ex)

        try:
            _ = distance.convert_to(unit='mm')
            self.fail('convert_to is expected to fail with unknown unit')
        except ValueError as ex:
            self.assertEqual('mm is not a valid unit', str(ex))

        try:
            result = distance.convert_to(unit='km')
            self.assertEqual(5, result)
        except ValueError as ex:
            self.fail(ex)

        try:
            result = distance.convert_to(unit='m')
            self.assertEqual(5000, result)
        except ValueError as ex:
            self.fail(ex)

        try:
            result = distance.convert_to(unit='ft')
            self.assertEqual('16404.20', '{:.2f}'.format(result))
        except ValueError as ex:
            self.fail(ex)

        try:
            result = distance.convert_to(unit='mile')
            self.assertEqual('3.11', '{:.2f}'.format(result))
        except ValueError as ex:
            self.fail(ex)

    def test_from_string(self):

        try:
            distance = FirstDistance.from_string(string='1 mile')
            self.assertEqual('1.0 mile', str(distance))
        except ValueError as ex:
            self.fail(ex)

        try:
            _ = FirstDistance.from_string('onlyonetoken')
            self.fail('from_string is expected to fail with only one token')
        except ValueError as ex:
            self.assertEqual('2 tokens are expected, number and unit, but got "onlyonetoken"', str(ex))

        try:
            _ = FirstDistance.from_string('34t papa')
            self.fail('from_string is expected to fail if the first token is not a number')
        except ValueError as ex:
            message = 'first token is expected to be a number but could not convert string to float: \'34t\''
            self.assertEqual(message, str(ex))

        try:
            _ = FirstDistance.from_string('-35.2 papa')
            self.fail('FirstDistance is expected to fail if the number is negative')
        except ValueError as ex:
            self.assertEqual('-35.2 is not a positive number', str(ex))

        try:
            _ = FirstDistance.from_string('42.2 papa')
            self.fail('FirstDistance is expected to fail for invalid unit')
        except ValueError as ex:
            self.assertEqual('"papa" is not a valid unit', str(ex))

    def test_json(self):
        try:
            distance = FirstDistance.from_string(string='1 mile')
            self.assertEqual({'distance': 1.0, 'unit': 'mile'}, distance.to_json())
            self.assertEqual({'distance': 1.609344, 'unit': 'km'}, distance.to_json(output_unit='km'))
        except ValueError as ex:
            self.fail(ex)


if __name__ == '__main__':
    unittest.main()
