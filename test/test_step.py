import unittest

# so i don't forget - decided to put the 'repeat' feature in the workout instead recursively here
from first_distance import FirstDistance
from first_pace import FirstPace
from first_step import FirstStepBody, FirstStepRepeat, FirstStepBase
from first_time import FirstTime


class TestFirstStepNew(unittest.TestCase):

    def test_body(self):

        FirstStepBase.reset_global_id()

        pace = FirstPace.from_string(str_input='0:10:00 min per mile')
        distance = FirstDistance.from_string(string='3 mile')
        time = FirstTime.from_string(string='0:15:00')

        try:  # distance step
            step_b = FirstStepBody(name='3 miles @ 10 minutes per mile', pace=pace, distance=distance)
            cmp_string = 'Step: "3 miles @ 10 minutes per mile"  id = 0\n' + \
                         'type - body  pace - 0:10:00 min per mile\nDistance - 3.0 mile\n'
            self.assertEqual(cmp_string, str(step_b))
            self.assertAlmostEqual(3.0, step_b.total(unit='mile'), 5)
            self.assertAlmostEqual(4.828032, step_b.total(unit='km'), 5)
            self.assertAlmostEqual(30.0, step_b.total(what='time', unit='minute'), 5)
            self.assertAlmostEqual(0.5, step_b.total(what='time', unit='hour'), 5)
            tcx_string = ('<Step xsi:type="Step_t">\n' +
                          '  <StepId>0</StepId>\n' +
                          '  <Name>3 miles @ 10 minutes per mile</Name>\n' +
                          '  <Duration xsi:type="Distance_t">\n' +
                          '    <Meters>4828</Meters>\n' +
                          '  </Duration>\n' +
                          '  <Intensity>Active</Intensity>\n' +
                          '  <Target xsi:type="Speed_t">\n' +
                          '    <SpeedZone xsi:type="CustomSpeedZone_t">\n' +
                          '      <LowInMetersPerSecond>2.6600727</LowInMetersPerSecond>\n' +
                          '      <HighInMetersPerSecond>2.7047798</HighInMetersPerSecond>\n' +
                          '    </SpeedZone>\n' +
                          '  </Target>\n' +
                          '</Step>')
            self.assertEqual(tcx_string, step_b.tcx().indented_str())  # no indent
            tcx_string = ('<Step xsi:type="Step_t">\n' +
                          '  <StepId>0</StepId>\n' +
                          '  <Name>3 miles @ 10 minutes per mile</Name>\n' +
                          '  <Duration xsi:type="Distance_t">\n' +
                          '    <Meters>4828</Meters>\n' +
                          '  </Duration>\n' +
                          '  <Intensity>Active</Intensity>\n' +
                          '  <Target xsi:type="Speed_t">\n' +
                          '    <SpeedZone xsi:type="CustomSpeedZone_t">\n' +
                          '      <LowInMetersPerSecond>2.6688955</LowInMetersPerSecond>\n' +
                          '      <HighInMetersPerSecond>2.6957186</HighInMetersPerSecond>\n' +
                          '    </SpeedZone>\n' +
                          '  </Target>\n' +
                          '</Step>')
            self.assertEqual(tcx_string, step_b.tcx(delta_seconds=3).indented_str())
            cmp_json = {'distance': {'distance': 3.0, 'unit': 'mile'},
                        'name': '3 miles @ 10 minutes per mile',
                        'pace': {'length_unit': 'mile',
                                 'pace': '0:10:00 min per mile',
                                 'time': {'seconds': 600, 'time': '0:10:00'}}}
            self.assertEqual(cmp_json, step_b.to_json())
            cmp_json = {'distance': {'distance': 4.828032, 'unit': 'km'},
                        'name': '3 miles @ 10 minutes per mile',
                        'pace': {'length_unit': 'km',
                                 'pace': '0:06:13 min per km',
                                 'time': {'seconds': 373, 'time': '0:06:13'}}}
            self.assertEqual(cmp_json, step_b.to_json(output_unit='km'))
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        try:  # time step
            step_b = FirstStepBody(name='15 minutes @ 10 minutes per mile', pace=pace, time=time)
            cmp_string = 'Step: "15 minutes @ 10 minutes per mile"  id = 1\n' + \
                         'type - body  pace - 0:10:00 min per mile\nTime - 0:15:00\n'
            self.assertEqual(cmp_string, str(step_b))
            self.assertAlmostEqual(15.0, step_b.total(what='time', unit='minute'), 5)
            self.assertAlmostEqual(7920.0, step_b.total(unit='ft'))
            tcx_string = ('<Step xsi:type="Step_t">\n' +
                          '  <StepId>1</StepId>\n' +
                          '  <Name>15 minutes @ 10 minutes per mile</Name>\n' +
                          '  <Duration xsi:type="Time_t">\n' +
                          '    <Seconds>900</Seconds>\n' +
                          '  </Duration>\n' +
                          '  <Intensity>Active</Intensity>\n' +
                          '  <Target xsi:type="Speed_t">\n' +
                          '    <SpeedZone xsi:type="CustomSpeedZone_t">\n' +
                          '      <LowInMetersPerSecond>2.6600727</LowInMetersPerSecond>\n' +
                          '      <HighInMetersPerSecond>2.7047798</HighInMetersPerSecond>\n' +
                          '    </SpeedZone>\n' +
                          '  </Target>\n' +
                          '</Step>')
            self.assertEqual(tcx_string, step_b.tcx().indented_str())
            cmp_json = {'name': '15 minutes @ 10 minutes per mile',
                        'pace': {'length_unit': 'mile',
                                 'pace': '0:10:00 min per mile',
                                 'time': {'seconds': 600, 'time': '0:10:00'}},
                        'time': {'seconds': 900, 'time': '0:15:00'}}
            self.assertEqual(cmp_json, step_b.to_json())
            cmp_json = {'name': '15 minutes @ 10 minutes per mile',
                        'pace': {'length_unit': 'km',
                                 'pace': '0:06:13 min per km',
                                 'time': {'seconds': 373, 'time': '0:06:13'}},
                        'time': {'seconds': 900, 'time': '0:15:00'}}
            self.assertEqual(cmp_json, step_b.to_json(output_unit='km'))
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        try:  # no distance and no time
            _ = FirstStepBody(name='dummy', pace=pace)
            self.fail('Should not get here with neither distance nor duration')
        except ValueError as ex:
            self.assertEqual('Either distance or time must have a value', str(ex))

        try:  # both distance and time
            _ = FirstStepBody(name='dummy', pace=pace, distance=distance, time=time)
            self.fail('Should not get here with both distance and time')
        except ValueError as ex:
            self.assertEqual('Cannot set both distance and duration in the same step', str(ex))

    def test_repeat(self):

        FirstStepBase.reset_global_id()

        pace = FirstPace.from_string(str_input='0:10:00 min per mile')
        distance = FirstDistance.from_string(string='3 mile')
        time = FirstTime.from_string(string='0:15:00')

        try:
            name = '3 X (3 mile @ 10 min per mile + 15 minutes @ 19 min per mile)'
            step_r = FirstStepRepeat(name=name, repeat=3)
            self.assertEqual('Step: "' + name + '"  id = 0\ntype - repeat  repeat - 3\n', str(step_r))
            self.assertAlmostEqual(0.0, step_r.total(unit='mile'), 5)
            self.assertAlmostEqual(0.0, step_r.total(what='time', unit='minute'))
            tcx_string = ('<Step xsi:type="Repeat_t">\n' +
                          '  <StepId>0</StepId>\n' +
                          '  <Name>3 X (3 mile @ 10 min per mile + 15 minutes @ 19 min per mile)</Name>\n' +
                          '  <Repetitions>3</Repetitions>\n' +
                          '</Step>')
            self.assertEqual(tcx_string, step_r.tcx().indented_str())
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        try:
            step_b1 = FirstStepBody(name='3 mile @ 10 min per mile', pace=pace, distance=distance)
            step_b2 = FirstStepBody(name='15 minutes @ 19 min per mile', pace=pace, time=time)
            step_r.add_step(step_b1)
            step_r.add_step(step_b2)
            short = 'Step: "' + name + '"  id = 0\ntype - repeat  repeat - 3\n'
            self.assertEqual(short, str(step_r))
            detail = 'Step: "3 X (3 mile @ 10 min per mile + 15 minutes @ 19 min per mile)"\n' + \
                     '  Step: "3 mile @ 10 min per mile"\n' + \
                     '    3.0 mile  at  0:10:00 min per mile\n' + \
                     '  Step: "15 minutes @ 19 min per mile"\n' + \
                     '    0:15:00  at  0:10:00 min per mile\n'
            self.assertEqual(detail, step_r.details())
            self.assertAlmostEqual(13.5, step_r.total(unit='mile'), 5)
            self.assertAlmostEqual(135.0, step_r.total(what='time', unit='minute'))
            tcx_string = ('<Step xsi:type="Repeat_t">\n' +
                          '  <StepId>0</StepId>\n' +
                          '  <Name>3 X (3 mile @ 10 min per mile + 15 minutes @ 19 min per mile)</Name>\n' +
                          '  <Repetitions>3</Repetitions>\n' +
                          '  <Child xsi:type="Step_t">\n' +
                          '    <StepId>1</StepId>\n' +
                          '    <Name>3 mile @ 10 min per mile</Name>\n' +
                          '    <Duration xsi:type="Distance_t">\n' +
                          '      <Meters>4828</Meters>\n' +
                          '    </Duration>\n' +
                          '    <Intensity>Active</Intensity>\n' +
                          '    <Target xsi:type="Speed_t">\n' +
                          '      <SpeedZone xsi:type="CustomSpeedZone_t">\n' +
                          '        <LowInMetersPerSecond>2.6382689</LowInMetersPerSecond>\n' +
                          '        <HighInMetersPerSecond>2.7277017</HighInMetersPerSecond>\n' +
                          '      </SpeedZone>\n' +
                          '    </Target>\n' +
                          '  </Child>\n' +
                          '  <Child xsi:type="Step_t">\n' +
                          '    <StepId>2</StepId>\n' +
                          '    <Name>15 minutes @ 19 min per mile</Name>\n' +
                          '    <Duration xsi:type="Time_t">\n' +
                          '      <Seconds>900</Seconds>\n' +
                          '    </Duration>\n' +
                          '    <Intensity>Active</Intensity>\n' +
                          '    <Target xsi:type="Speed_t">\n' +
                          '      <SpeedZone xsi:type="CustomSpeedZone_t">\n' +
                          '        <LowInMetersPerSecond>2.6382689</LowInMetersPerSecond>\n' +
                          '        <HighInMetersPerSecond>2.7277017</HighInMetersPerSecond>\n' +
                          '      </SpeedZone>\n' +
                          '    </Target>\n' +
                          '  </Child>\n'
                          '</Step>')
            self.assertEqual(tcx_string, step_r.tcx(delta_seconds=10).indented_str())
            cmp_json = {'name': '3 X (3 mile @ 10 min per mile + 15 minutes @ 19 min per mile)',
                        'repeat': 3,
                        'steps': [{'distance': {'distance': 3.0, 'unit': 'mile'},
                                   'name': '3 mile @ 10 min per mile',
                                   'pace': {'length_unit': 'mile',
                                            'pace': '0:10:00 min per mile',
                                            'time': {'seconds': 600, 'time': '0:10:00'}}},
                                  {'name': '15 minutes @ 19 min per mile',
                                   'pace': {'length_unit': 'mile',
                                            'pace': '0:10:00 min per mile',
                                            'time': {'seconds': 600, 'time': '0:10:00'}},
                                   'time': {'seconds': 900, 'time': '0:15:00'}}]}
            self.assertEqual(cmp_json, step_r.to_json())
            cmp_json = {'name': '3 X (3 mile @ 10 min per mile + 15 minutes @ 19 min per mile)',
                        'repeat': 3,
                        'steps': [{'distance': {'distance': 4.828032, 'unit': 'km'},
                                   'name': '3 mile @ 10 min per mile',
                                   'pace': {'length_unit': 'km',
                                            'pace': '0:06:13 min per km',
                                            'time': {'seconds': 373, 'time': '0:06:13'}}},
                                  {'name': '15 minutes @ 19 min per mile',
                                   'pace': {'length_unit': 'km',
                                            'pace': '0:06:13 min per km',
                                            'time': {'seconds': 373, 'time': '0:06:13'}},
                                   'time': {'seconds': 900, 'time': '0:15:00'}}]}
            self.assertEqual(cmp_json, step_r.to_json(output_unit='km'))
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        try:  # negative repeat
            _ = FirstStepRepeat(name='bla', repeat=-3)
            self.fail('Should not get here with negative repeat value')
        except ValueError as ex:
            self.assertEqual('repeat must be greater than 0', str(ex))

    def test_reset(self):

        FirstStepBase.reset_global_id()

        try:
            _ = FirstStepRepeat(name='before reset', repeat=1)  # id = 0
            step_r1 = FirstStepRepeat(name='before reset', repeat=1)  # id = 1
            self.assertEqual('Step: "before reset"  id = 1\ntype - repeat  repeat - 1\n', str(step_r1))
            FirstStepBase.reset_global_id()
            step_r2 = FirstStepRepeat(name='after reset', repeat=2)  # id = 0
            self.assertEqual('Step: "after reset"  id = 0\ntype - repeat  repeat - 2\n', str(step_r2))
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))


if __name__ == '__main__':
    unittest.main()
