from datetime import timedelta
from typing import Dict

from dateutil.parser import parse


class FirstTime(timedelta):

    """FirstTime adds restrictions to timedelta. It allows only positive values and a has a conversion method"""

    def __new__(cls, hours: int = 0, minutes: int = 0, seconds: int = 0):

        """
        Constructor

        :param hours:
        :type hours: int
        :param minutes:
        :type minutes: int
        :param seconds:
        :type seconds: int
        :return: instance of FirstTime
        :rtype: FirstTime
        """
        if hours < 0 or minutes < 0 or seconds < 0:
            raise ValueError('negative values are invalid')

        return super().__new__(cls, hours=hours, minutes=minutes, seconds=seconds)

    def to_json(self) -> Dict:

        return {'time': str(self), 'seconds': self.seconds}

    conversions = {'second': 1, 'minute': 60, 'hour': 3600}

    @classmethod
    def from_string(cls, string: str):

        """
        Create FirstTime from a string
        
        :type string: str
        :param string: format - HH:MM:SS
        :return: instance of FirstTime
        :rtype: FirstTime
        """
        t_from_str = parse(timestr=string)  # caller should catch the exception

        if t_from_str.hour == 0 and t_from_str.minute == 0 and t_from_str.second == 0:
            raise ValueError('unknown string format for "{}"'.format(string))

        return cls(hours=t_from_str.hour, minutes=t_from_str.minute, seconds=t_from_str.second)

    def convert_to(self, unit: str) -> float:

        """
        Convert a duration value to another unit

        :param unit: to unit
        :type unit: str
        :return: the converted value
        :rtype: float
        """
        if unit not in self.conversions:
            raise ValueError('{} is not a valid unit'.format(unit))

        seconds = timedelta.total_seconds(self)
        # seconds = super(FirstTime, self).total_seconds()

        if unit == 'second':
            return seconds
        else:
            return seconds / self.conversions[unit]
