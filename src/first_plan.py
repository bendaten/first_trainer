from datetime import timedelta

from first_data import FirstData
from first_race import FirstRace
from first_runner import FirstRunner
from first_step import FirstStepBase
from first_workout import FirstWorkout


class FirstPlan(object):

    # noinspection PyTypeChecker
    def __init__(self, name, weekly_schedule, race=None, runner=None):

        """
        Constructor
        
        :param name: plan name
        :type name: str
        :param weekly_schedule: a list of 3 days of week where workouts will be scheduled 0 = Mon; 6 = Sun
        :type weekly_schedule: list
        :param race: the target race
        :type race: FirstRace
        :param runner: runner profile
        :type runner: FirstRunner
        :return: instance of FirstPlan
        :rtype: FirstPlan
        """
        where_am_i = 'FirstPlan.__init__'
        if not isinstance(name, basestring):
            raise TypeError(where_am_i + ' - name must be a string')
        if not isinstance(weekly_schedule, list):
            raise TypeError(where_am_i + ' - weekly_schedule must be a list')
        if len(weekly_schedule) != 3:
            raise ValueError(where_am_i + ' - weekly_schedule must have 3 days')
        if (not isinstance(weekly_schedule[0], int) or
                not isinstance(weekly_schedule[1], int) or
                not isinstance(weekly_schedule[2], int)):
            raise ValueError(where_am_i + ' - weekly_schedule items must be integers')
        if weekly_schedule[1] <= weekly_schedule[0] or weekly_schedule[2] <= weekly_schedule[1]:
            raise ValueError(where_am_i + ' - weekly_schedule items must be sorted')
        if weekly_schedule[0] < 0 or weekly_schedule[2] > 6:
            raise ValueError(where_am_i + ' - weekly_schedule items must be between 0 (Mon) and 6 (Sun)')
        if race is not None and not isinstance(race, FirstRace):
            raise TypeError(where_am_i + ' - race must be an instance of FirstRace')
        if runner is not None and not isinstance(runner, FirstRunner):
            raise TypeError(where_am_i + ' - runner must be an instance of FirstRunner')

        self.name = name
        self.weekly_schedule = weekly_schedule
        self.race = race
        self.runner = runner
        self.workouts = []

    def __str__(self):

        return self.details()

    def details(self, level=0, indent=''):

        """
        Text report of a training plan

        :param level: level of details; 0 for minimum
        :type level: int
        :param indent:
        :type indent: str
        :return: plain text string
        :rtype: str
        """
        where_am_i = 'FirstPlan.details'
        if not isinstance(level, int):
            raise TypeError(where_am_i + ' - level should be an integer')
        if level < 0:
            raise ValueError(where_am_i + ' - level should be greater than or equal to 0')

        week = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
        out_string = indent + 'Training Plan:\n' + indent + 'Name - "' + self.name + '"\n'
        out_string += indent + ('Workout days: ' + week[self.weekly_schedule[0]] + ', ' +
                                week[self.weekly_schedule[1]] + ', ' +
                                week[self.weekly_schedule[2]] + '\n')
        if self.race is not None:
            out_string += self.race.details(level=level, indent=indent)

        if self.runner is not None:
            out_string += self.runner.details(indent=indent, level=level)

        if len(self.workouts) > 0:
            out_string += indent + 'Workouts:\n'
            for wo in self.workouts:
                out_string += wo.details(level=level, indent=indent + '  ')
            out_string += indent + 'Total ' + str(len(self.workouts)) + ' workouts\n'

        return out_string

    def tcx(self):

        """
        Generate a tcx string to download to a Garmin device

        :return: a tcx format for the training plan
        :rtype: str
        """
        tcx_string = '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n' + \
                     '<TrainingCenterDatabase xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2" ' + \
                     'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' + \
                     'xsi:schemaLocation="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 ' + \
                     'http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd">\n\n'

        tcx_string += '  <Folders>\n'
        tcx_string += '    <Workouts>\n'
        tcx_string += '      <Running Name="' + self.name + '">\n'

        for workout in self.workouts:
            tcx_string += '        <WorkoutNameRef>\n'
            tcx_string += '          <Id>' + workout.name + '</Id>\n'
            tcx_string += '        </WorkoutNameRef>\n'

        tcx_string += '      </Running>\n'
        tcx_string += '      <Biking Name="Biking"/>\n'
        tcx_string += '      <Other Name="Other"/>\n'
        tcx_string += '    </Workouts>\n'
        tcx_string += '  </Folders>\n\n'

        tcx_string += '  <Workouts>\n'

        for workout in self.workouts:
            tcx_string += workout.tcx(indent='    ')

        tcx_string += '  </Workouts>\n\n'

        tcx_string += '</TrainingCenterDatabase>\n'

        return tcx_string

    def add_workout(self, workout):

        """
        Add a workout to the plan
        
        :param workout: a workout
        :type workout: FirstWorkout
        """
        where_am_i = 'FirstPlan.add_workout'
        if not isinstance(workout, FirstWorkout):
            raise TypeError(where_am_i + ' - workout must be an instance of FirstWorkout')

        self.workouts.append(workout)

    def can_generate_workouts(self):

        """
        Check if there are enough data to generate the workouts
        :return: True
        :rtype: bool
        """
        where_am_i = 'FirstPlan.can_generate_workouts'
        if self.race is None:
            raise ValueError(where_am_i + ' - must have a race info to generate workouts')
        if self.race.target_time is None:
            raise ValueError(where_am_i + ' - must have a target time (race) to generate workouts')

        return True

    def generate_workouts(self, data):

        """
        Generate the training plan

        :param data: the database
        :type data: FirstData
        """
        where_am_i = 'FirstPlan.generate_workouts'
        if not isinstance(data, FirstData):
            raise TypeError(where_am_i + ' - data must be an instance of FirstData')

        self.can_generate_workouts()
        if self.workouts is not None and len(self.workouts) > 0:
            del self.workouts[:]

        FirstStepBase.reset_global_id()  # ids are auto incremented. Make sure you start from 0

        index = data.race_type_index_by_name(self.race.race_type.name)
        plan_instructions = data.plan_instructions[index]
        time_index = data.pace_index_by_race_time(race_time=self.race.target_time, race_name=self.race.race_type.name)
        # TODO for now all plans have 3 weekly keyruns. Add a parameter num_weekly_runs to generalize
        num_weekly_runs = 3
        num_weeks = len(plan_instructions.instructions) / num_weekly_runs
        start_date = self.race.race_date - timedelta(weeks=(num_weeks-1))
        dow = start_date.weekday()
        delta = dow - self.weekly_schedule[0]
        start_date = start_date - timedelta(days=delta)
        delta = self.weekly_schedule[1] - self.weekly_schedule[0]
        second_date = start_date + timedelta(days=delta)
        delta = self.weekly_schedule[2] - self.weekly_schedule[0]
        third_date = start_date + timedelta(days=delta)
        week_dates = [start_date, second_date, third_date]
        weekday_index = 0
        race_pace = self.race.race_pace()
        for wi in plan_instructions.instructions:
            self.workouts.append(FirstWorkout.from_instructions(instructions=wi, wo_date=week_dates[weekday_index],
                                                                data=data, time_index=time_index,
                                                                race_pace=race_pace))
            week_dates[weekday_index] += timedelta(days=7)
            weekday_index = (weekday_index + 1) % num_weekly_runs
        if self.workouts[-1].workout_date != self.race.race_date:
            self.workouts[-1].workout_date = self.race.race_date
        if self.workouts[-2].workout_date >= self.race.race_date:
            self.workouts[-2].workout_date -= timedelta(days=1)
