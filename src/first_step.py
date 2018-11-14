import copy

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
    def reset_global_id():  # reset before each training plan

        """
        Reset the global id
        """
        FirstStepBase.__global_id = 0

    # noinspection PyTypeChecker
    def __init__(self, name):

        where_am_i = 'FirstStepBase.__init__'
        if not isinstance(name, basestring):
            raise TypeError(where_am_i + ' - name must be a string')

        self.step_id = FirstStepBase.__global_id
        FirstStepBase.__global_id += 1
        self.name = name

    def __str__(self):

        return 'Step: "' + self.name + '"  id = ' + str(self.step_id) + '\n'

    def details(self, indent=''):

        return indent + 'Step: "' + self.name + '"\n'

    def tcx_start(self, child, step_type, indent):

        if child:
            token = 'Child'
        else:
            token = 'Step'

        tcx_string = indent + '<' + token + ' xsi:type="' + step_type + '">\n'
        tcx_string += indent + '  <StepId>' + str(self.step_id) + '</StepId>\n'
        tcx_string += indent + '  <Name>' + self.name + '</Name>\n'

        return tcx_string


class FirstStepRepeat(FirstStepBase):

    # noinspection PyTypeChecker
    def __init__(self, name, repeat):

        """
        Constructor
        
        :param name: step name
        :type name: str
        :param repeat: number of repetitions of the child steps
        :type repeat: int
        :return: instance of FirstStepRepeat
        :rtype: FirstStepRepeat
        """
        where_am_i = 'FirstStepRepeat.__init__'
        if repeat is not None and not isinstance(repeat, int):
            raise TypeError(where_am_i + ' - repeat must be an integer')
        if repeat < 1:
            raise ValueError(where_am_i + ' - repeat must be greater than 0')

        FirstStepBase.__init__(self, name=name)

        self.repeat = repeat
        self.steps = []

    @staticmethod
    def __get_type():

        return 'repeat'

    def __str__(self):

        return FirstStepBase.__str__(self) + 'type - ' + self.__get_type() + '  repeat - ' + str(self.repeat) + '\n'

    def details(self, level=0, indent=''):

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

    def tcx(self, indent='', child=False, delta_seconds=5):

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

        tcx_string += indent + '  <Repetitions>' + str(self.repeat) + '</Repetitions>\n'

        for step in self.steps:
            tcx_string += step.tcx(indent=indent + '  ', child=True, delta_seconds=delta_seconds)

        if child:
            tcx_string += indent + '</Child>\n'
        else:
            tcx_string += indent + '</Step>\n'

        return tcx_string

    def add_step(self, step):

        """
        Add a child step
        
        :param step: the step to be added
        :type step: FirstStepBase
        """
        where_am_i = 'FirstStepRepeat.add_step'
        if not isinstance(step, FirstStepBase):
            raise TypeError(where_am_i + ' - step must be an instance of FirstStepBase')

        self.steps.append(step)
        
    def set_steps(self, steps):

        """
        Set the steps to be repeated

        :param steps: list of steps
        :type steps: list of FirstStepBase
        """
        self.steps = steps

    def total(self, what='distance', unit='m'):

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
    def __init__(self, name, pace, intensity='Active', distance=None, time=None):

        """
        Constructor
        
        :param name: step name
        :type name: str
        :param pace: running pace
        :type pace: FirstPace
        :param distance: the segment distance
        :type distance: FirstDistance
        :param time: the segment duration
        :type time: FirstTime
        :return: instance of FirstStepBocy
        :rtype: FirstStepBody
        """
        where_am_i = 'FirstStepBody.__init__'
        if not isinstance(pace, FirstPace):
            raise TypeError(where_am_i + ' - pace must be an instance of FirstPace')
        if distance is None and time is None:
            raise ValueError(where_am_i + ' - Either distance or time must have a value')
        if distance is not None and not isinstance(distance, FirstDistance):
            raise TypeError(where_am_i + ' - distance must be an instance of FirstDistance')
        if time is not None and not isinstance(time, FirstTime):
            raise TypeError(where_am_i + ' - time must be an instance of FirstTime')
        if distance is not None and time is not None:
            raise ValueError(where_am_i + ' - cannot set both distance and duration in the same step')

        FirstStepBase.__init__(self, name=name)

        self.pace = pace
        self.intensity = intensity
        self.distance = distance
        self.time = time

    @staticmethod
    def __get_type():

        return 'body'

    @staticmethod
    def __get_tcx_type():

        return 'Step_t'

    def get_duration_type(self):

        """
        Either distance or time

        :return: 'distance' or 'time'
        :rtype: str
        """
        if self.distance is not None:
            return 'distance'
        else:
            return 'time'

    def __str__(self):

        output = FirstStepBase.__str__(self)
        output += 'type - ' + self.__get_type() + '  pace - ' + str(self.pace) + '\n'
        if self.get_duration_type() == 'distance':
            output += 'Distance - ' + str(self.distance) + '\n'
        else:
            output += 'Time - ' + str(self.time) + '\n'

        return output

    def details(self, level=0, indent=''):

        """
        Text report of a training plan

        :param level: level of details; 0 for minimum
        :param indent:
        :return: plain text string
        :rtype: str
        """
        out_string = FirstStepBase.details(self, indent=indent)
        if self.get_duration_type() == 'distance':
            out_string += indent + '  ' + str(self.distance)
        else:
            out_string += indent + '  ' + str(self.time)

        out_string += '  at  ' + str(self.pace) + '\n'

        return out_string

    def tcx(self, indent='', child=False, delta_seconds=5):

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
            tcx_string += indent + '  <Duration xsi:type="Distance_t">\n'
            tcx_string += indent + '    <Meters>' + '{:.0f}'.format(self.distance.convert_to('m')) + '</Meters>\n'
        else:  # time
            tcx_string += indent + '  <Duration xsi:type="Time_t">\n'
            tcx_string += indent + '    <Seconds>' + str(int(self.time.convert_to('second'))) + '</Seconds>\n'

        tcx_string += indent + '  </Duration>\n'

        tcx_string += indent + '  <Intensity>' + self.intensity + '</Intensity>\n'

        tcx_string += indent + '  <Target xsi:type="Speed_t">\n'
        tcx_string += indent + '    <SpeedZone xsi:type="CustomSpeedZone_t">\n'
        tcx_string += indent + '    <LowInMetersPerSecond>' +                                      \
                               '{:.7f}'.format(self.pace.meters_per_second_delta(delta_seconds)) + \
                               '</LowInMetersPerSecond>\n'
        tcx_string += indent + '    <HighInMetersPerSecond>' +                                     \
                               '{:.7f}'.format(self.pace.meters_per_second_delta(-delta_seconds)) + \
                               '</HighInMetersPerSecond>\n'
        tcx_string += indent + '  </SpeedZone>\n'
        tcx_string += indent + '  </Target>\n'

        if child:
            tcx_string += indent + '</Child>\n'
        else:
            tcx_string += indent + '</Step>\n'

        return tcx_string

    def total(self, what='distance', unit='m'):

        """
        Calculate the total distance or time for this step

        :param what: distance or time
        :type what: str
        :param unit:
        :type unit: str
        :return: total distance value
        :rtype: float
        """
        where_am_i = 'FirstStepBody.total'
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
            raise ValueError(where_am_i + ' - what must be "distance" or "time"')

    @classmethod
    def from_instructions(cls, instructions, data, time_index, rp):

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
