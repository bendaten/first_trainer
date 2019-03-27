import json
import unittest
from datetime import date

from first_config import Config
from first_data import FirstData
from first_distance import FirstDistance
from first_pace import FirstPace
from first_plan import FirstPlan
from first_race import FirstRaceType, FirstRace
from first_runner import FirstRunner
from first_step import FirstStepBody, FirstStepRepeat
from first_time import FirstTime
from first_workout import FirstWorkout


class TestFirstPlan(unittest.TestCase):

    def test_to_string(self):

        ws1 = [0, 2, 5]
        ws2 = [1, 3, 6]

        try:  # name only
            p1 = FirstPlan(name='My first marathon training plan', weekly_schedule=ws1)
            self.assertEqual('Training Plan:\nName - "My first marathon training plan"\nWorkout days: Mon, Wed, Sat\n',
                             str(p1))

            file_name = 'cmp_plan1.tcx'
            with open('{}/{}'.format(Config.TEST_RESOURCE_DIR, file_name), 'r') as from_file:
                cmp_string = from_file.read()
                self.assertEqual(cmp_string, p1.tcx())
            cmp_json = {"name": "My first marathon training plan",
                        "weekly_schedule": ["mon", "wed", "sat"],
                        "workouts": []}
            self.assertEqual(cmp_json, p1.to_json())
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        rt1 = FirstRaceType(name='Marathon', distance=FirstDistance.from_string('42.195 km'))
        rd1 = date(year=2017, month=7, day=29)
        r1 = FirstRace(name='SFM', race_type=rt1, race_date=rd1)
        rn1 = FirstRunner(name='DBD')

        try:  # all
            p2 = FirstPlan(name='My first marathon training plan', weekly_schedule=ws2, race=r1, runner=rn1)
            cmp_string = ('Training Plan:\nName - "My first marathon training plan"\nWorkout days: Tue, Thu, Sun\n' +
                          'Race:\n  Name - "SFM" of type Marathon - 42.195 km\nRunner:\n  Name - "DBD"\n')
            self.assertEqual(cmp_string, str(p2))
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

    def test_add_workout(self):

        ws1 = [0, 2, 5]
        rt1 = FirstRaceType(name='Marathon', distance=FirstDistance.from_string('42.195 km'))
        rd1 = date(year=2017, month=7, day=29)
        r1 = FirstRace(name='SFM', race_type=rt1, race_date=rd1)
        rn1 = FirstRunner(name='DBD')
        p1 = FirstPlan(name='My first marathon training plan', weekly_schedule=ws1, race=r1, runner=rn1)

        t_warmup = FirstTime.from_string('0:15:00')
        p_warmup = FirstPace.from_string('0:10:00 min per mile')
        s_warmup = FirstStepBody(name='Warm up', pace=p_warmup, time=t_warmup)

        s_repeat = FirstStepRepeat(name='repeat X 8', repeat=8)
        d_interval = FirstDistance.from_string('400 m')
        p_fast = FirstPace.from_string('0:08:00 min per mile')
        s_fast = FirstStepBody(name='Fast', pace=p_fast, distance=d_interval)
        s_repeat.add_step(s_fast)
        s_slow = FirstStepBody(name='Rest', pace=p_warmup, distance=d_interval)
        s_repeat.add_step(s_slow)

        t_cooldown = FirstTime.from_string('0:10:00')
        s_cooldown = FirstStepBody(name='Cool down', pace=p_warmup, time=t_cooldown)

        wo = FirstWorkout(name='Week 1 Key-run 1', workout_date=date(year=2017, month=6, day=24))
        wo.add_step(step=s_warmup)
        wo.add_step(step=s_repeat)
        wo.add_step(step=s_cooldown)

        try:  # first workout
            p1.add_workout(workout=wo)
            cmp_string = ('Training Plan:\nName - "My first marathon training plan"\n' +
                          'Workout days: Mon, Wed, Sat\nRace:\n' +
                          '  Name - "SFM" of type Marathon - 42.195 km\nRunner:\n  Name - "DBD"\nWorkouts:\n' +
                          '  "Week 1 Key-run 1"\n    Sat 2017-06-24\n    scheduled\n' +
                          'Total 1 workouts\n')
            self.assertEqual(cmp_string, str(p1))

            file_name = 'cmp_plan2.tcx'
            with open('{}/{}'.format(Config.TEST_RESOURCE_DIR, file_name), 'r') as from_file:
                cmp_string = from_file.read()
                self.assertEqual(cmp_string, p1.tcx())
            file_name = 'cmp_plan2.json'
            with open('{}/{}'.format(Config.TEST_RESOURCE_DIR, file_name), 'r') as from_file:
                cmp_json = json.load(from_file)
                self.assertEqual(cmp_json, p1.to_json())
            file_name = 'cmp_plan2_km.json'
            with open('{}/{}'.format(Config.TEST_RESOURCE_DIR, file_name), 'r') as from_file:
                cmp_json = json.load(from_file)
                self.assertEqual(cmp_json, p1.to_json(output_unit='km'))
        except TypeError as ex:
            self.fail(str(ex))

    def test_generate_workouts(self):

        data = FirstData(json_path=Config.DATABASE_JSON)
        ws1 = [0, 2, 5]
        target_time = data.equivalent_time(time_from=FirstTime(minutes=30),
                                           race_index_from=data.race_type_index_by_name('5K'),
                                           race_index_to=data.race_type_index_by_name('Marathon'))
        sf_marathon = FirstRace(race_type=data.get_race_type_by_name('Marathon'),
                                name='San Francisco Marathon',
                                race_date=date(year=2017, month=7, day=23),
                                target_time=target_time)
        me = FirstRunner(name='Daniel BenDavid', age=56, gender='m', email='yossi@gmail.com')
        p1 = FirstPlan(name='My first marathon training plan', weekly_schedule=ws1, race=sf_marathon, runner=me)

        try:  # positive
            p1.generate_workouts(data=data)
            self.assertEqual(48, len(p1.workouts))
            wo = p1.workouts[0]
            self.assertEqual('Week 1 Keyrun 1', wo.name)
            self.assertEqual(3, len(wo.steps))
            step = wo.steps[0]
            self.assertEqual('warmup', step.name)
            self.assertEqual(0, step.step_id)
            self.assertEqual('time', step.get_duration_type())
            self.assertEqual('0:15:00', str(step.time))
            self.assertEqual('0:11:31 min per mile', str(step.pace))

            step = wo.steps[1]
            self.assertEqual('repeat X 3', step.name)
            self.assertEqual(1, step.step_id)
            self.assertEqual(3, step.repeat)  # repeat
            self.assertEqual(2, len(step.steps))
            substep = step.steps[0]
            self.assertEqual('1600m', substep.name)
            self.assertEqual(2, substep.step_id)
            self.assertEqual('distance', substep.get_duration_type())
            self.assertEqual('1600.0 m', str(substep.distance))
            self.assertEqual('0:09:26 min per mile', str(substep.pace))
            substep = step.steps[1]
            self.assertEqual('200 m@RI', substep.name)
            self.assertEqual(3, substep.step_id)
            self.assertEqual('distance', substep.get_duration_type())
            self.assertEqual('200.0 m', str(substep.distance))
            self.assertEqual('0:11:31 min per mile', str(substep.pace))

            step = wo.steps[2]
            self.assertEqual('cooldown', step.name)
            self.assertEqual(4, step.step_id)
            self.assertEqual('time', step.get_duration_type())
            self.assertEqual('0:10:00', str(step.time))
            self.assertEqual('0:11:31 min per mile', str(step.pace))

            file_name = 'cmp_plan_marathon.tcx'
            with open('{}/{}'.format(Config.TEST_RESOURCE_DIR, file_name), 'r') as from_file:
                cmp_string = from_file.read()
                self.assertEqual(cmp_string, p1.tcx())
            file_name = 'cmp_plan_marathon.json'
            with open('{}/{}'.format(Config.TEST_RESOURCE_DIR, file_name), 'r') as from_file:
                cmp_json = json.load(from_file)
                self.assertEqual(cmp_json, p1.to_json())

        except ValueError as vex:
            self.fail(str(vex))
        except TypeError as tex:
            self.fail(str(tex))

        ws1 = [0, 3, 6]
        target_time = data.equivalent_time(time_from=FirstTime(minutes=22, seconds=36),
                                           race_index_from=data.race_type_index_by_name('5K'),
                                           race_index_to=data.race_type_index_by_name('HalfMarathon'))
        sf_half_marathon = FirstRace(race_type=data.get_race_type_by_name('HalfMarathon'),
                                     name='San Francisco Marathon',
                                     race_date=date(year=2017, month=7, day=23),
                                     target_time=target_time)
        me = FirstRunner(name='Daniel BenDavid', age=56, gender='m', email='yossi@gmail.com')
        p2 = FirstPlan(name='San Francisco half-marathon training plan', weekly_schedule=ws1,
                       race=sf_half_marathon, runner=me)

        try:  # positive
            p2.generate_workouts(data=data)

            file_name = 'cmp_plan_half_marathon.tcx'
            from_file = open('{}/{}'.format(Config.TEST_RESOURCE_DIR, file_name))
            cmp_string = from_file.read()
            from_file.close()
            self.assertEqual(cmp_string, p2.tcx())

        except ValueError as vex:
            self.fail(str(vex))
        except TypeError as tex:
            self.fail(str(tex))


if __name__ == '__main__':
    unittest.main()
