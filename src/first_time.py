from datetime import timedelta
from dateutil.parser import parse


class FirstTime(timedelta):

    """FirstTime adds restrictions to timedelta. It allows only positive values and a has a conversion method"""

    def __init__(self, hours=0, minutes=0, seconds=0):

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
        where_am_i = 'FirstTime.__init__'
        if hours < 0 or minutes < 0 or seconds < 0:
            raise ValueError(where_am_i + ' - does not allow negative values')

        timedelta.__init__(self, hours=hours, minutes=minutes, seconds=seconds)

    conversions = {'second': 1, 'minute': 60, 'hour': 3600}

    @classmethod
    def from_string(cls, string):

        """
        Create FirstTime from a string
        
        :type string: str
        :param string: format - HH:MM:SS
        :return: instance of FirstTime
        :rtype: FirstTime
        """
        where_am_i = 'FirstTime.from_string'
        try:
            t_from_str = parse(string)
        except ValueError as ex:
            raise ValueError(where_am_i + ' - ' + str(ex) + ' - "' + string + '"')

        if t_from_str.hour == 0 and t_from_str.minute == 0 and t_from_str.second == 0:
            raise ValueError(where_am_i + ' - unknown string format for "%1s"' % string)

        return cls(hours=t_from_str.hour, minutes=t_from_str.minute, seconds=t_from_str.second)

    def convert_to(self, unit):

        """
        Convert a duration value to another unit

        :param unit: to unit
        :type unit: str
        :return: the converted value
        :rtype: float
        """
        where_am_i = 'FirstTime.convert_to'
        if unit not in self.conversions:
            raise ValueError(where_am_i + ' - %1s is not a valid unit' % unit)

        seconds = timedelta.total_seconds(self)
        # seconds = super(FirstTime, self).total_seconds()

        if unit == 'second':
            return seconds
        else:
            return seconds / self.conversions[unit]
