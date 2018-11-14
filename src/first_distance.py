class FirstDistance(object):

    @staticmethod
    def is_valid_unit(unit):

        """
        Check if a string is one of the known length units

        :param unit: a unit string to check
        :type unit: str
        :return: True if unit is one of the recognized length unit strings
        :rtype: bool
        """
        return unit in ['m', 'km', 'ft', 'mile']

    conversions = {'m': 1, 'km': 1000, 'mile': 1609.344, 'ft': 0.3048}

    def __init__(self, distance, unit):

        """
        Constructor

        :param distance: positive distance value
        :type distance: float
        :param unit: length unit
        :type unit: str
        :return: instance of FirstDistance
        :rtype: FirstDistance
        """
        where_am_i = 'FirstDistance.__init__'
        if distance < 0:
            raise ValueError(where_am_i + ' - %1s is not a positive number' % distance)
        self.distance = distance

        if not self.is_valid_unit(unit):
            raise ValueError(where_am_i + ' - "%1s" is not a valid unit' % unit)
        self.unit = unit

    @classmethod
    def from_string(cls, string):

        """
        Instantiate FirstDistance from a string input

        :param string: a distance with value and unit like '4.5 km'
        :type string: str
        :return: instance of FirstDistance created from the string
        :rtype: FirstDistance
        """
        where_am_i = 'FirstDistance.from_string'
        tokens = string.split()
        if len(tokens) != 2:
            raise ValueError(where_am_i + ' - from_string() ' +
                             'expects 2 tokens, number and unit, but got "%1s"' % string)

        try:
            value = float(tokens[0])
        except ValueError as ex:
            raise ValueError(where_am_i + ' - expects the first token to be a number but ' + str(ex))
        unit = tokens[1]

        return cls(distance=value, unit=unit)

    def __str__(self):

        return str(self.distance) + ' ' + self.unit

    def convert_to(self, unit):

        """
        Convert a distance value to another unit

        :param unit: to unit
        :type unit: str
        :return: the converted value
        :rtype: float
        """
        where_am_i = 'FirstDistance.convert_to'
        if not self.is_valid_unit(unit):
            raise ValueError(where_am_i + ' - %1s is not a valid unit' % unit)

        if self.unit == unit:
            return self.distance
        else:
            to_m = self.conversions[self.unit]
            from_m = self.conversions[unit]
            return self.distance * to_m / from_m
