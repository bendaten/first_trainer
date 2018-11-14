# noinspection PyTypeChecker
from first_distance import FirstDistance
from first_utils import FirstUtils


class FirstRunner(object):

    # noinspection PyTypeChecker
    def __init__(self, name, age=None, gender=None, email=None, length_unit='mile'):

        """
        Constructor

        :param name:
        :type name: str
        :param age: years only
        :type age: int
        :param gender: for now anything
        :type gender: str
        :param email: Should be a valid email address
        :type email: str
        :param length_unit: preferred and valid length unit
        :type length_unit: str
        """
        where_am_i = 'FirstRunner.__init__'
        if not isinstance(name, basestring):
            raise TypeError(where_am_i + ' - name must be a string')
        if age is not None:
            if not isinstance(age, int):
                raise TypeError(where_am_i + ' - age must be an integer')
            if age <= 0:
                raise ValueError(where_am_i + ' - age must be positive')
        if gender is not None:
            if not isinstance(gender, basestring):
                raise TypeError(where_am_i + ' - gender must be a string')
            # for now no limit on gender but if the plan has gender related instructions then we might post a warning
            # when a gender is not recognized by the plan
        if not isinstance(length_unit, basestring):
            raise TypeError(where_am_i + ' - length_unit is expected to be a string')
        if not FirstDistance.is_valid_unit(length_unit):
            raise ValueError(where_am_i + ' - length unit not recognized')

        if FirstUtils.is_internet_on():
            from validate_email import validate_email

            if email is not None and not validate_email(email=email):
                raise ValueError(where_am_i + ' - invalid email address')

        self.name = name
        self.age = age
        self.gender = gender
        self.email = email
        self.length_unit = length_unit

    def __str__(self):

        out_string = 'Name - ' + self.name + '\n'
        if self.age is not None:
            out_string += 'Age - ' + str(self.age) + '\n'
        if self.gender is not None:
            out_string += 'Gender - ' + self.gender + '\n'
        if self.email is not None:
            out_string += 'Email - ' + self.email + '\n'

        return out_string

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
        out_string = indent + 'Runner:\n'
        out_string += indent + '  Name - "' + self.name + '"\n'
        if level > 0:
            if self.age is not None:
                out_string += indent + '  Age - ' + str(self.age) + '\n'
            if self.gender is not None:
                out_string += indent + '  Gender - ' + self.gender + '\n'
            if self.email is not None:
                out_string += indent + '  Email - ' + self.email + '\n'

        return out_string
