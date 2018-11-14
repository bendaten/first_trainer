import unittest
from datetime import date

from first_race import FirstRaceType, FirstRace
from first_time import FirstTime


class TestFirstRaceType(unittest.TestCase):

    def test_to_string(self):

        try:
            r1 = FirstRaceType(name='marathon', distance=26.219, unit='mile')
            self.assertEqual('marathon - 26.219 mile', str(r1))
        except ValueError as ex:
            self.fail(str(ex))


class TestFirstRace(unittest.TestCase):

    def test_to_string(self):

        rt1 = FirstRaceType(name='5K', distance=5.0, unit='km')
        rd1 = date(year=2017, month=7, day=29)
        tt1 = FirstTime.from_string('0:25:30')
        tt2 = FirstTime.from_string('0:24:34')

        try:  # positive
            r1 = FirstRace(race_type=rt1, race_date=rd1, name='Martial Cottle Park 5K', target_time=tt1)
            cmp_string = ('Martial Cottle Park 5K of type ' + str(rt1) + '\n' +
                          'On ' + str(rd1) + '\n' + 'Target time - ' + str(tt1) + '\n' + 'Status - scheduled\n')
            self.assertEqual(cmp_string, str(r1))
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        try:  # add actual time
            r1.set_status('done')
            r1.set_actual_time(tt2)
            cmp_string = ('Martial Cottle Park 5K of type ' + str(rt1) + '\n' +
                          'On ' + str(rd1) + '\n' + 'Target time - ' + str(tt1) + '\n' + 'Status - done\n' +
                          'Actual time - ' + str(tt2) + '\n')
            self.assertEqual(cmp_string, str(r1))
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        try:  # remove target time
            r1.set_target_time()
            cmp_string = ('Martial Cottle Park 5K of type ' + str(rt1) + '\n' +
                          'On ' + str(rd1) + '\n' + 'Status - done\n' +
                          'Actual time - ' + str(tt2) + '\n')
            self.assertEqual(cmp_string, str(r1))
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        try:  # negative
            r1.set_target_time(1243)
            self.fail('Should not get here with bad target time')
        except TypeError as ex:
            self.assertEqual('FirstRace.set_target_time - a_time must be an instance of FirstTime', str(ex))

        try:  # negative
            r1.set_actual_time(1243)
            self.fail('Should not get here with bad actual time')
        except TypeError as ex:
            self.assertEqual('FirstRace.set_actual_time - a_time must be an instance of FirstTime', str(ex))

        try:  # negative
            r1.set_status(1234)
            self.fail('Should not get here with bad status')
        except TypeError as ex:
            self.assertEqual('FirstRace.set_status - status must be a string', str(ex))

        try:  # negative
            r1.set_status('lulu')
            self.fail('Should not get here with a bad status')
        except ValueError as ex:
            self.assertEqual("FirstRace.set_status - Status not in ['scheduled', 'done', 'skipped']", str(ex))


if __name__ == '__main__':
    unittest.main()
