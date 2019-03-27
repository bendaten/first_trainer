import datetime
from typing import Dict, Union

from first_distance import FirstDistance
from first_pace import FirstPace
from first_time import FirstTime
from first_utils import XmlTag, HtmlTable, HtmlBold


class FirstRaceType(object):

    def __init__(self, name: str, distance: FirstDistance):

        """
        Constructor

        :param name: like Marathon
        :type name: str
        :param distance: distance
        :type distance: FirstDistance
        :return: instance of FirstRaceType
        :rtype: FirstRaceType
        """
        self.name = name
        self.distance = distance

    def __str__(self) -> str:

        return self.name + ' - ' + str(self.distance)

    def to_json(self, output_unit: Union[str, None] = None) -> Dict:

        return {'name': self.name, 'distance': self.distance.to_json(output_unit=output_unit)}

    def distance_to_html(self, output_unit: Union[str, None] = None):

        return self.distance.to_html(output_unit)


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

    def to_json(self, output_unit: Union[str, None] = None) -> Dict:

        result_dict = {'Name': self.name}
        if self.actual_time:
            result_dict['actual_time'] = str(self.actual_time)
        result_dict['race_date'] = str(self.race_date)
        result_dict['race_type'] = self.race_type.to_json(output_unit=output_unit)
        result_dict['status'] = self.status
        if self.target_time:
            result_dict['target_time'] = {'time': str(self.target_time), 'seconds': self.target_time.seconds}

        return result_dict

    def to_html(self, output_unit: Union[str, None] = None) -> XmlTag:

        section = XmlTag(name='div')
        title = XmlTag(name='h2', single_line=True)
        title.add('Race:')
        section.add(title)

        table = HtmlTable(attributes={'style': 'border-spacing: 15px 0'})
        section.add(table)
        table.add_header(column_names=['key', 'value'], mute=True)
        table.add_row(values=['Name:', HtmlBold(self.name)])
        table.add_row(values=['Type:', HtmlBold(self.race_type.name)])
        table.add_row(values=['Distance:', HtmlBold(self.race_type.distance_to_html(output_unit))])
        table.add_row(values=['Date:', HtmlBold(str(self.race_date))])
        table.add_row(values=['Target time:', HtmlBold(str(self.target_time))])
        table.add_row(values=['Status:', HtmlBold(self.status)])

        return section

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
