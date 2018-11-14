import unittest


# so i don't forget - decided to put the 'repeat' feature in the workout instead recursively here
from first_distance import FirstDistance
from first_pace import FirstPace
from first_step import FirstStepBody, FirstStepRepeat, FirstStepBase
from first_time import FirstTime


class TestFirstStepNew(unittest.TestCase):

    def test_body(self):

        FirstStepBase.reset_global_id()

        p1 = FirstPace.from_string('0:10:00 min per mile')
        d1 = FirstDistance.from_string('3 mile')
        t1 = FirstTime.from_string('0:15:00')

        try:  # distance step
            s1 = FirstStepBody(name='3 miles @ 10 minutes per mile', pace=p1, distance=d1)
            cmp_string = 'Step: "3 miles @ 10 minutes per mile"  id = 0\n' + \
                         'type - body  pace - 0:10:00 min per mile\nDistance - 3.0 mile\n'
            self.assertEqual(cmp_string, str(s1))
            self.assertAlmostEquals(3.0, s1.total(unit='mile'), 5)
            self.assertAlmostEquals(4.828032, s1.total(unit='km'), 5)
            self.assertAlmostEquals(30.0, s1.total(what='time', unit='minute'), 5)
            self.assertAlmostEquals(0.5, s1.total(what='time', unit='hour'), 5)
            tcx_string = ('<Step xsi:type="Step_t">\n' +
                          '  <StepId>0</StepId>\n' +
                          '  <Name>3 miles @ 10 minutes per mile</Name>\n' +
                          '  <Duration xsi:type="Distance_t">\n' +
                          '    <Meters>4828</Meters>\n' +
                          '  </Duration>\n' +
                          '  <Intensity>Active</Intensity>\n' +
                          '  <Target xsi:type="Speed_t">\n' +
                          '    <SpeedZone xsi:type="CustomSpeedZone_t">\n' +
                          '    <LowInMetersPerSecond>2.6600727</LowInMetersPerSecond>\n' +
                          '    <HighInMetersPerSecond>2.7047798</HighInMetersPerSecond>\n' +
                          '  </SpeedZone>\n' +
                          '  </Target>\n' +
                          '</Step>\n')
            self.assertEqual(tcx_string, s1.tcx())  # no indent
            tcx_string = ('    <Step xsi:type="Step_t">\n' +
                          '      <StepId>0</StepId>\n' +
                          '      <Name>3 miles @ 10 minutes per mile</Name>\n' +
                          '      <Duration xsi:type="Distance_t">\n' +
                          '        <Meters>4828</Meters>\n' +
                          '      </Duration>\n' +
                          '      <Intensity>Active</Intensity>\n' +
                          '      <Target xsi:type="Speed_t">\n' +
                          '        <SpeedZone xsi:type="CustomSpeedZone_t">\n' +
                          '        <LowInMetersPerSecond>2.6688955</LowInMetersPerSecond>\n' +
                          '        <HighInMetersPerSecond>2.6957186</HighInMetersPerSecond>\n' +
                          '      </SpeedZone>\n' +
                          '      </Target>\n' +
                          '    </Step>\n')
            self.assertEqual(tcx_string, s1.tcx(indent='    ', delta_seconds=3))  # with indent
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        try:  # time step
            s1 = FirstStepBody(name='15 minutes @ 10 minutes per mile', pace=p1, time=t1)
            cmp_string = 'Step: "15 minutes @ 10 minutes per mile"  id = 1\n' + \
                         'type - body  pace - 0:10:00 min per mile\nTime - 0:15:00\n'
            self.assertEqual(cmp_string, str(s1))
            self.assertAlmostEquals(15.0, s1.total(what='time', unit='minute'), 5)
            self.assertAlmostEquals(7920.0, s1.total(unit='ft'))
            tcx_string = ('<Step xsi:type="Step_t">\n' +
                          '  <StepId>1</StepId>\n' +
                          '  <Name>15 minutes @ 10 minutes per mile</Name>\n' +
                          '  <Duration xsi:type="Time_t">\n' +
                          '    <Seconds>900</Seconds>\n' +
                          '  </Duration>\n' +
                          '  <Intensity>Active</Intensity>\n' +
                          '  <Target xsi:type="Speed_t">\n' +
                          '    <SpeedZone xsi:type="CustomSpeedZone_t">\n' +
                          '    <LowInMetersPerSecond>2.6600727</LowInMetersPerSecond>\n' +
                          '    <HighInMetersPerSecond>2.7047798</HighInMetersPerSecond>\n' +
                          '  </SpeedZone>\n' +
                          '  </Target>\n' +
                          '</Step>\n')
            self.assertEqual(tcx_string, s1.tcx())
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        try:  # bad name type
            dummy = FirstStepBody(name=123, pace=p1, time=t1)
            self.fail('Should not get here with bad name')
        except TypeError as ex:
            self.assertEqual('FirstStepBase.__init__ - name must be a string', str(ex))

        try:  # bad pace
            dummy = FirstStepBody(name='dummy', pace='bad pace type', time=t1)
            self.fail('Should not get here with bad pace')
        except TypeError as ex:
            self.assertEqual('FirstStepBody.__init__ - pace must be an instance of FirstPace', str(ex))

        try:  # no distance and no time
            dummy = FirstStepBody(name='dummy', pace=p1)
            self.fail('Should not get here with neither distance nor duration')
        except ValueError as ex:
            self.assertEqual('FirstStepBody.__init__ - Either distance or time must have a value', str(ex))

        try:  # bad distance
            dummy = FirstStepBody(name='dummy', pace=p1, distance=123.45)
            self.fail('Should not get here with bad distance')
        except TypeError as ex:
            self.assertEqual('FirstStepBody.__init__ - distance must be an instance of FirstDistance', str(ex))

        try:  # bad time
            dummy = FirstStepBody(name='dummy', pace=p1, time=987.65)
            self.fail('Should not get here with bad time')
        except TypeError as ex:
            self.assertEqual('FirstStepBody.__init__ - time must be an instance of FirstTime', str(ex))

        try:  # both distance and time
            dummy = FirstStepBody(name='dummy', pace=p1, distance=d1, time=t1)
            self.fail('Should not get here with both distance and time')
        except ValueError as ex:
            self.assertEqual('FirstStepBody.__init__ - cannot set both distance and duration in the same step', str(ex))

    def test_repeat(self):

        FirstStepBase.reset_global_id()

        p1 = FirstPace.from_string('0:10:00 min per mile')
        d1 = FirstDistance.from_string('3 mile')
        t1 = FirstTime.from_string('0:15:00')

        try:
            name = '3 X (3 mile @ 10 min per mile + 15 minutes @ 19 min per mile)'
            s1 = FirstStepRepeat(name=name, repeat=3)
            self.assertEqual('Step: "' + name + '"  id = 0\ntype - repeat  repeat - 3\n', str(s1))
            self.assertAlmostEquals(0.0, s1.total(unit='mile'), 5)
            self.assertAlmostEquals(0.0, s1.total(what='time', unit='minute'))
            tcx_string = ('<Step xsi:type="Repeat_t">\n' +
                          '  <StepId>0</StepId>\n' +
                          '  <Name>3 X (3 mile @ 10 min per mile + 15 minutes @ 19 min per mile)</Name>\n' +
                          '  <Repetitions>3</Repetitions>\n' +
                          '</Step>\n')
            self.assertEqual(tcx_string, s1.tcx())
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        try:
            s2 = FirstStepBody(name='3 mile @ 10 min per mile', pace=p1, distance=d1)
            s3 = FirstStepBody(name='15 minutes @ 19 min per mile', pace=p1, time=t1)
            s1.add_step(s2)
            s1.add_step(s3)
            short = 'Step: "' + name + '"  id = 0\ntype - repeat  repeat - 3\n'
            self.assertEqual(short, str(s1))
            detail = 'Step: "3 X (3 mile @ 10 min per mile + 15 minutes @ 19 min per mile)"\n' +\
                     '  Step: "3 mile @ 10 min per mile"\n' +\
                     '    3.0 mile  at  0:10:00 min per mile\n' +\
                     '  Step: "15 minutes @ 19 min per mile"\n' +\
                     '    0:15:00  at  0:10:00 min per mile\n'
            self.assertEqual(detail, s1.details())
            self.assertAlmostEquals(13.5, s1.total(unit='mile'), 5)
            self.assertAlmostEquals(135.0, s1.total(what='time', unit='minute'))
            tcx_string = ('  <Step xsi:type="Repeat_t">\n' +
                          '    <StepId>0</StepId>\n' +
                          '    <Name>3 X (3 mile @ 10 min per mile + 15 minutes @ 19 min per mile)</Name>\n' +
                          '    <Repetitions>3</Repetitions>\n' +
                          '    <Child xsi:type="Step_t">\n' +
                          '      <StepId>1</StepId>\n' +
                          '      <Name>3 mile @ 10 min per mile</Name>\n' +
                          '      <Duration xsi:type="Distance_t">\n' +
                          '        <Meters>4828</Meters>\n' +
                          '      </Duration>\n' +
                          '      <Intensity>Active</Intensity>\n' +
                          '      <Target xsi:type="Speed_t">\n' +
                          '        <SpeedZone xsi:type="CustomSpeedZone_t">\n' +
                          '        <LowInMetersPerSecond>2.6382689</LowInMetersPerSecond>\n' +
                          '        <HighInMetersPerSecond>2.7277017</HighInMetersPerSecond>\n' +
                          '      </SpeedZone>\n' +
                          '      </Target>\n' +
                          '    </Child>\n' +
                          '    <Child xsi:type="Step_t">\n' +
                          '      <StepId>2</StepId>\n' +
                          '      <Name>15 minutes @ 19 min per mile</Name>\n' +
                          '      <Duration xsi:type="Time_t">\n' +
                          '        <Seconds>900</Seconds>\n' +
                          '      </Duration>\n' +
                          '      <Intensity>Active</Intensity>\n' +
                          '      <Target xsi:type="Speed_t">\n' +
                          '        <SpeedZone xsi:type="CustomSpeedZone_t">\n' +
                          '        <LowInMetersPerSecond>2.6382689</LowInMetersPerSecond>\n' +
                          '        <HighInMetersPerSecond>2.7277017</HighInMetersPerSecond>\n' +
                          '      </SpeedZone>\n' +
                          '      </Target>\n' +
                          '    </Child>\n'
                          '  </Step>\n')
            self.assertEqual(tcx_string, s1.tcx(indent='  ', delta_seconds=10))
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        try:  # bad repeat type
            dummy = FirstStepRepeat(name='bla', repeat='3')
            self.fail('Should not get here with bad repeat type')
        except TypeError as ex:
            self.assertEqual('FirstStepRepeat.__init__ - repeat must be an integer', str(ex))

        try:  # negative repeat
            dummy = FirstStepRepeat(name='bla', repeat=-3)
            self.fail('Should not get here with negative repeat value')
        except ValueError as ex:
            self.assertEqual('FirstStepRepeat.__init__ - repeat must be greater than 0', str(ex))

        try:  # bad child step type
            s1.add_step('bad step')
            self.fail('Should not get here with bad step type')
        except TypeError as ex:
            self.assertEqual('FirstStepRepeat.add_step - step must be an instance of FirstStepBase', str(ex))

    def test_reset(self):

        FirstStepBase.reset_global_id()

        try:
            s0 = FirstStepRepeat(name='before reset', repeat=1)  # id = 0
            s1 = FirstStepRepeat(name='before reset', repeat=1)  # id = 1
            self.assertEqual('Step: "before reset"  id = 1\ntype - repeat  repeat - 1\n', str(s1))
            FirstStepBase.reset_global_id()
            s2 = FirstStepRepeat(name='after reset', repeat=2)  # id = 0
            self.assertEqual('Step: "after reset"  id = 0\ntype - repeat  repeat - 2\n', str(s2))
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))


if __name__ == '__main__':
    unittest.main()
