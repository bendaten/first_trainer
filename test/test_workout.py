import unittest
from datetime import date
from os.path import expanduser

from first_data import FirstData
from first_distance import FirstDistance
from first_pace import FirstPace
from first_step import FirstStepBody, FirstStepRepeat, FirstStepBase
from first_time import FirstTime
from first_workout import FirstWorkout


class TestFirstWorkout(unittest.TestCase):

    def test_to_string_new(self):

        pass

    def test_steps_new(self):

        FirstStepBase.reset_global_id()
        t_warmup = FirstTime.from_string('0:15:00')
        p_warmup = FirstPace.from_string('0:10:00 min per mile')
        s_warmup = FirstStepBody(name='Warm up', pace=p_warmup, time=t_warmup)

        s_intervals = FirstStepRepeat(name='Intervals', repeat=8)
        d_interval = FirstDistance.from_string('400 m')
        p_fast = FirstPace.from_string('0:08:00 min per mile')
        s_fast = FirstStepBody(name='Fast', pace=p_fast, distance=d_interval)
        s_slow = FirstStepBody(name='Rest', pace=p_warmup, distance=d_interval)
        s_intervals.add_step(s_fast)
        s_intervals.add_step(s_slow)

        t_cooldown = FirstTime.from_string('0:10:00')
        s_cooldown = FirstStepBody(name='Cool down', pace=p_warmup, time=t_cooldown)

        try:  # positive
            wo = FirstWorkout(name='Week 1 Key-run 1', workout_date=date(2017, 6, 24))
            wo.add_step(s_warmup)
            wo.add_step(s_intervals)
            wo.add_step(s_cooldown)
            cmp_string = ('Week 1 Key-run 1\n' +
                          '2017-06-24\n' +
                          'scheduled\n' +
                          '\tStep: "Warm up"  id = 0\n' +
                          'type - body  pace - 0:10:00 min per mile\n' +
                          'Time - 0:15:00\n' +
                          '\tStep: "Intervals"  id = 1\n' +
                          'type - repeat  repeat - 8\n' +
                          '\tStep: "Cool down"  id = 4\n' +
                          'type - body  pace - 0:10:00 min per mile\n' +
                          'Time - 0:10:00\n')
            self.assertEqual(cmp_string, str(wo))
            cmp_string = '"Week 1 Key-run 1"\n' +\
                         '  Sat 2017-06-24\n' +\
                         '  scheduled\n' +\
                         '  Step: "Warm up"\n' +\
                         '    0:15:00  at  0:10:00 min per mile\n' +\
                         '  Step: "Intervals"\n' +\
                         '    Step: "Fast"\n' +\
                         '      400.0 m  at  0:08:00 min per mile\n' +\
                         '    Step: "Rest"\n' +\
                         '      400.0 m  at  0:10:00 min per mile\n' +\
                         '  Step: "Cool down"\n' +\
                         '    0:10:00  at  0:10:00 min per mile\n' +\
                         '  Totals: distance = 6.48 miles   duration = 60.79 minutes\n'
            self.assertEqual(cmp_string, wo.details(level=2))
            total_distance_miles = 15.0/10 + 8*(800/1609.344) + 10.0/10
            self.assertAlmostEqual(total_distance_miles, wo.total(), 5)
            total_distance_km = total_distance_miles * 1.609344
            self.assertAlmostEqual(total_distance_km, wo.total(unit='km'), 5)
            total_time_minutes = 15.0 + 8*(400/1609.344*8 + 400/1609.344*10) + 10.0
            self.assertAlmostEqual(total_time_minutes, wo.total(what='time', unit='minute'))
            total_time_hours = total_time_minutes / 60.0
            self.assertAlmostEqual(total_time_hours, wo.total(what='time', unit='hour'))
            tcx_string = ('<Workout Sport="Running">\n' +
                          '  <Name>Week 1 Key-run 1</Name>\n' +
                          '  <Step xsi:type="Step_t">\n' +
                          '    <StepId>0</StepId>\n' +
                          '    <Name>Warm up</Name>\n' +
                          '    <Duration xsi:type="Time_t">\n' +
                          '      <Seconds>900</Seconds>\n' +
                          '    </Duration>\n' +
                          '    <Intensity>Active</Intensity>\n' +
                          '    <Target xsi:type="Speed_t">\n' +
                          '      <SpeedZone xsi:type="CustomSpeedZone_t">\n' +
                          '      <LowInMetersPerSecond>2.6600727</LowInMetersPerSecond>\n' +
                          '      <HighInMetersPerSecond>2.7047798</HighInMetersPerSecond>\n' +
                          '    </SpeedZone>\n' +
                          '    </Target>\n' +
                          '  </Step>\n' +
                          '  <Step xsi:type="Repeat_t">\n' +
                          '    <StepId>1</StepId>\n' +
                          '    <Name>Intervals</Name>\n' +
                          '    <Repetitions>8</Repetitions>\n' +
                          '    <Child xsi:type="Step_t">\n' +
                          '      <StepId>2</StepId>\n' +
                          '      <Name>Fast</Name>\n' +
                          '      <Duration xsi:type="Distance_t">\n' +
                          '        <Meters>400</Meters>\n' +
                          '      </Duration>\n' +
                          '      <Intensity>Active</Intensity>\n' +
                          '      <Target xsi:type="Speed_t">\n' +
                          '        <SpeedZone xsi:type="CustomSpeedZone_t">\n' +
                          '        <LowInMetersPerSecond>3.3182351</LowInMetersPerSecond>\n' +
                          '        <HighInMetersPerSecond>3.3880926</HighInMetersPerSecond>\n' +
                          '      </SpeedZone>\n' +
                          '      </Target>\n' +
                          '    </Child>\n' +
                          '    <Child xsi:type="Step_t">\n' +
                          '      <StepId>3</StepId>\n' +
                          '      <Name>Rest</Name>\n' +
                          '      <Duration xsi:type="Distance_t">\n' +
                          '        <Meters>400</Meters>\n' +
                          '      </Duration>\n' +
                          '      <Intensity>Active</Intensity>\n' +
                          '      <Target xsi:type="Speed_t">\n' +
                          '        <SpeedZone xsi:type="CustomSpeedZone_t">\n' +
                          '        <LowInMetersPerSecond>2.6600727</LowInMetersPerSecond>\n' +
                          '        <HighInMetersPerSecond>2.7047798</HighInMetersPerSecond>\n' +
                          '      </SpeedZone>\n' +
                          '      </Target>\n' +
                          '    </Child>\n' +
                          '  </Step>\n' +
                          '  <Step xsi:type="Step_t">\n' +
                          '    <StepId>4</StepId>\n' +
                          '    <Name>Cool down</Name>\n' +
                          '    <Duration xsi:type="Time_t">\n' +
                          '      <Seconds>600</Seconds>\n' +
                          '    </Duration>\n' +
                          '    <Intensity>Active</Intensity>\n' +
                          '    <Target xsi:type="Speed_t">\n' +
                          '      <SpeedZone xsi:type="CustomSpeedZone_t">\n' +
                          '      <LowInMetersPerSecond>2.6600727</LowInMetersPerSecond>\n' +
                          '      <HighInMetersPerSecond>2.7047798</HighInMetersPerSecond>\n' +
                          '    </SpeedZone>\n' +
                          '    </Target>\n' +
                          '  </Step>\n')
            tcx_string_end = ('  <ScheduledOn>2017-06-24</ScheduledOn>\n' +
                              '</Workout>\n')
            cmp_string = tcx_string + tcx_string_end
            self.assertEqual(cmp_string, wo.tcx())

            wo.add_step(step=s_warmup)
            cmp_string = ('Week 1 Key-run 1\n' +
                          '2017-06-24\n' +
                          'scheduled\n' +
                          '\tStep: "Warm up"  id = 0\n' +
                          'type - body  pace - 0:10:00 min per mile\n' +
                          'Time - 0:15:00\n' +
                          '\tStep: "Intervals"  id = 1\n' +
                          'type - repeat  repeat - 8\n' +
                          '\tStep: "Cool down"  id = 4\n' +
                          'type - body  pace - 0:10:00 min per mile\n' +
                          'Time - 0:10:00\n' +
                          '\tStep: "Warm up"  id = 0\n' +
                          'type - body  pace - 0:10:00 min per mile\n' +
                          'Time - 0:15:00\n')
            self.assertEqual(cmp_string, str(wo))
        except ValueError as vex:
            self.fail(str(vex))
        except TypeError as tex:
            self.fail(str(tex))

        try:  # wrong type
            dummy = FirstWorkout(name='Week 1 Key-run 1', workout_date=123)
            self.fail('Should not get here with a wrong type for date')
        except TypeError as ex:
            self.assertEqual('FirstWorkout.__init__ - date must be a datetime', str(ex))

        wo1 = FirstWorkout(name='Week 1 Key-run 1', workout_date=date(2017, 4, 1))

        try:  # change status
            wo1.set_status('skipped')
            self.assertEqual('Week 1 Key-run 1\n2017-04-01\nskipped\n\tEmpty workout\n', str(wo1))
        except ValueError as ex:
            self.fail(str(ex))

        try:  # bad status
            wo1.set_status('lulu')
            self.fail('Should not get here with bad status')
        except ValueError as ex:
            self.assertEqual("FirstWorkout.set_status - Status not in ['scheduled', 'done', 'skipped']", str(ex))

    def test_from_instructions_new(self):

        rp = FirstPace.from_string('0:09:35 min per mile')
        ti = 50
        wo_date = date(2017, 8, 21)
        data_file_path = expanduser('~') + '/PycharmProjects/first/database/FIRSTregularPlans.xml'
        data = FirstData(data_file_path)
        instructions = '1 1 warmup#3x(1600m#200 m@RI)cooldown'
        FirstStepBase.reset_global_id()

        try:
            wo1 = FirstWorkout.from_instructions(instructions=instructions, wo_date=wo_date, data=data,
                                                 time_index=ti, race_pace=rp)
            self.assertEqual('Week 1 Keyrun 1', wo1.name)
            self.assertEqual('2017-08-21', str(wo1.workout_date))
            self.assertEqual('scheduled', wo1.status)
            self.assertEqual('warmup#3x(1600m#200 m@RI)cooldown', wo1.note)
            self.assertEqual(3, len(wo1.steps))

            # Time steps
            step = wo1.steps[0]
            self.assertEqual(0, step.step_id)
            self.assertEqual('warmup', step.name)
            self.assertEqual('0:09:23 min per mile', str(step.pace))
            self.assertEqual(None, step.distance)
            self.assertEqual('time', step.get_duration_type())
            self.assertEqual('0:15:00', str(step.time))
            self.assertEqual(15.0, step.total(what='time', unit='minute'))
            self.assertAlmostEquals(1.59858, step.total(what='distance', unit='mile'), 5)

            step = wo1.steps[2]
            self.assertEqual(4, step.step_id)
            self.assertEqual('cooldown', step.name)
            self.assertEqual('0:09:23 min per mile', str(step.pace))
            self.assertEqual(None, step.distance)
            self.assertEqual('time', step.get_duration_type())
            self.assertEqual('0:10:00', str(step.time))
            self.assertEqual(600.0, step.total(what='time', unit='second'))
            self.assertAlmostEquals(1.06572, step.total(what='distance', unit='mile'), 5)

            # Repeat step
            step = wo1.steps[1]
            self.assertEqual(1, step.step_id)
            self.assertEqual('repeat X 3', step.name)
            self.assertEqual(3, step.repeat)
            self.assertEqual(2, len(step.steps))
            substep = step.steps[0]
            self.assertEqual(2, substep.step_id)
            self.assertEqual('1600m', substep.name)
            self.assertEqual('0:07:18 min per mile', str(substep.pace))
            self.assertEqual(None, substep.time)
            self.assertEqual('distance', substep.get_duration_type())
            self.assertEqual('1600.0 m', str(substep.distance))
            self.assertAlmostEquals(7.25762, substep.total(what='time', unit='minute'), 5)
            self.assertAlmostEquals(0.99419, substep.total(what='distance', unit='mile'), 5)
            substep = step.steps[1]
            self.assertEqual(3, substep.step_id)
            self.assertEqual('200 m@RI', substep.name)
            self.assertEqual('0:09:23 min per mile', str(substep.pace))
            self.assertEqual(None, substep.time)
            self.assertEqual('distance', substep.get_duration_type())
            self.assertEqual('200.0 m', str(substep.distance))
            self.assertAlmostEquals(1.16611, substep.total(what='time', unit='minute'), 5)
            self.assertAlmostEquals(0.12427, substep.total(what='distance', unit='mile'), 5)

            # Repeat steps totals
            self.assertAlmostEquals(25.27117, step.total(what='time', unit='minute'), 5)
            self.assertAlmostEquals(3.35540, step.total(what='distance', unit='mile'), 5)

            # Workout totals
            self.assertAlmostEquals(50.27117, wo1.total(what='time', unit='minute'), 5)
            self.assertAlmostEquals(6.01970, wo1.total(what='distance', unit='mile'), 5)

            file_name = expanduser('~/PycharmProjects/first/database/cmp_workout1.tcx')
            # to_file = open(file_name, 'w')
            # to_file.write(wo1.tcx())
            # to_file.close()
            from_file = open(file_name)
            cmp_string = from_file.read()
            from_file.close()
            self.assertEqual(cmp_string, wo1.tcx())

        except ValueError as ex:
            self.fail(str(ex))

        instructions = '1 2 warmup#3x(1600m#4x(200 m@RI)800m)cooldown'
        try:
            wo2 = FirstWorkout.from_instructions(instructions=instructions, wo_date=wo_date, data=data,
                                                 time_index=ti, race_pace=rp)

            self.assertEqual('Week 1 Keyrun 2', wo2.name)
            self.assertEqual('2017-08-21', str(wo2.workout_date))
            self.assertEqual('scheduled', wo2.status)
            self.assertEqual('warmup#3x(1600m#4x(200 m@RI)800m)cooldown', wo2.note)
            self.assertEqual(3, len(wo2.steps))

            # recursive repeat step
            step = wo2.steps[1]
            self.assertEqual(6, step.step_id)
            self.assertEqual('repeat X 3', step.name)
            self.assertEqual(3, step.repeat)
            self.assertEqual(3, len(step.steps))
            substep = step.steps[1]
            self.assertEqual(8, substep.step_id)
            self.assertEqual('repeat X 4', substep.name)
            self.assertEqual(4, substep.repeat)
            self.assertEqual(1, len(substep.steps))
            subsubstep = substep.steps[0]
            self.assertEqual(9, subsubstep.step_id)
            self.assertEqual('200 m@RI', subsubstep.name)
            self.assertEqual('0:09:23 min per mile', str(subsubstep.pace))
            self.assertEqual(None, subsubstep.time)
            self.assertEqual('distance', subsubstep.get_duration_type())
            self.assertEqual('200.0 m', str(subsubstep.distance))
            self.assertAlmostEquals(1.16611, subsubstep.total(what='time', unit='minute'), 5)
            self.assertAlmostEquals(0.12427, subsubstep.total(what='distance', unit='mile'), 5)

            self.assertAlmostEquals(4.66443, substep.total(what='time', unit='minute'), 5)
            self.assertAlmostEquals(0.4971, substep.total(what='distance', unit='mile'), 5)

            self.assertAlmostEquals(46.20516, step.total(what='time', unit='minute'), 5)
            self.assertAlmostEquals(5.96516, step.total(what='distance', unit='mile'), 5)

            self.assertAlmostEquals(71.20516, wo2.total(what='time', unit='minute'), 5)
            self.assertAlmostEquals(8.62946, wo2.total(what='distance', unit='mile'), 5)

            file_name = expanduser('~/PycharmProjects/first/database/cmp_workout2.tcx')
            # to_file = open(file_name, 'w')
            # to_file.write(wo2.tcx())
            # to_file.close()
            from_file = open(file_name)
            cmp_string = from_file.read()
            from_file.close()
            self.assertEqual(cmp_string, wo2.tcx())

        except ValueError as ex:
            self.fail(str(ex))

        instructions = '1 1 warmup#3x(1600m#200 m@RI#cooldown'
        try:  # unbalanced parentheses
            dummy = FirstWorkout.from_instructions(instructions=instructions, wo_date=wo_date,
                                                   data=data, time_index=ti, race_pace=rp)
        except ValueError as ex:
            self.assertEqual('FirstWorkout.__parse_steps - Unbalanced parentheses', str(ex))


if __name__ == '__main__':
    unittest.main()
