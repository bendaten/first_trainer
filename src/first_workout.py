import datetime

from parse import *

from first_data import FirstData
from first_step import FirstStepBase, FirstStepRepeat, FirstStepBody


class FirstWorkout(object):

    # noinspection PyTypeChecker
    def __init__(self, name, workout_date, note=None):

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
        where_am_i = 'FirstWorkout.__init__'
        if not isinstance(name, str):
            raise TypeError(where_am_i + ' - name must be a string')
        if not isinstance(workout_date, datetime.date):
            raise TypeError(where_am_i + ' - date must be a datetime')
        if note is not None and not isinstance(note, str):
            raise ValueError(where_am_i + ' - note must be a string')

        self.name = name
        self.workout_date = workout_date
        self.status = 'scheduled'
        self.note = note
        self.steps = []

    def add_step(self, step):

        """
        Add a step to the workout

        :param step:
        :type step: FirstStepBase
        """
        where_am_i = 'FirstWorkout.add_step'
        if not isinstance(step, FirstStepBase):
            raise TypeError(where_am_i + ' - step must be an instance of FirstStepBase')

        self.steps.append(step)

    statuses = ['scheduled', 'done', 'skipped']

    def set_status(self, status):

        """

        :param status: for now anything
        :type status: str
        """
        where_am_i = 'FirstWorkout.set_status'
        if status in self.statuses:
            self.status = status
        else:
            raise ValueError(where_am_i + ' - Status not in ' + str(self.statuses))

    def __str__(self):

        out_string = self.name + '\n'
        out_string += str(self.workout_date) + '\n'
        out_string += self.status + '\n'

        if len(self.steps) == 0:
            out_string += '\tEmpty workout\n'
        else:
            for step in self.steps:
                out_string += '\t' + str(step)

        return out_string

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
        out_string = indent + '"' + self.name + '"\n'
        out_string += indent + '  ' + self.workout_date.strftime('%a %Y-%m-%d') + '\n'
        out_string += indent + '  ' + self.status + '\n'

        if level > 0:
            if level > 1:
                for step in self.steps:
                    out_string += step.details(indent=indent + '  ')

            out_string += indent + '  Totals: distance = {0:.2f} miles   duration = {1:.2f} minutes\n'. \
                format(self.total(unit='mile'), self.total(what='time', unit='minute'))

        return out_string

    def total(self, what='distance', unit='mile'):

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

    def tcx(self, indent=''):

        """
        Generate a tcx string to download to a Garmin device

        :param indent:
        :type indent: str
        :return: a tcx format for the training plan
        :rtype: str
        """
        tcx_string = indent + '<Workout Sport="Running">\n'
        tcx_string += indent + '  ' + '<Name>' + self.name + '</Name>\n'

        for step in self.steps:
            tcx_string += step.tcx(indent=indent + '  ')

        tcx_string += indent + '  ' + '<ScheduledOn>' + str(self.workout_date) + '</ScheduledOn>\n'
        if self.note is not None:
            tcx_string += indent + '  ' + '<Notes>' + self.note + '</Notes>\n'
        tcx_string += indent + '</Workout>\n'

        return tcx_string

    @staticmethod
    def __parse_simple_steps(data, instructions, time_index, race_pace):

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
    def __parse_steps(data, instructions, time_index, race_pace):

        where_am_i = 'FirstWorkout.__parse_steps'
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
                    raise ValueError(where_am_i + ' - Syntax error: missing nX before (')

                steps += simple_steps
                remainder = remainder[1:]
                step = FirstStepRepeat(name='repeat X ' + str(repeat), repeat=repeat)
                repeat_steps, remainder, close_par = FirstWorkout.__parse_steps(data=data, instructions=remainder,
                                                                                time_index=time_index,
                                                                                race_pace=race_pace)
                if not close_par:
                    raise ValueError(where_am_i + ' - Unbalanced parentheses')
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
            raise ValueError(where_am_i + ' - Syntax error: trailing nX')
        steps += simple_steps

        return steps, remainder, False

    @classmethod
    def from_instructions(cls, instructions, wo_date, data, time_index, race_pace):

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
        where_am_i = 'FirstWorkout.from_instructions'
        # noinspection PyTypeChecker
        if not isinstance(instructions, str):
            raise TypeError(where_am_i + ' - wi is expected to be a string')
        if not isinstance(data, FirstData):
            raise TypeError(where_am_i + ' - data should be an instance of FirstData')

        split1 = instructions.split(' ', 2)
        name = 'Week ' + split1[0] + ' Keyrun ' + split1[1]
        wo = cls(name=name, workout_date=wo_date, note=split1[2])

        steps, remainder, close_par = FirstWorkout.__parse_steps(instructions=split1[2], data=data,
                                                                 time_index=time_index, race_pace=race_pace)
        if len(remainder) > 0:
            raise ValueError(where_am_i + ' - remainder is expected to be empty after all steps are parsed')
        for step in steps:
            wo.add_step(step=step)

        return wo
