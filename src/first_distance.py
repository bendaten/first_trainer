from typing import Union


class FirstDistance(object):

    @staticmethod
    def is_valid_unit(unit: str) -> bool:

        """
        Check if a string is one of the known length units

        :param unit: a unit string to check
        :type unit: str
        :return: True if unit is one of the recognized length unit strings
        :rtype: bool
        """
        return unit in ['m', 'km', 'ft', 'mile']

    conversions = {'m': 1, 'km': 1000, 'mile': 1609.344, 'ft': 0.3048}

    def __init__(self, distance: float, unit: str):

        """
        Constructor

        :param distance: positive distance value
        :type distance: float
        :param unit: length unit
        :type unit: str
        :return: instance of FirstDistance
        :rtype: FirstDistance
        """
        if distance < 0:
            raise ValueError('{} is not a positive number'.format(distance))
        self.distance = distance

        if not self.is_valid_unit(unit=unit):
            raise ValueError('"{}" is not a valid unit'.format(unit))
        self.unit = unit

    @classmethod
    def from_string(cls, string: str):

        """
        Instantiate FirstDistance from a string input

        :param string: a distance with value and unit like '4.5 km'
        :type string: str
        :return: instance of FirstDistance created from the string
        :rtype: FirstDistance
        """
        tokens = string.split()
        if len(tokens) != 2:
            raise ValueError('2 tokens are expected, number and unit, but got "{}"'.format(string))

        try:
            value = float(tokens[0])
        except ValueError as ex:
            raise ValueError('first token is expected to be a number but {}'.format(str(ex)))
        unit = tokens[1]

        return cls(distance=value, unit=unit)

    def to_json(self, output_unit: Union[str, None] = None):

        if output_unit:
            dist = self.convert_to(output_unit)
            return {'distance': dist, 'unit': output_unit}
        else:
            return {'distance': self.distance, 'unit': self.unit}

    def __str__(self):

        return '{} {}'.format(str(self.distance), self.unit)

    def convert_to(self, unit: str) -> float:

        """
        Convert a distance value to another unit

        :param unit: to unit
        :type unit: str
        :return: the converted value
        :rtype: float
        """
        if not self.is_valid_unit(unit=unit):
            raise ValueError('{} is not a valid unit'.format(unit))

        if self.unit == unit:
            return self.distance
        else:
            to_m = self.conversions[self.unit]
            from_m = self.conversions[unit]
            return self.distance * to_m / from_m
