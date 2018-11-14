import unittest

from first_runner import FirstRunner
from first_utils import FirstUtils


class TestFirstRunner(unittest.TestCase):

    def test_to_string(self):

        try:  # name only
            r1 = FirstRunner(name='Yoseph Abulafia')
            self.assertEqual('Name - Yoseph Abulafia\n', str(r1))
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        try:  # everything
            r2 = FirstRunner(name='David Ben Gurion', age=105, gender='male', email='dbg@pmo.gov.il')
            cmp_string = 'Name - David Ben Gurion\nAge - 105\nGender - male\nEmail - dbg@pmo.gov.il\n'
            self.assertEqual(cmp_string, str(r2))
        except TypeError as tex:
            self.fail(str(tex))
        except ValueError as vex:
            self.fail(str(vex))

        try:  # no name
            r3 = FirstRunner(name=None, age=34, gender='female')
            self.fail('Should not get here with no name')
        except TypeError as ex:
            self.assertEqual('FirstRunner.__init__ - name must be a string', str(ex))

        try:  # bad type for age
            r3 = FirstRunner(name='Forest Gump', age='thirty four')
            self.fail('Should not get here with string for age')
        except TypeError as ex:
            self.assertEqual('FirstRunner.__init__ - age must be an integer', str(ex))

        try:  # negative age
            r3 = FirstRunner(name='Forest Gump', age=-34)
            self.fail('Should not get here with negative age')
        except ValueError as ex:
            self.assertEqual('FirstRunner.__init__ - age must be positive', str(ex))

        try:  # bad type for gender
            r3 = FirstRunner(name='Forest Gump', gender=0)
            self.fail('Should not get here with number for gender')
        except TypeError as ex:
            self.assertEqual('FirstRunner.__init__ - gender must be a string', str(ex))

        # TODO don't run this when not connected to the network
        if FirstUtils.is_internet_on():
            try:  # bad email
                r3 = FirstRunner(name='Forest Gump', email='doesnt#have.symbol.at')
                self.fail('Should not get here with a bad email')
            except ValueError as ex:
                self.assertEqual('FirstRunner.__init__ - invalid email address', str(ex))


if __name__ == '__main__':
    unittest.main()
