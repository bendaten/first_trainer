import datetime
from typing import Dict

from first_distance import FirstDistance
from first_pace import FirstPace
from first_time import FirstTime


class FirstRaceType(object):

    def __init__(self, name: str, distance: float, unit: str):

        """
        Constructor

        :param name: like Marathon
        :type name: str
        :param distance: distance value
        :type distance: float
        :param unit: length unit
        :type unit: str
        :return: instance of FirstRaceType
        :rtype: FirstRaceType
        """
        if not FirstDistance.is_valid_unit(unit=unit):
            raise ValueError('"{}" is not a valid length unit'.format(unit))
        self.name = name
        self.distance = FirstDistance(distance=distance, unit=unit)

    def __str__(self) -> str:

        return self.name + ' - ' + str(self.distance)

    def to_json(self) -> Dict:

        return {'name': self.name, 'distance': self.distance.to_json()}


class FirstRace(object):

    # noinspection PyTypeChecker
    def __init__(self, race_type: FirstRaceType, name: str, race_date: datetime.date, target_time: FirstTime = None):

        """
        Constructor

        :param race_type:
        :type race_type: FirstRaceType
        :param name: like San Francisco Marathon
        :type name: str
        :param race_date:
        :type race_date: datetime.date
        :param target_time:
        :type target_time: FirstTime
        :return: instance of FirstRace
        :rtype: FirstRace
        """

        self.race_type = race_type
        self.name = name
        self.race_date = race_date
        self.target_time = target_time
        self.status = 'scheduled'
        self.actual_time = None

    statuses = ['scheduled', 'done', 'skipped']

    # noinspection PyTypeChecker
    def set_status(self, status: str) -> None:

        """
        Set the race status

        :param status:
        :type status: str
        """

        if status in self.statuses:
            self.status = status
        else:
            raise ValueError('Status not in ' + str(self.statuses))

    def __str__(self) -> str:

        out_string = (self.name + ' of type ' + str(self.race_type) + '\n' +
                      'On ' + str(self.race_date) + '\n')
        if self.target_time is not None:
            out_string += 'Target time - ' + str(self.target_time) + '\n'
        out_string += 'Status - ' + self.status + '\n'
        if self.status == 'done' and self.actual_time is not None:
            out_string += 'Actual time - ' + str(self.actual_time) + '\n'

        return out_string

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
        out_string = indent + 'Race:\n'
        out_string += indent + '  ' + 'Name - "' + self.name + '" of type ' + str(self.race_type) + '\n'
        if level > 0:
            out_string += indent + '  On ' + str(self.race_date) + '\n'
            if self.target_time is not None:
                out_string += indent + '  Target time - ' + str(self.target_time) + '\n'
            out_string += indent + '  Status - ' + self.status + '\n'
            if self.status == 'done' and self.actual_time is not None:
                out_string += indent + '  Actual time - ' + str(self.actual_time) + '\n'

        return out_string

    def to_json(self) -> Dict:

        result_dict = {'Name': self.name}
        if self.actual_time:
            result_dict['actual_time'] = str(self.actual_time)
        result_dict['race_date'] = str(self.race_date)
        result_dict['race_type'] = self.race_type.to_json()
        result_dict['status'] = self.status
        result_dict['target_time'] = {'time': str(self.target_time), 'seconds': self.target_time.seconds}

        return result_dict

    def set_target_time(self, a_time: FirstTime = None) -> None:

        """
        Set the target time for the race

        :param a_time:
        :type a_time: FirstTime
        """

        self.target_time = a_time

    def set_actual_time(self, a_time: FirstTime = None) -> None:

        """
        Set the actual race time after finished (future use)
        :param a_time:
        :type a_time: FirstTime
        """
        self.actual_time = a_time

    def race_pace(self) -> FirstPace:

        """
        Get the target race pace
        :return:
        :rtype: FirstPace
        """
        return FirstPace.from_time_distance(time=self.target_time, distance=self.race_type.distance)
