import unittest

from first_pace import FirstPace


class TestFirstPace(unittest.TestCase):

    def test_to_string(self):

        try:
            pace = FirstPace(minutes=10, seconds=2)
            self.assertEqual('0:10:02 min per mile', str(pace))
        except ValueError as ex:
            self.fail(str(ex))

        try:
            pace = FirstPace(minutes=5, seconds=23, length_unit='km')
            self.assertEqual('0:05:23 min per km', str(pace))
        except ValueError as ex:
            self.fail(str(ex))

        try:
            pace = FirstPace(minutes=7)
            self.assertEqual('0:07:00 min per mile', str(pace))
        except ValueError as ex:
            self.fail(str(ex))

        try:
            _ = FirstPace(minutes=3, length_unit='lulu')
            self.fail('Should not get here with unit = lulu')
        except ValueError as ex:
            self.assertEqual('"lulu" is not a valid length unit', str(ex))

    def test_from_string(self):

        try:
            pace = FirstPace.from_string(str_input='0:06:23 min per mile')
            self.assertEqual('0:06:23 min per mile', str(pace))
            cmp_json = {'length_unit': 'mile',
                        'pace': '0:06:23 min per mile',
                        'time': {'seconds': 383, 'time': '0:06:23'}}
            self.assertEqual(cmp_json, pace.to_json())
            cmp_json = {'length_unit': 'km',
                        'pace': '0:03:58 min per km',
                        'time': {'seconds': 238, 'time': '0:03:58'}}
            self.assertEqual(cmp_json, pace.to_json(output_unit='km'))
            cmp_html = '0:06:23 min per mile'
            self.assertEqual(cmp_html, pace.to_html())
            cmp_html = '0:03:58 min per km'
            self.assertEqual(cmp_html, pace.to_html(output_unit='km'))

        except ValueError as ex:
            self.fail(str(ex))

        try:
            _ = FirstPace.from_string('0:06:23 min per lulu')
            self.fail('Should not get here with unit = lulu')
        except ValueError as ex:
            self.assertEqual('"lulu" is not a valid length unit', str(ex))
