import datetime

from parse import *

from first_data import FirstData
from first_pace import FirstPace
from first_step import FirstStepBase, FirstStepRepeat, FirstStepBody


class FirstWorkout(object):

    # noinspection PyTypeChecker
    def __init__(self, name: str, workout_date: datetime.date, note: str =None):

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

    def details(self, level: int =0, indent: str ='') -> str:

        """
        Text report of a training plan

        :param level: level of details; 0 for minimum
        :type level: int
        :param indent:
        :type indent: str
        :return: plain text string
        :rtype: str
        """
        out_string = indent + '{}"{}"\n'.format(indent, self.name)
        out_string += indent + '{}  {}\n'.format(indent, self.workout_date.strftime('%a %Y-%m-%d'))
        out_string += indent + '{}  {}\n'.format(indent, self.status)

        if level > 0:
            if level > 1:
                for step in self.steps:
                    out_string += step.details(indent=indent + '  ')

            out_string += '{0}  Totals: distance = {1:.2f} miles   duration = {2:.2f} minutes\n'.format(
                indent, self.total(unit='mile'), self.total(what='time', unit='minute'))

        return out_string

    def total(self, what: str ='distance', unit: str ='mile') -> float:

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

    def tcx(self, indent: str ='') -> str:

        """
        Generate a tcx string to download to a Garmin device

        :param indent:
        :type indent: str
        :return: a tcx format for the training plan
        :rtype: str
        """
        tcx_string = '{}<Workout Sport="Running">\n'.format(indent)
        tcx_string += '{}  <Name>{}</Name>\n'.format(indent, self.name)

        for step in self.steps:
            tcx_string += step.tcx(indent=indent + '  ')

        tcx_string += '{}  <ScheduledOn>{}</ScheduledOn>\n'.format(indent, str(self.workout_date))
        if self.note is not None:
            tcx_string += '{}  <Notes>{}</Notes>\n'.format(indent, self.note)
        tcx_string += '{}</Workout>\n'.format(indent)

        return tcx_string

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
