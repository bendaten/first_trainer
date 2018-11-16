import copy
from typing import List

from first_data import FirstData
from first_distance import FirstDistance
from first_pace import FirstPace
from first_time import FirstTime


class FirstStepBase(object):

    """Base class for steps
    Manage the step name and id.
    ids start with 0 and incremented with each new instance.
    You should reset the global id for each plan to restart the counting"""

    __global_id = 0  # static

    @staticmethod
    def reset_global_id() -> None:  # reset before each training plan

        """
        Reset the global id
        """
        FirstStepBase.__global_id = 0

    # noinspection PyTypeChecker
    def __init__(self, name: str):

        self.step_id = FirstStepBase.__global_id
        FirstStepBase.__global_id += 1
        self.name = name

    def __str__(self) -> str:

        return 'Step: "{}"  id = {}\n'.format(self.name, self.step_id)

    def details(self, indent: str ='') -> str:

        return '{}Step: "{}"\n'.format(indent, self.name)

    def tcx_start(self, child: bool, step_type: str, indent: str) -> str:

        if child:
            token = 'Child'
        else:
            token = 'Step'

        tcx_string = '{}<{} xsi:type="{}">\n'.format(indent, token, step_type)
        tcx_string += '{}  <StepId>{}</StepId>\n'.format(indent, str(self.step_id))
        tcx_string += '{}  <Name>{}</Name>\n'.format(indent, self.name)

        return tcx_string


class FirstStepRepeat(FirstStepBase):

    # noinspection PyTypeChecker
    def __init__(self, name: str, repeat: int =1):

        """
        Constructor
        
        :param name: step name
        :type name: str
        :param repeat: number of repetitions of the child steps
        :type repeat: int
        :return: instance of FirstStepRepeat
        :rtype: FirstStepRepeat
        """
        if repeat < 1:
            raise ValueError('repeat must be greater than 0')

        FirstStepBase.__init__(self, name=name)

        self.repeat = repeat
        self.steps = []

    @staticmethod
    def __get_type() -> str:

        return 'repeat'

    def __str__(self) -> str:

        return '{}type - {}  repeat - {}\n'.format(FirstStepBase.__str__(self), self.__get_type(), str(self.repeat))

    def details(self, level: int =0, indent: str ='') -> str:

        """
        Generate a detailed text report

        :param level: level of details; 0 for minimum
        :type level: int
        :param indent:
        :type indent: str
        :return: plain text string
        :rtype: str
        """
        out_string = FirstStepBase.details(self, indent=indent)
        for child in self.steps:
            out_string += child.details(indent=indent + '  ')

        return out_string

    def tcx(self, indent: str ='', child: bool =False, delta_seconds: int =5) -> str:

        """
        Generate a tcx string to download to a Garmin device

        :param indent:
        :type indent: str
        :param child: is a child of a repeat step (can be recursive)
        :type child: bool
        :param delta_seconds: for speed tolerance
        :type delta_seconds: int
        :return: a tcx format for the training plan
        :rtype: str
        """
        tcx_string = FirstStepBase.tcx_start(self, child=child, step_type='Repeat_t', indent=indent)

        tcx_string += '{}  <Repetitions>{}</Repetitions>\n'.format(indent, str(self.repeat))

        for step in self.steps:
            tcx_string += step.tcx(indent=indent + '  ', child=True, delta_seconds=delta_seconds)

        if child:
            tcx_string += indent + '</Child>\n'
        else:
            tcx_string += indent + '</Step>\n'

        return tcx_string

    def add_step(self, step: FirstStepBase) -> None:

        """
        Add a child step
        
        :param step: the step to be added
        :type step: FirstStepBase
        """

        self.steps.append(step)
        
    def set_steps(self, steps: List[FirstStepBase]) -> None:

        """
        Set the steps to be repeated

        :param steps: list of steps
        :type steps: list[FirstStepBase]
        """
        self.steps = steps

    def total(self, what: str ='distance', unit: str ='m') -> float:

        """
        Calculate the total distance or time for this step
        
        :param what: distance or time
        :type what: str
        :param unit: 
        :type unit: str
        :return: total distance value
        :rtype: float
        """
        value = 0

        for step in self.steps:
            value += step.total(what=what, unit=unit)

        return value * self.repeat


class FirstStepBody(FirstStepBase):

    # noinspection PyTypeChecker
    def __init__(self, name: str, pace: FirstPace, intensity: str ='Active',
                 distance: FirstDistance =None, time: FirstTime =None):

        """
        Constructor
        
        :param name: step name
        :type name: str
        :param pace: running pace
        :type pace: FirstPace
        :param intensity: TBD
        :type intensity: str
        :param distance: the segment distance
        :type distance: FirstDistance
        :param time: the segment duration
        :type time: FirstTime
        """
        if distance is None and time is None:
            raise ValueError('Either distance or time must have a value')
        if distance is not None and time is not None:
            raise ValueError('Cannot set both distance and duration in the same step')

        FirstStepBase.__init__(self, name=name)

        self.pace = pace
        self.intensity = intensity
        self.distance = distance
        self.time = time

    @staticmethod
    def __get_type() -> str:

        return 'body'

    @staticmethod
    def __get_tcx_type() -> str:

        return 'Step_t'

    def get_duration_type(self) -> str:

        """
        Either distance or time

        :return: 'distance' or 'time'
        :rtype: str
        """
        if self.distance is not None:
            return 'distance'
        else:
            return 'time'

    def __str__(self) -> str:

        output = FirstStepBase.__str__(self)
        output += 'type - {}  pace - {}\n'.format(self.__get_type(), str(self.pace))
        if self.get_duration_type() == 'distance':
            output += 'Distance - {}\n'.format(str(self.distance))
        else:
            output += 'Time - {}\n'.format(str(self.time))

        return output

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
        out_string = FirstStepBase.details(self, indent=indent)
        if self.get_duration_type() == 'distance':
            out_string += '{}  {}'.format(indent, str(self.distance))
        else:
            out_string += '{}  {}'.format(indent, str(self.time))

        out_string += '  at  {}\n'.format(str(self.pace))

        return out_string

    def tcx(self, indent: str ='', child: bool =False, delta_seconds: int =5) -> str:

        """
        Generate a tcx string to download to a Garmin device

        :param indent:
        :type indent: str
        :param child: is a child of a repeat step (can be recursive)
        :type child: bool
        :param delta_seconds: for speed tolerance
        :type delta_seconds: int
        :return: a tcx format for the training plan
        :rtype: str
        """
        tcx_string = FirstStepBase.tcx_start(self, child=child, step_type='Step_t', indent=indent)

        if self.get_duration_type() == 'distance':
            tcx_string += '{}  <Duration xsi:type="Distance_t">\n'.format(indent)
            tcx_string += '{}    <Meters>{:.0f}</Meters>\n'.format(indent, self.distance.convert_to('m'))
        else:  # time
            tcx_string += '{}  <Duration xsi:type="Time_t">\n'.format(indent)
            tcx_string += '{}    <Seconds>{}</Seconds>\n'.format(indent, str(int(self.time.convert_to('second'))))

        tcx_string += '{}  </Duration>\n'.format(indent)

        tcx_string += '{}  <Intensity>{}</Intensity>\n'.format(indent, self.intensity)

        tcx_string += '{}  <Target xsi:type="Speed_t">\n'.format(indent)
        tcx_string += '{}    <SpeedZone xsi:type="CustomSpeedZone_t">\n'.format(indent)
        tcx_string += '{}    <LowInMetersPerSecond>{:.7f}</LowInMetersPerSecond>\n'.format(
            indent, self.pace.meters_per_second_delta(delta_seconds))
        tcx_string += '{}    <HighInMetersPerSecond>{:.7f}</HighInMetersPerSecond>\n'.format(
            indent, self.pace.meters_per_second_delta(-delta_seconds))
        tcx_string += '{}  </SpeedZone>\n'.format(indent)
        tcx_string += '{}  </Target>\n'.format(indent)

        if child:
            tcx_string += indent + '</Child>\n'
        else:
            tcx_string += indent + '</Step>\n'

        return tcx_string

    def total(self, what: str ='distance', unit: str ='m') -> float:

        """
        Calculate the total distance or time for this step

        :param what: distance or time
        :type what: str
        :param unit:
        :type unit: str
        :return: total distance value
        :rtype: float
        """
        if what == 'distance':
            if self.get_duration_type() == what:
                return self.distance.convert_to(unit=unit)
            else:
                return self.pace.to_distance(time=self.time, unit=unit)
        elif what == 'time':
            if self.get_duration_type() == what:
                return self.time.convert_to(unit=unit)
            else:
                return self.pace.to_time(distance=self.distance, unit=unit)
        else:
            raise ValueError('what must be "distance" or "time"')

    @classmethod
    def from_instructions(cls, instructions: str, data: FirstData, time_index: int, rp: FirstPace):

        """
        Create a step from an instruction string

        :param instructions: instruction string
        :type instructions: str
        :param data: First database
        :type data: FirstData
        :param time_index: the index in the paces table
        :type time_index: int
        :param rp: race pace
        :type rp: FirstPace
        :return: the step
        :rtype: FirstStep
        """
        segment_name = instructions.split('@')[0]
        increment = None
        pace = None
        duration = None
        try:
            segment = data.segment_by_name(segment_name)
            distance = segment.distance
        except KeyError:
            distance = FirstDistance.from_string(segment_name)
            segment_name = instructions.split('@')[1]
            pace_list = segment_name.split('+')
            segment_name = pace_list[0]
            if len(pace_list) > 1:
                increment = int(pace_list[1])
            else:
                increment = None
            if segment_name == 'RP':  # special case for race-pace
                segment = None
                pace = copy.deepcopy(rp)
            else:
                segment = data.segment_by_name(segment_name)

        if segment is not None:
            if segment.ref_pace_name is not None:
                segment_name = segment.ref_pace_name
            segment_index = data.segment_index_by_name(segment_name) + 1  # +1 since the first column is the ref time
            pace = data.segments_paces[time_index][segment_index]
            duration = segment.duration

        if increment is not None:
            pace.increment(increment)
        return cls(name=instructions, pace=pace, time=duration, distance=distance)
