import unittest
from datetime import date

from first_distance import FirstDistance
from first_race import FirstRaceType, FirstRace
from first_time import FirstTime
from first_utils import FirstUtils


class TestFirstRaceType(unittest.TestCase):

    def test_to_string(self):

        try:
            race_type = FirstRaceType(name='marathon', distance=FirstDistance.from_string('26.219 mile'))
            self.assertEqual('marathon - 26.219 mile', str(race_type))
        except ValueError as ex:
            self.fail(str(ex))

    def test_to_json(self):

        try:
            race_type = FirstRaceType(name='marathon', distance=FirstDistance.from_string('26.219 mile'))
            self.assertEqual({'distance': {'distance': 26.219, 'unit': 'mile'}, 'name': 'marathon'}, race_type.to_json())
            self.assertEqual({'distance': {'distance': 42.195390336, 'unit': 'km'}, 'name': 'marathon'},
                             race_type.to_json(output_unit='km'))
        except ValueError as ex:
            self.fail(str(ex))


class TestFirstRace(unittest.TestCase):

    def test_to_string(self):

        rt1 = FirstRaceType(name='5K', distance=FirstDistance.from_string('5.0 km'))
        rd1 = date(year=2017, month=7, day=29)
        tt1 = FirstTime.from_string(string='0:25:30')
        tt2 = FirstTime.from_string(string='0:24:34')

        try:  # positive
            race = FirstRace(race_type=rt1, race_date=rd1, name='Martial Cottle Park 5K', target_time=tt1)
            cmp_string = ('Martial Cottle Park 5K of type ' + str(rt1) + '\n' +
                          'On ' + str(rd1) + '\n' + 'Target time - ' + str(tt1) + '\n' + 'Status - scheduled\n')
            self.assertEqual(cmp_string, str(race))
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        try:  # add actual time
            race.set_status(status='done')
            race.set_actual_time(a_time=tt2)
            cmp_string = ('Martial Cottle Park 5K of type ' + str(rt1) + '\n' +
                          'On ' + str(rd1) + '\n' + 'Target time - ' + str(tt1) + '\n' + 'Status - done\n' +
                          'Actual time - ' + str(tt2) + '\n')
            self.assertEqual(cmp_string, str(race))
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        try:  # remove target time
            race.set_target_time()
            cmp_string = ('Martial Cottle Park 5K of type ' + str(rt1) + '\n' +
                          'On ' + str(rd1) + '\n' + 'Status - done\n' +
                          'Actual time - ' + str(tt2) + '\n')
            self.assertEqual(cmp_string, str(race))
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        try:  # negative
            race.set_status('lulu')
            self.fail('Should not get here with a bad status')
        except ValueError as ex:
            self.assertEqual("Status not in ['scheduled', 'done', 'skipped']", str(ex))

    def test_to_json(self):

        rt1 = FirstRaceType(name='5K', distance=FirstDistance.from_string('5.0 km'))
        rd1 = date(year=2017, month=7, day=29)
        tt1 = FirstTime.from_string(string='0:25:30')
        tt2 = FirstTime.from_string(string='0:24:34')

        try:  # positive
            race = FirstRace(race_type=rt1, race_date=rd1, name='Martial Cottle Park 5K', target_time=tt1)
            cmp_json = {'Name': 'Martial Cottle Park 5K',
                        'race_date': '2017-07-29',
                        'race_type': {'distance': {'distance': 5.0, 'unit': 'km'}, 'name': '5K'},
                        'status': 'scheduled',
                        'target_time': {'seconds': 1530, 'time': '0:25:30'}}
            self.assertEqual(cmp_json, race.to_json())
            cmp_json = {'Name': 'Martial Cottle Park 5K',
                        'race_date': '2017-07-29',
                        'race_type': {'distance': {'distance': 3.10686, 'unit': 'mile'}, 'name': '5K'},
                        'status': 'scheduled',
                        'target_time': {'seconds': 1530, 'time': '0:25:30'}}
            FirstUtils.assert_deep_almost_equal(self, cmp_json, race.to_json(output_unit='mile'), 5)
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        try:  # add actual time
            race.set_status(status='done')
            race.set_actual_time(a_time=tt2)
            cmp_json = {'Name': 'Martial Cottle Park 5K',
                        'actual_time': '0:24:34',
                        'race_date': '2017-07-29',
                        'race_type': {'distance': {'distance': 5.0, 'unit': 'km'}, 'name': '5K'},
                        'status': 'done',
                        'target_time': {'seconds': 1530, 'time': '0:25:30'}}
            self.assertEqual(cmp_json, race.to_json())
            cmp_json = {'Name': 'Martial Cottle Park 5K',
                        'actual_time': '0:24:34',
                        'race_date': '2017-07-29',
                        'race_type': {'distance': {'distance': 3.10686, 'unit': 'mile'}, 'name': '5K'},
                        'status': 'done',
                        'target_time': {'seconds': 1530, 'time': '0:25:30'}}
            FirstUtils.assert_deep_almost_equal(self, cmp_json, race.to_json(output_unit='mile'), 5)
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))


if __name__ == '__main__':
    unittest.main()
