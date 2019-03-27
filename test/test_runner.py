import unittest

from first_runner import FirstRunner
from first_utils import FirstUtils


class TestFirstRunner(unittest.TestCase):

    def test_to_string(self):

        try:  # name only
            runner = FirstRunner(name='John Doe')
            self.assertEqual('Name - John Doe\n', str(runner))
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        try:  # everything
            runner = FirstRunner(name='David Ben Gurion', age=105, gender='male', email='dbg@pmo.gov.il')
            cmp_string = 'Name - David Ben Gurion\nAge - 105\nGender - male\nEmail - dbg@pmo.gov.il\n'
            self.assertEqual(cmp_string, str(runner))
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        try:  # negative age
            _ = FirstRunner(name='Forest Gump', age=-34)
            self.fail('Should not get here with negative age')
        except ValueError as ex:
            self.assertEqual('age must be positive', str(ex))

        if FirstUtils.is_internet_on():
            try:  # bad email
                _ = FirstRunner(name='Forest Gump', email='doesnt#have.symbol.at')
                self.fail('Should not get here with a bad email')
            except ValueError as ex:
                self.assertEqual('invalid email address', str(ex))

    def test_to_json(self):
        try:  # name only
            runner = FirstRunner(name='John Doe')
            self.assertEqual({'length_unit': 'mile', 'name': 'John Doe'}, runner.to_json())
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        try:  # everything
            runner = FirstRunner(name='David Ben Gurion', age=105, gender='male', email='dbg@pmo.gov.il')
            cmp_json = {'age': 105,
                        'email': 'dbg@pmo.gov.il',
                        'gender': 'male',
                        'length_unit': 'mile',
                        'name': 'David Ben Gurion'}
            self.assertEqual(cmp_json, runner.to_json())
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))


if __name__ == '__main__':
    unittest.main()
