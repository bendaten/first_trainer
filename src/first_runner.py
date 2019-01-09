# noinspection PyTypeChecker
from typing import Dict

from first_distance import FirstDistance
from first_utils import FirstUtils


class FirstRunner(object):

    # noinspection PyTypeChecker
    def __init__(self, name: str, age: int = None, gender: str = None, email: str = None, length_unit: str = 'mile'):

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
        if name is None:
            raise ValueError('name is required')
        if age is not None and age <= 0:
                raise ValueError('age must be positive')
        # for now no limit on gender but if the plan has gender related instructions then we might post a warning
        # when a gender is not recognized by the plan
        if not FirstDistance.is_valid_unit(unit=length_unit):
            raise ValueError('length unit not recognized')

        if FirstUtils.is_internet_on():
            from validate_email import validate_email

            if email is not None and not validate_email(email=email):
                raise ValueError('invalid email address')

        self.name = name
        self.age = age
        self.gender = gender
        self.email = email
        self.length_unit = length_unit

    def __str__(self) -> str:

        out_string = 'Name - ' + self.name + '\n'
        if self.age is not None:
            out_string += 'Age - ' + str(self.age) + '\n'
        if self.gender is not None:
            out_string += 'Gender - ' + self.gender + '\n'
        if self.email is not None:
            out_string += 'Email - ' + self.email + '\n'

        return out_string

    def details(self, level=0, indent='') -> str:

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

    def to_json(self) -> Dict:

        result_dict = {'name': self.name}
        if self.age:
            result_dict['age'] = self.age
        if self.gender:
            result_dict['gender'] = self.gender
        if self.email:
            result_dict['email'] = self.email
        if self.length_unit:
            result_dict['length_unit'] = self.length_unit

        return result_dict
