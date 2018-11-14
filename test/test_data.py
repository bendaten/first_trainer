import unittest

from os.path import expanduser

from first_data import FirstData
from first_time import FirstTime


class TestFirstData(unittest.TestCase):

    def test_equivalent_time(self):

        data_file_path = expanduser('~') + '/PycharmProjects/first/database/FIRSTregularPlans.xml'
        try:  # good path
            data = FirstData(xml_path=data_file_path)
            self.assertEqual(4, len(data.race_types))
            self.assertEqual(1, data.race_type_index_by_name('10K'))
            self.assertEqual(2, data.race_type_index_by_name('HalfMarathon'))
            self.assertEqual(91, len(data.race_times))
            self.assertEqual(4, len(data.race_times[0]))
            from_time = FirstTime.from_string('0:20:13')
            self.assertEqual('1:34:15', str(data.equivalent_time(time_from=from_time,
                                                                 race_index_from=0, race_index_to=2)))
            from_time = FirstTime.from_string('1:54:32')
            self.assertEqual('4:01:39', str(data.equivalent_time(time_from=from_time,
                                                                 race_index_from=2, race_index_to=3)))
        except ValueError as vex:
            self.fail(str(vex))
        except IOError as ioex:
            self.fail(str(ioex))

        try:  # bad race name
            index = data.race_type_index_by_name('lulu')
            self.fail('Should not get here with a bad race type name')
        except ValueError as ex:
            self.assertEqual('FirstSegment.race_type_index_by_name - Race type lulu not found', str(ex))

        try:  # time not found high
            from_time = FirstTime.from_string('4:49:59')
            equivalent_time = data.equivalent_time(time_from=from_time, race_index_from=2, race_index_to=0)
            self.fail('Should not get here with time not found')
        except ValueError as ex:
            self.assertEqual('FirstData.equivalent_time - time is longer than the highest database time', str(ex))

        try:  # time not found low
            from_time = FirstTime.from_string('0:49:59')
            equivalent_time = data.equivalent_time(time_from=from_time, race_index_from=2, race_index_to=0)
            self.fail('Should not get here with time not found')
        except ValueError as ex:
            self.assertEqual('FirstData.equivalent_time - time is shorter than the lowest database time', str(ex))

        try:  # bad time type
            equivalent_time = data.equivalent_time(time_from='abc', race_index_from=0, race_index_to=1)
            self.fail('Should not get here with bad time type')
        except TypeError as ex:
            self.assertEqual('FirstData.equivalent_time - time_from must be an instance of FirstTime', str(ex))

        try:  # bad index type
            equivalent_time = data.equivalent_time(time_from=from_time, race_index_from='abc', race_index_to=2)
            self.fail('Should not get here with bad index')
        except TypeError as ex:
            self.assertEqual('FirstData.equivalent_time - race_index_from must be an int', str(ex))

        try:  # bad index type
            equivalent_time = data.equivalent_time(time_from=from_time, race_index_from=0, race_index_to='abc')
            self.fail('Should not get here with bad index')
        except TypeError as ex:
            self.assertEqual('FirstData.equivalent_time - race_index_to must be an int', str(ex))

        try:  # index out of range
            equivalent_time = data.equivalent_time(time_from=from_time, race_index_from=-1, race_index_to=2)
            self.fail('Should not get here with bad index')
        except ValueError as ex:
            self.assertEqual('FirstData.equivalent_time - race index must be between 0 and 3', str(ex))

        try:  # index out of range
            equivalent_time = data.equivalent_time(time_from=from_time, race_index_from=4, race_index_to=2)
            self.fail('Should not get here with bad index')
        except ValueError as ex:
            self.assertEqual('FirstData.equivalent_time - race index must be between 0 and 3', str(ex))

        try:  # index out of range
            equivalent_time = data.equivalent_time(time_from=from_time, race_index_from=1, race_index_to=-2)
            self.fail('Should not get here with bad index')
        except ValueError as ex:
            self.assertEqual('FirstData.equivalent_time - race index must be between 0 and 3', str(ex))

        try:  # index out of range
            equivalent_time = data.equivalent_time(time_from=from_time, race_index_from=1, race_index_to=55)
            self.fail('Should not get here with bad index')
        except ValueError as ex:
            self.assertEqual('FirstData.equivalent_time - race index must be between 0 and 3', str(ex))

        try:  # bad database file
            bad_data = FirstData(xml_path='lulu')
            self.fail('Should not get here with bad file name')
        except IOError as ioex:
            self.assertEqual("[Errno 2] No such file or directory: 'lulu'", str(ioex))

    def test_segments(self):

        data_file_path = expanduser('~') + '/PycharmProjects/first/database/FIRSTregularPlans.xml'
        try:  # good path
            data = FirstData(xml_path=data_file_path)
            self.assertEqual(14, len(data.segments))
            self.assertEqual('400m  distance  400.0 m', str(data.segments[0]))
            self.assertEqual('long  pace', str(data.segments[-5]))
            self.assertEqual('cooldown  time  0:10:00  easy', str(data.segments[-2]))
            self.assertEqual('5K', data.reference_race)
            self.assertEqual(91, len(data.segments_paces))
            self.assertEqual('0:15:00', str(data.segments_paces[0][0]))
            self.assertEqual('0:04:22 min per mile', str(data.segments_paces[0][4]))
            self.assertEqual('0:20:00', str(data.segments_paces[30][0]))
            self.assertEqual('0:05:56 min per mile', str(data.segments_paces[30][3]))
            self.assertEqual('0:30:00', str(data.segments_paces[-1][0]))
            self.assertEqual('0:11:31 min per mile', str(data.segments_paces[-1][11]))
        except ValueError as vex:
            self.fail(str(vex))
        except IOError as ioex:
            self.fail(str(ioex))

    def test_plan_instructions(self):

        data_file_path = expanduser('~') + '/PycharmProjects/first/database/FIRSTregularPlans.xml'
        try:  # good path
            data = FirstData(xml_path=data_file_path)
            self.assertEqual(4, len(data.plan_instructions))
            plan1 = data.plan_instructions[0]
            self.assertEqual('5K plan instructions', plan1.name)
            self.assertEqual('5K', plan1.race_name)
            self.assertEqual(36, len(plan1.instructions))
            self.assertEqual('1 1 warmup#8x(400m#400 m@RI)cooldown', plan1.instructions[0])
            self.assertEqual('5 1 warmup#4x(1000m#400 m@RI)cooldown', plan1.instructions[12])
            plan2 = data.plan_instructions[1]
            self.assertEqual('10K plan instructions', plan2.name)
            self.assertEqual('10K', plan2.race_name)
            self.assertEqual(36, len(plan2.instructions))
            self.assertEqual('1 1 warmup#8x(400m#400 m@RI)cooldown', plan2.instructions[0])
            self.assertEqual('2 3 7 mile@long', plan2.instructions[5])
            plan3 = data.plan_instructions[2]
            self.assertEqual('Half Marathon plan instructions', plan3.name)
            self.assertEqual('HalfMarathon', plan3.race_name)
            self.assertEqual(54, len(plan3.instructions))
            self.assertEqual('1 1 warmup#12x(400m#300 m@RI)cooldown', plan3.instructions[0])
            self.assertEqual('13 3 10 mile@RP+20', plan3.instructions[38])
            plan4 = data.plan_instructions[3]
            self.assertEqual('Marathon plan instructions', plan4.name)
            self.assertEqual('Marathon', plan4.race_name)
            self.assertEqual(48, len(plan4.instructions))
            self.assertEqual('1 1 warmup#3x(1600m#200 m@RI)cooldown', plan4.instructions[0])
            self.assertEqual('16 3 26.22 mile@RP', plan4.instructions[47])
        except ValueError as vex:
            self.fail(str(vex))
        except IOError as ioex:
            self.fail(str(ioex))


if __name__ == '__main__':
    unittest.main()
