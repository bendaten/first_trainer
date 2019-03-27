from typing import List, Dict, Union

from first_data import FirstData
from first_distance import FirstDistance
from first_pace import FirstPace
from first_time import FirstTime
from first_utils import XmlTag


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

    def details(self, indent: str = '') -> str:

        return '{}Step: "{}"\n'.format(indent, self.name)

    def tcx_top(self, child: bool, step_type: str) -> XmlTag:

        level = 'Child' if child else 'Step'
        step = XmlTag(name=level, attributes={'xsi:type': step_type})
        step_id = XmlTag(name='StepId', single_line=True)
        step_id.add(item=str(self.step_id))
        step.add(item=step_id)

        name = XmlTag(name='Name', single_line=True)
        name.add(item=self.name)
        step.add(item=name)

        return step


class FirstStepRepeat(FirstStepBase):

    # noinspection PyTypeChecker
    def __init__(self, name: str, repeat: int = 1):

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

    def details(self, level: int = 0, indent: str = '') -> str:

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

    def to_json(self, output_unit: Union[str, None] = None) -> Dict:

        result_dict = {'name': self.name,
                       'repeat': self.repeat,
                       'steps': [step.to_json(output_unit=output_unit) for step in self.steps]}

        return result_dict

    def to_html(self) -> XmlTag:

        section = XmlTag(name='div', attributes={'style': 'margin-left: 20px'})
        par = XmlTag(name='p')
        section.add(par)
        par.add('Repeat {} times:'.format(self.repeat))
        for step in self.steps:
            section.add(step.to_html())

        return section

    def tcx(self, child: bool = False, delta_seconds: int = 5) -> XmlTag:

        step = self.tcx_top(child=child, step_type='Repeat_t')

        repetitions = XmlTag(name='Repetitions', single_line=True)
        repetitions.add(item=str(self.repeat))
        step.add(item=repetitions)

        for step_item in self.steps:
            step.add(item=step_item.tcx(child=True, delta_seconds=delta_seconds))

        return step

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

    def total(self, what: str = 'distance', unit: str = 'm') -> float:

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
    def __init__(self, name: str, pace: FirstPace, intensity: str = 'Active',
                 distance: FirstDistance = None, time: FirstTime = None):

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
        out_string = FirstStepBase.details(self, indent=indent)
        if self.get_duration_type() == 'distance':
            out_string += '{}  {}'.format(indent, str(self.distance))
        else:
            out_string += '{}  {}'.format(indent, str(self.time))

        out_string += '  at  {}\n'.format(str(self.pace))

        return out_string

    def to_json(self, output_unit: Union[str, None] = None) -> Dict:

        result_dict = {'name': self.name}
        if self.time:
            result_dict['time'] = self.time.to_json()
        if self.distance:
            result_dict['distance'] = self.distance.to_json(output_unit=output_unit)
        result_dict['pace'] = self.pace.to_json(output_unit=output_unit)

        return result_dict

    def to_html(self) -> XmlTag:

        section = XmlTag(name='div', attributes={'style': 'margin-left: 20px'})
        par = XmlTag(name='p')
        section.add(par)
        text = ''
        if self.time:
            text = str(self.time)
        if self.distance:
            text = str(self.distance)
        par.add('{} - {} at {}'.format(self.name, text, str(self.pace)))

        return section

    def tcx(self, child: bool = False, delta_seconds: int = 5) -> XmlTag:

        step = self.tcx_top(child=child, step_type='Step_t')

        if self.get_duration_type() == 'distance':
            dur_type = 'Distance_t'
            dur_quantity = 'Meters'
            dur_value = '{:.0f}'.format(self.distance.convert_to('m'))
        else:  # time
            dur_type = 'Time_t'
            dur_quantity = 'Seconds'
            dur_value = '{:.0f}'.format(self.time.convert_to('second'))

        duration = XmlTag(name='Duration', attributes={'xsi:type': dur_type})
        dur = XmlTag(name=dur_quantity, single_line=True)
        dur.add(item=dur_value)
        duration.add(item=dur)
        step.add(item=duration)

        intensity = XmlTag(name='Intensity', single_line=True)
        intensity.add(item=self.intensity)
        step.add(item=intensity)

        target = XmlTag(name='Target', attributes={'xsi:type': 'Speed_t'})
        step.add(item=target)
        zone = XmlTag(name='SpeedZone', attributes={'xsi:type': 'CustomSpeedZone_t'})
        target.add(item=zone)
        low = XmlTag(name='LowInMetersPerSecond', single_line=True)
        low.add(item='{:.7f}'.format(self.pace.meters_per_second_delta(delta_seconds)))
        zone.add(item=low)
        high = XmlTag(name='HighInMetersPerSecond', single_line=True)
        high.add(item='{:.7f}'.format(self.pace.meters_per_second_delta(-delta_seconds)))
        zone.add(item=high)

        return step

    def total(self, what: str = 'distance', unit: str = 'm') -> float:

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
                pace = FirstPace.copy(rp)
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
