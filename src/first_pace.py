from typing import Dict

from first_distance import FirstDistance
from first_time import FirstTime


class FirstPace(object):

    def __init__(self, minutes: int = 0, seconds: int = 0, length_unit: str = 'mile'):

        """
        Constructor

        :param minutes:
        :type minutes: int
        :param seconds:
        :type seconds: int
        :param length_unit:
        :type length_unit: str
        :return: instance of FirstPace
        :rtype: FirstPace
        """
        if not FirstDistance.is_valid_unit(unit=length_unit):
            raise ValueError('"{}" is not a valid length unit'.format(length_unit))
        self.time = FirstTime(minutes=minutes, seconds=seconds)
        self.length_unit = length_unit

    def __str__(self):

        return str(self.time) + ' min per ' + self.length_unit

    def to_json(self) -> Dict:

        return {'pace': str(self), 'length_unit': self.length_unit, 'time': self.time.to_json()}

    @classmethod
    def from_string(cls, str_input: str):

        """
        Constructor: Instantiate FirstPace from a string input
        
        :param str_input: format - '0:MM:SS per unit'
        :type str_input: str
        :return: instance of FirstPace
        :rtype: FirstPace
        """
        tokens = str_input.split()

        p_time = FirstTime.from_string(string=tokens[0])  # pass the exception on
        length_unit = tokens[-1]

        if not FirstDistance.is_valid_unit(unit=tokens[-1]):
            raise ValueError('"{}" is not a valid length unit'.format(length_unit))

        return cls(minutes=p_time.seconds//60, seconds=p_time.seconds % 60, length_unit=length_unit)

    @classmethod
    def copy(cls, from_pace: 'FirstPace'):

        return cls.from_string(str(from_pace))

    def to_time(self, distance: FirstDistance, unit: str) -> float:

        """
        How much time will take to run a given distance with this pace

        :param distance: the distance
        :type distance: FirstDistance
        :param unit: the desired unit of the result
        :type unit: str
        :return: the time value for this unit
        :rtype: float
        """
        factor = distance.convert_to(unit=self.length_unit)
        seconds = self.time.total_seconds() * factor
        result_time = FirstTime(seconds=round(seconds))
        return result_time.convert_to(unit=unit)

    def to_distance(self, time: FirstTime, unit: str) -> float:

        """
        How far you run given duration with this pace
        
        :param time: the duration
        :type time: FirstTime
        :param unit: the desired unit of the result
        :type unit: str
        :return: the distance value for this unit
        :rtype: float
        """
        factor = time.total_seconds()/self.time.total_seconds()
        result_distance = FirstDistance(distance=factor, unit=self.length_unit)
        return result_distance.convert_to(unit=unit)

    @classmethod
    def from_time_distance(cls, time: FirstTime, distance: FirstDistance, unit: str = None):

        """
        Constructor: Initiate FirstPace from time/distance

        :param time:
        :type time: FirstTime
        :param distance:
        :type distance: FirstDistance
        :param unit: length unit
        :type unit: str
        :return: instance to FirstPace
        :rtype: FirstPace
        """
        if unit is None:
            unit = distance.unit
        factor = distance.convert_to(unit=unit)  # 400m with unit = mile will become ~0.25
        seconds = time.total_seconds() / factor  # 2 minutes for 400m will give ~(2*60)/0.25

        return cls(minutes=int(seconds//60), seconds=round(seconds % 60), length_unit=unit)

    def increment(self, seconds: int) -> None:

        """
        Increment the pace by number of seconds - for instructions like 'RP+15'

        :param seconds:
        :type seconds: int
        """
        self.time = FirstTime(seconds=self.time.seconds + seconds)

    def meters_per_second_delta(self, delta_in_seconds: int) -> float:

        """
        Convert to speed in m/s for tcx with delta for tolerance

        :param delta_in_seconds:
        :type delta_in_seconds: int
        :return: calculated speed in m/s
        :rtype: float
        """
        seconds = self.time.total_seconds() + delta_in_seconds
        meters = FirstDistance(distance=1.0, unit=self.length_unit).convert_to(unit='m')

        return meters / seconds
