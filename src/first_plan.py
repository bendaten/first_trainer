import json
from datetime import timedelta
from typing import List, Union, Dict

from first_data import FirstData
from first_race import FirstRace
from first_runner import FirstRunner
from first_step import FirstStepBase
from first_utils import XmlTag
from first_workout import FirstWorkout


class FirstPlan(object):

    # noinspection PyTypeChecker
    def __init__(self, name: str, weekly_schedule: List[int], race: FirstRace = None, runner: FirstRunner = None):

        """
        Constructor
        
        :param name: plan name
        :type name: str
        :param weekly_schedule: a list of 3 days of week where workouts will be scheduled 0 = Mon; 6 = Sun
        :type weekly_schedule: list[int]
        :param race: the target race
        :type race: FirstRace
        :param runner: runner profile
        :type runner: FirstRunner
        :return: instance of FirstPlan
        :rtype: FirstPlan
        """
        if len(weekly_schedule) != 3:
            raise ValueError('Weekly_schedule must have 3 days')
        if weekly_schedule[1] <= weekly_schedule[0] or weekly_schedule[2] <= weekly_schedule[1]:
            raise ValueError('Weekly_schedule items must be sorted')
        if weekly_schedule[0] < 0 or weekly_schedule[2] > 6:
            raise ValueError('Weekly_schedule items must be between 0 (Mon) and 6 (Sun)')

        self.name = name
        self.weekly_schedule = weekly_schedule
        self.race = race
        self.runner = runner
        self.workouts = []

    def __str__(self) -> str:

        return self.details()

    def details(self, level: int = 0, indent: str = '') -> str:

        """
        Text report of a training plan

        :param level: level of details; 0 for minimum
        :type level: int
        :param indent:
        :type indent: str
        :return: plain text string
        :rtype: str
        """
        if level < 0:
            raise ValueError('Level should be greater than or equal to 0')

        week = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
        out_string = '{}Training Plan:\n{}Name - "{}"\n'.format(indent, indent, self.name)
        out_string += '{}Workout days: {}, {}, {}\n'.format(
            indent, week[self.weekly_schedule[0]], week[self.weekly_schedule[1]], week[self.weekly_schedule[2]])
        if self.race is not None:
            out_string += self.race.details(level=level, indent=indent)

        if self.runner is not None:
            out_string += self.runner.details(indent=indent, level=level)

        if len(self.workouts) > 0:
            out_string += '{}Workouts:\n'.format(indent)
            for wo in self.workouts:
                out_string += wo.details(level=level, indent=indent + '  ')
            out_string += '{}Total {} workouts\n'.format(indent,  str(len(self.workouts)))

        return out_string

    def tcx(self) -> str:

        tcx_attr = {'xmlns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
                    'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                    'xsi:schemaLocation': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 ' +
                                          'http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd'}
        tcx = XmlTag(name='TrainingCenterDatabase', attributes=tcx_attr)

        folders = XmlTag(name='Folders')
        tcx.add(item=folders)
        workouts_hdrs = XmlTag(name='Workouts')
        folders.add(item=workouts_hdrs)
        running = XmlTag(name='Running', attributes={'Name': self.name})
        workouts_hdrs.add(item=running)
        for workout in self.workouts:
            wo_ref = XmlTag(name='WorkoutNameRef')
            running.add(item=wo_ref)
            wo_id = XmlTag(name='Id', single_line=True)
            wo_id.add(item=workout.name)
            wo_ref.add(item=wo_id)

        biking = XmlTag(name='Biking', attributes={'Name': 'Biking'}, single_line=True)
        workouts_hdrs.add(item=biking)
        other = XmlTag(name='Other', attributes={'Name': 'Other'}, single_line=True)
        workouts_hdrs.add(item=other)

        workouts = XmlTag(name='Workouts')
        tcx.add(item=workouts)
        for workout in self.workouts:
            workouts.add(item=workout.tcx())

        return tcx.indented_str(doctype='xml')

    def to_json(self, output_unit: Union[str, None] = None) -> Dict:

        result_dict = {'name': self.name}

        week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        result_dict['weekly_schedule'] = [week[day_index] for day_index in self.weekly_schedule]
        if self.race:
            result_dict['race'] = self.race.to_json(output_unit=output_unit)
        if self.runner:
            result_dict['runner'] = self.runner.to_json()
        workouts_list = [workout.to_json(output_unit=output_unit) for workout in self.workouts]
        result_dict['workouts'] = workouts_list

        return result_dict

    def to_html(self, output_unit: Union[str, None] = None) -> str:

        html = XmlTag(name='html')

        header = XmlTag(name='head')
        html.add(header)

        body = XmlTag(name='body')
        html.add(body)

        title = XmlTag(name='h1', single_line=True)
        body.add(title)
        title.add('Training Plan: {}'.format(self.name))

        if self.race:
            body.add(self.race.to_html(output_unit=output_unit))
        if self.runner:
            body.add(self.runner.to_html())

        workouts_section = XmlTag('div')
        body.add(workouts_section)
        schedule_title = XmlTag('h2')
        schedule_title.add('Schedule:')
        workouts_section.add(schedule_title)
        for workout in self.workouts:
            body.add(workout.to_html(output_unit=output_unit))

        return html.indented_str(doctype='html')

    def add_workout(self, workout: FirstWorkout) -> None:

        """
        Add a workout to the plan
        
        :param workout: a workout
        :type workout: FirstWorkout
        """

        self.workouts.append(workout)

    def can_generate_workouts(self) -> bool:

        """
        Check if there are enough data to generate the workouts
        :return: True
        :rtype: bool
        """
        if self.race is None:
            raise ValueError('Must have a race info to generate workouts')
        if self.race.target_time is None:
            raise ValueError('Must have a target time (race) to generate workouts')

        return True

    def generate_workouts(self, data: FirstData) -> None:

        """
        Generate the training plan

        :param data: the database
        :type data: FirstData
        """

        self.can_generate_workouts()
        if self.workouts is not None and len(self.workouts) > 0:
            del self.workouts[:]

        FirstStepBase.reset_global_id()  # ids are auto incremented. Make sure you start from 0

        index = data.race_type_index_by_name(name=self.race.race_type.name)
        plan_instructions = data.plan_instructions[index]
        time_index = data.pace_index_by_race_time(race_time=self.race.target_time, race_name=self.race.race_type.name)
        # TODO for now all plans have 3 weekly key-runs. Add a parameter num_weekly_runs to generalize
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
