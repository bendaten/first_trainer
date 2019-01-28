from typing import Dict

from parse import *

import datetime

from first_data import FirstData
from first_pace import FirstPace
from first_step import FirstStepBase, FirstStepRepeat, FirstStepBody
from first_utils import XmlTag, HtmlTable, HtmlBold


class FirstWorkout(object):

    # noinspection PyTypeChecker
    def __init__(self, name: str, workout_date: datetime.date, note: str = None):

        """
        Constructor

        :param name:
        :type name: str
        :param workout_date:
        :type workout_date: datetime.date
        :param note:
        :type note: str
        :return: instance to FirstWorkout
        :rtype: FirstWorkout
        """

        self.name = name
        self.workout_date = workout_date
        self.status = 'scheduled'
        self.note = note
        self.steps = []

    def add_step(self, step: FirstStepBase) -> None:

        """
        Add a step to the workout

        :param step:
        :type step: FirstStepBase
        """

        self.steps.append(step)

    statuses = ['scheduled', 'done', 'skipped']

    def set_status(self, status: str) -> None:

        """

        :param status: for now anything
        :type status: str
        """
        if status in self.statuses:
            self.status = status
        else:
            raise ValueError('Status not in {}'.format(str(self.statuses)))

    def __str__(self) -> str:

        out_string = '{}\n{}\n{}\n'.format(self.name, str(self.workout_date), self.status)

        if len(self.steps) == 0:
            out_string += '\tEmpty workout\n'
        else:
            for step in self.steps:
                out_string += '\t{}'.format(str(step))

        return out_string

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
        out_string = '{}"{}"\n'.format(indent, self.name)
        out_string += '{}  {}\n'.format(indent, self.workout_date.strftime('%a %Y-%m-%d'))
        out_string += '{}  {}\n'.format(indent, self.status)

        if level > 0:
            if level > 1:
                for step in self.steps:
                    out_string += step.details(indent=indent + '  ')

            out_string += '{0}  Totals: distance = {1:.2f} miles   duration = {2:.2f} minutes\n'.format(
                indent, self.total(unit='mile'), self.total(what='time', unit='minute'))

        return out_string

    def to_json(self) -> Dict:

        result_dict = {'name': self.name,
                       'note': self.note,
                       'status': self.status,
                       'date': str(self.workout_date),
                       'steps': [step.to_json() for step in self.steps],
                       'total_distance': {'distance': self.total(unit='mile'), 'unit': 'mile'},
                       'total_time': {'time': self.total(what='time', unit='minute'), 'unit': 'minute'}}

        return result_dict

    def to_html(self) -> XmlTag:

        section = XmlTag(name='div', attributes={'style': 'margin-left: 20px'})
        title = XmlTag(name='h3', single_line=True)
        title.add('{} - {}'.format(self.name, self.workout_date.strftime('%a, %b %d %Y')))
        section.add(title)
        for step in self.steps:
            section.add(step.to_html())

        table = HtmlTable(attributes={'style': 'border-spacing: 15px 0'})
        section.add(table)
        table.add_header(column_names=['key', 'value'], mute=True)
        table.add_row(values=['Total Distance:', HtmlBold('{:.2f} miles'.format(self.total(unit='mile')))])
        table.add_row(values=['Total Time:', HtmlBold('{:.0f} minutes'.format(self.total(what='time', unit='minute')))])

        return section

    def total(self, what: str = 'distance', unit: str = 'mile') -> float:

        """
        Calculate the total distance or time for this workout

        :param what: distance or time
        :type what: str
        :param unit:
        :type unit: str
        :return: total distance value
        :rtype: float
        """
        result = 0
        for step in self.steps:
            result += step.total(what=what, unit=unit)

        return result

    def tcx(self) -> XmlTag:

        workout = XmlTag(name='Workout', attributes={'Sport': 'Running'})
        name = XmlTag(name='Name', single_line=True)
        name.add(item=self.name)
        workout.add(item=name)

        for step in self.steps:
            workout.add(step.tcx())

        scheduled = XmlTag(name='ScheduledOn', single_line=True)
        workout.add(item=scheduled)
        scheduled.add(item=str(self.workout_date))

        if self.note is not None:
            notes = XmlTag(name='Notes', single_line=True)
            workout.add(item=notes)
            notes.add(item=self.note)

        return workout

    @staticmethod
    def __parse_simple_steps(data: FirstData, instructions: str, time_index: int, race_pace: FirstPace):

        steps = []

        last = instructions.split('#')[-1]
        result = parse('{:d}x', last)
        if result is not None:
            simple_instructions = '#'.join(instructions.split('#')[:-1])
            repeat = result.fixed[0]
        else:
            simple_instructions = instructions
            repeat = -1

        if simple_instructions != '':
            for item in simple_instructions.split('#'):
                steps.append(FirstStepBody.from_instructions(instructions=item, data=data,
                                                             time_index=time_index, rp=race_pace))

        return steps, repeat

    @staticmethod
    def __parse_steps(data: FirstData, instructions: str, time_index: int, race_pace: FirstPace):

        steps = []
        simple_instructions = ''
        remainder = instructions

        while remainder:
            char = remainder[0]
            if char == '(':
                simple_steps, repeat = FirstWorkout.__parse_simple_steps(data=data, instructions=simple_instructions,
                                                                         time_index=time_index, race_pace=race_pace)
                simple_instructions = ''
                if repeat < 1:
                    raise ValueError('Syntax error: missing nX before (')

                steps += simple_steps
                remainder = remainder[1:]
                step = FirstStepRepeat(name='repeat X ' + str(repeat), repeat=repeat)
                repeat_steps, remainder, close_par = FirstWorkout.__parse_steps(data=data, instructions=remainder,
                                                                                time_index=time_index,
                                                                                race_pace=race_pace)
                if not close_par:
                    raise ValueError('Unbalanced parentheses')
                step.set_steps(steps=repeat_steps)
                steps.append(step)
            elif char == ')':
                remainder = remainder[1:]
                simple_steps, repeat = FirstWorkout.__parse_simple_steps(data=data, instructions=simple_instructions,
                                                                         time_index=time_index, race_pace=race_pace)

                steps += simple_steps
                return steps, remainder, True
            else:
                simple_instructions += char
                remainder = remainder[1:]

        simple_steps, repeat = FirstWorkout.__parse_simple_steps(data=data, instructions=simple_instructions,
                                                                 time_index=time_index, race_pace=race_pace)
        if repeat > 0:
            raise ValueError('Syntax error: trailing nX')
        steps += simple_steps

        return steps, remainder, False

    @classmethod
    def from_instructions(cls, instructions: str, wo_date: datetime.date,
                          data: FirstData, time_index: int, race_pace: FirstPace):

        """
        Constructor - create workout from instructions
        :param instructions: see test_workout.py for examples
        :type instructions: str
        :param wo_date:
        :type wo_date: datetime.date
        :param data:
        :type data: FirstData
        :param time_index:
        :type time_index: int
        :param race_pace:
        :type race_pace: FirstPace
        :return: instance of FirstWorkout
        :rtype: FirstWorkout
        """

        split1 = instructions.split(' ', 2)
        name = 'Week {} Keyrun {}'.format(split1[0], split1[1])
        wo = cls(name=name, workout_date=wo_date, note=split1[2])

        steps, remainder, close_par = FirstWorkout.__parse_steps(instructions=split1[2], data=data,
                                                                 time_index=time_index, race_pace=race_pace)
        if len(remainder) > 0:
            raise ValueError('remainder is expected to be empty after all steps are parsed')
        for step in steps:
            wo.add_step(step=step)

        return wo
