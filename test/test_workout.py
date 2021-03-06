import json
import unittest
from datetime import date

from first_config import Config
from first_data import FirstData
from first_distance import FirstDistance
from first_pace import FirstPace
from first_step import FirstStepBody, FirstStepRepeat, FirstStepBase
from first_time import FirstTime
from first_utils import FirstUtils
from first_workout import FirstWorkout


class TestFirstWorkout(unittest.TestCase):

    def test_to_string_new(self):

        pass

    def test_steps(self):

        FirstStepBase.reset_global_id()
        t_warmup = FirstTime.from_string(string='0:15:00')
        p_warmup = FirstPace.from_string(str_input='0:10:00 min per mile')
        s_warmup = FirstStepBody(name='Warm up', pace=p_warmup, time=t_warmup)

        s_intervals = FirstStepRepeat(name='Intervals', repeat=8)
        d_interval = FirstDistance.from_string(string='400 m')
        p_fast = FirstPace.from_string(str_input='0:08:00 min per mile')
        s_fast = FirstStepBody(name='Fast', pace=p_fast, distance=d_interval)
        s_slow = FirstStepBody(name='Rest', pace=p_warmup, distance=d_interval)
        s_intervals.add_step(step=s_fast)
        s_intervals.add_step(step=s_slow)

        t_cooldown = FirstTime.from_string(string='0:10:00')
        s_cooldown = FirstStepBody(name='Cool down', pace=p_warmup, time=t_cooldown)

        try:  # positive
            wo = FirstWorkout(name='Week 1 Key-run 1', workout_date=date(2017, 6, 24))
            wo.add_step(step=s_warmup)
            wo.add_step(step=s_intervals)
            wo.add_step(step=s_cooldown)
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
            cmp_string = '"Week 1 Key-run 1"\n' + \
                         '  Sat 2017-06-24\n' + \
                         '  scheduled\n' + \
                         '  Step: "Warm up"\n' + \
                         '    0:15:00  at  0:10:00 min per mile\n' + \
                         '  Step: "Intervals"\n' + \
                         '    Step: "Fast"\n' + \
                         '      400.0 m  at  0:08:00 min per mile\n' + \
                         '    Step: "Rest"\n' + \
                         '      400.0 m  at  0:10:00 min per mile\n' + \
                         '  Step: "Cool down"\n' + \
                         '    0:10:00  at  0:10:00 min per mile\n' + \
                         '  Totals: distance = 6.48 miles   duration = 60.73 minutes\n'
            self.assertEqual(cmp_string, wo.details(level=2))
            total_distance_miles = 15.0 / 10 + 8 * (800 / 1609.344) + 10.0 / 10
            self.assertAlmostEqual(total_distance_miles, wo.total(), 5)
            total_distance_km = total_distance_miles * 1.609344
            self.assertAlmostEqual(total_distance_km, wo.total(unit='km'), 5)
            total_time_minutes = 15.0 + 8 * (
                    round(400 / 1609.344 * 8 * 60) / 60 + round(400 / 1609.344 * 10 * 60) / 60) + 10.0
            self.assertAlmostEqual(total_time_minutes, wo.total(what='time', unit='minute'), 5)
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
                          '        <LowInMetersPerSecond>2.6600727</LowInMetersPerSecond>\n' +
                          '        <HighInMetersPerSecond>2.7047798</HighInMetersPerSecond>\n' +
                          '      </SpeedZone>\n' +
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
                          '          <LowInMetersPerSecond>3.3182351</LowInMetersPerSecond>\n' +
                          '          <HighInMetersPerSecond>3.3880926</HighInMetersPerSecond>\n' +
                          '        </SpeedZone>\n' +
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
                          '          <LowInMetersPerSecond>2.6600727</LowInMetersPerSecond>\n' +
                          '          <HighInMetersPerSecond>2.7047798</HighInMetersPerSecond>\n' +
                          '        </SpeedZone>\n' +
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
                          '        <LowInMetersPerSecond>2.6600727</LowInMetersPerSecond>\n' +
                          '        <HighInMetersPerSecond>2.7047798</HighInMetersPerSecond>\n' +
                          '      </SpeedZone>\n' +
                          '    </Target>\n' +
                          '  </Step>\n')
            tcx_string_end = ('  <ScheduledOn>2017-06-24</ScheduledOn>\n' +
                              '</Workout>')
            cmp_string = tcx_string + tcx_string_end
            self.assertEqual(cmp_string, wo.tcx().indented_str())
            steps = [{'name': 'Warm up',
                      'pace': {'length_unit': 'mile',
                               'pace': '0:10:00 min per mile',
                               'time': {'seconds': 600, 'time': '0:10:00'}},
                      'time': {'seconds': 900, 'time': '0:15:00'}},
                     {'name': 'Intervals',
                      'repeat': 8,
                      'steps': [{'distance': {'distance': 400.0, 'unit': 'm'},
                                 'name': 'Fast',
                                 'pace': {'length_unit': 'mile',
                                          'pace': '0:08:00 min per mile',
                                          'time': {'seconds': 480, 'time': '0:08:00'}}},
                                {'distance': {'distance': 400.0, 'unit': 'm'},
                                 'name': 'Rest',
                                 'pace': {'length_unit': 'mile',
                                          'pace': '0:10:00 min per mile',
                                          'time': {'seconds': 600, 'time': '0:10:00'}}}]},
                     {'name': 'Cool down',
                      'pace': {'length_unit': 'mile',
                               'pace': '0:10:00 min per mile',
                               'time': {'seconds': 600, 'time': '0:10:00'}},
                      'time': {'seconds': 600, 'time': '0:10:00'}}]
            cmp_json = {'date': '2017-06-24',
                        'name': 'Week 1 Key-run 1',
                        'note': None,
                        'status': 'scheduled',
                        'steps': steps,
                        'total_distance': {'distance': 6.47678, 'unit': 'mile'},
                        'total_time': {'time': 60.73333, 'unit': 'minute'}}
            FirstUtils.assert_deep_almost_equal(self, cmp_json, wo.to_json(), 5)
            km_steps = [{'name': 'Warm up',
                         'pace': {'length_unit': 'km',
                                  'pace': '0:06:13 min per km',
                                  'time': {'seconds': 373, 'time': '0:06:13'}},
                         'time': {'seconds': 900, 'time': '0:15:00'}},
                        {'name': 'Intervals',
                         'repeat': 8,
                         'steps': [{'distance': {'distance': 0.4, 'unit': 'km'},
                                    'name': 'Fast',
                                    'pace': {'length_unit': 'km',
                                             'pace': '0:04:58 min per km',
                                             'time': {'seconds': 298, 'time': '0:04:58'}}},
                                   {'distance': {'distance': 0.4, 'unit': 'km'},
                                    'name': 'Rest',
                                    'pace': {'length_unit': 'km',
                                             'pace': '0:06:13 min per km',
                                             'time': {'seconds': 373, 'time': '0:06:13'}}}]},
                        {'name': 'Cool down',
                         'pace': {'length_unit': 'km',
                                  'pace': '0:06:13 min per km',
                                  'time': {'seconds': 373, 'time': '0:06:13'}},
                         'time': {'seconds': 600, 'time': '0:10:00'}}]
            cmp_json['steps'] = km_steps
            cmp_json['total_distance'] = {'distance': 10.42336, 'unit': 'km'}
            FirstUtils.assert_deep_almost_equal(self, cmp_json, wo.to_json(output_unit='km'), 5)
            cmp_html = ('<div style="margin-left: 20px">\n' +
                        '  <h3>Week 1 Key-run 1 - Sat, Jun 24 2017</h3>\n' +
                        '  <div style="margin-left: 20px">\n' +
                        '    <p>\n' +
                        '      Warm up - 0:15:00 at 0:10:00 min per mile\n' +
                        '    </p>\n' +
                        '  </div>\n' +
                        '  <div style="margin-left: 20px">\n' +
                        '    <p>\n' +
                        '      Repeat 8 times:\n' +
                        '    </p>\n' +
                        '    <div style="margin-left: 20px">\n' +
                        '      <p>\n' +
                        '        Fast - 400.000 m at 0:08:00 min per mile\n' +
                        '      </p>\n' +
                        '    </div>\n' +
                        '    <div style="margin-left: 20px">\n' +
                        '      <p>\n' +
                        '        Rest - 400.000 m at 0:10:00 min per mile\n' +
                        '      </p>\n' +
                        '    </div>\n' +
                        '  </div>\n' +
                        '  <div style="margin-left: 20px">\n' +
                        '    <p>\n' +
                        '      Cool down - 0:10:00 at 0:10:00 min per mile\n' +
                        '    </p>\n' +
                        '  </div>\n' +
                        '  <table style="border-spacing: 15px 0">\n' +
                        '    <tbody>\n' +
                        '      <tr>\n' +
                        '        <td>Total Distance:</td>\n' +
                        '        <td><b>6.48 mile</b></td>\n' +
                        '      </tr>\n' +
                        '      <tr>\n' +
                        '        <td>Total Time:</td>\n' +
                        '        <td><b>61 minutes</b></td>\n' +
                        '      </tr>\n' +
                        '    </tbody>\n' +
                        '  </table>\n' +
                        '</div>')
            self.assertEqual(cmp_html, wo.to_html().indented_str())
            cmp_html = ('<div style="margin-left: 20px">\n' +
                        '  <h3>Week 1 Key-run 1 - Sat, Jun 24 2017</h3>\n' +
                        '  <div style="margin-left: 20px">\n' +
                        '    <p>\n' +
                        '      Warm up - 0:15:00 at 0:06:13 min per km\n' +
                        '    </p>\n' +
                        '  </div>\n' +
                        '  <div style="margin-left: 20px">\n' +
                        '    <p>\n' +
                        '      Repeat 8 times:\n' +
                        '    </p>\n' +
                        '    <div style="margin-left: 20px">\n' +
                        '      <p>\n' +
                        '        Fast - 0.400 km at 0:04:58 min per km\n' +
                        '      </p>\n' +
                        '    </div>\n' +
                        '    <div style="margin-left: 20px">\n' +
                        '      <p>\n' +
                        '        Rest - 0.400 km at 0:06:13 min per km\n' +
                        '      </p>\n' +
                        '    </div>\n' +
                        '  </div>\n' +
                        '  <div style="margin-left: 20px">\n' +
                        '    <p>\n' +
                        '      Cool down - 0:10:00 at 0:06:13 min per km\n' +
                        '    </p>\n' +
                        '  </div>\n' +
                        '  <table style="border-spacing: 15px 0">\n' +
                        '    <tbody>\n' +
                        '      <tr>\n' +
                        '        <td>Total Distance:</td>\n' +
                        '        <td><b>10.42 km</b></td>\n' +
                        '      </tr>\n' +
                        '      <tr>\n' +
                        '        <td>Total Time:</td>\n' +
                        '        <td><b>61 minutes</b></td>\n' +
                        '      </tr>\n' +
                        '    </tbody>\n' +
                        '  </table>\n' +
                        '</div>')
            self.assertEqual(cmp_html, wo.to_html(output_unit='km').indented_str())

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
            steps.append({'name': 'Warm up',
                          'pace': {'length_unit': 'mile',
                                   'pace': '0:10:00 min per mile',
                                   'time': {'seconds': 600, 'time': '0:10:00'}},
                          'time': {'seconds': 900, 'time': '0:15:00'}})
            cmp_json['steps'] = steps
            cmp_json['total_distance'] = {'distance': 7.97678, 'unit': 'mile'}
            cmp_json['total_time'] = {'time': 75.73333, 'unit': 'minute'}
            FirstUtils.assert_deep_almost_equal(self, cmp_json, wo.to_json(), 5)
            km_steps.append({'name': 'Warm up',
                             'pace': {'length_unit': 'km',
                                      'pace': '0:06:13 min per km',
                                      'time': {'seconds': 373, 'time': '0:06:13'}},
                             'time': {'seconds': 900, 'time': '0:15:00'}})
            cmp_json['steps'] = km_steps
            cmp_json['total_distance'] = {'distance': 12.83738, 'unit': 'km'}
            FirstUtils.assert_deep_almost_equal(self, cmp_json, wo.to_json(output_unit='km'), 5)
        except ValueError as vex:
            self.fail(str(vex))
        except TypeError as tex:
            self.fail(str(tex))

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
            self.assertEqual("Status not in ['scheduled', 'done', 'skipped']", str(ex))

    def test_from_instructions(self):

        rp = FirstPace.from_string(str_input='0:09:35 min per mile')
        ti = 50
        wo_date = date(2017, 8, 21)
        data = FirstData(json_path=Config.DATABASE_JSON)
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
            self.assertAlmostEqual(1.59858, step.total(what='distance', unit='mile'), 5)

            step = wo1.steps[2]
            self.assertEqual(4, step.step_id)
            self.assertEqual('cooldown', step.name)
            self.assertEqual('0:09:23 min per mile', str(step.pace))
            self.assertEqual(None, step.distance)
            self.assertEqual('time', step.get_duration_type())
            self.assertEqual('0:10:00', str(step.time))
            self.assertEqual(600.0, step.total(what='time', unit='second'))
            self.assertAlmostEqual(1.06572, step.total(what='distance', unit='mile'), 5)

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
            self.assertAlmostEqual(7.25, substep.total(what='time', unit='minute'), 5)
            self.assertAlmostEqual(0.99419, substep.total(what='distance', unit='mile'), 5)
            substep = step.steps[1]
            self.assertEqual(3, substep.step_id)
            self.assertEqual('200 m@RI', substep.name)
            self.assertEqual('0:09:23 min per mile', str(substep.pace))
            self.assertEqual(None, substep.time)
            self.assertEqual('distance', substep.get_duration_type())
            self.assertEqual('200.0 m', str(substep.distance))
            self.assertAlmostEqual(1.16667, substep.total(what='time', unit='minute'), 5)
            self.assertAlmostEqual(0.12427, substep.total(what='distance', unit='mile'), 5)

            # Repeat steps totals
            self.assertAlmostEqual(25.25, step.total(what='time', unit='minute'), 5)
            self.assertAlmostEqual(3.35540, step.total(what='distance', unit='mile'), 5)

            # Workout totals
            self.assertAlmostEqual(50.25, wo1.total(what='time', unit='minute'), 5)
            self.assertAlmostEqual(6.01970, wo1.total(what='distance', unit='mile'), 5)

            # tcx
            file_name = 'cmp_workout1.tcx'
            with open('{}/{}'.format(Config.TEST_RESOURCE_DIR, file_name), 'r') as from_file:
                cmp_string = from_file.read()
                self.assertEqual(cmp_string, wo1.tcx().indented_str())

            # json
            file_name = 'cmp_workout1.json'
            with open('{}/{}'.format(Config.TEST_RESOURCE_DIR, file_name), 'r') as from_file:
                cmp_json = json.load(from_file)
                FirstUtils.assert_deep_almost_equal(self, cmp_json, wo1.to_json(), 5)

            file_name = 'cmp_workout1_km.json'
            with open('{}/{}'.format(Config.TEST_RESOURCE_DIR, file_name), 'r') as from_file:
                cmp_json = json.load(from_file)
                FirstUtils.assert_deep_almost_equal(self, cmp_json, wo1.to_json(output_unit='km'), 5)

            # html
            file_name = 'cmp_workout1.html'
            with open('{}/{}'.format(Config.TEST_RESOURCE_DIR, file_name), 'r') as from_file:
                cmp_html = from_file.read()
                self.assertEqual(cmp_html, wo1.to_html().indented_str())

            file_name = 'cmp_workout1_km.html'
            with open('{}/{}'.format(Config.TEST_RESOURCE_DIR, file_name), 'r') as from_file:
                cmp_html = from_file.read()
                self.assertEqual(cmp_html, wo1.to_html(output_unit='km').indented_str())

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
            self.assertAlmostEqual(1.16667, subsubstep.total(what='time', unit='minute'), 5)
            self.assertAlmostEqual(0.12427, subsubstep.total(what='distance', unit='mile'), 5)

            self.assertAlmostEqual(4.66667, substep.total(what='time', unit='minute'), 5)
            self.assertAlmostEqual(0.4971, substep.total(what='distance', unit='mile'), 5)

            self.assertAlmostEqual(46.2, step.total(what='time', unit='minute'), 5)
            self.assertAlmostEqual(5.96516, step.total(what='distance', unit='mile'), 5)

            self.assertAlmostEqual(71.2, wo2.total(what='time', unit='minute'), 5)
            self.assertAlmostEqual(8.62946, wo2.total(what='distance', unit='mile'), 5)

            file_name = 'cmp_workout2.tcx'
            with open('{}/{}'.format(Config.TEST_RESOURCE_DIR, file_name), 'r') as from_file:
                cmp_string = from_file.read()
                self.assertEqual(cmp_string, wo2.tcx().indented_str())

        except ValueError as ex:
            self.fail(str(ex))

        instructions = '1 1 warmup#3x(1600m#200 m@RI#cooldown'
        try:  # unbalanced parentheses
            _ = FirstWorkout.from_instructions(instructions=instructions, wo_date=wo_date,
                                               data=data, time_index=ti, race_pace=rp)
        except ValueError as ex:
            self.assertEqual('Unbalanced parentheses', str(ex))


if __name__ == '__main__':
    unittest.main()
