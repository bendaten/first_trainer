import urllib.request
from typing import List, Dict

import numpy

INDENT = '  '


class FirstUtils(object):

    @staticmethod
    def is_internet_on() -> bool:

        """
        Check if connected to the internet to enable email validation

        :return:
        :rtype: bool
        """
        try:
            urllib.request.urlopen(url='http://216.58.192.142', timeout=1)
            return True
        except urllib.request.URLError as ex:
            print(str(ex))
            return False

    @staticmethod
    def assert_deep_almost_equal(test_case, expected, actual, *args, **kwargs):
        """
        Assert that two complex structures have almost equal contents.

        Compares lists, dicts and tuples recursively. Checks numeric values
        using test_case's :py:meth:`unittest.TestCase.assertAlmostEqual` and
        checks all other values with :py:meth:`unittest.TestCase.assertEqual`.
        Accepts additional positional and keyword arguments and pass those
        intact to assertAlmostEqual() (that's how you specify comparison
        precision).

        :param test_case: TestCase object on which we can call all of the basic
        'assert' methods.
        :type test_case: :py:class:`unittest.TestCase` object
        :param expected: expected complex object
        :param actual: actual complex object
        """
        if isinstance(expected, (int, float, complex)):
            test_case.assertAlmostEqual(expected, actual, *args, **kwargs)
        elif isinstance(expected, (list, tuple, numpy.ndarray)):
            test_case.assertEqual(len(expected), len(actual))
            for index in range(len(expected)):
                v1, v2 = expected[index], actual[index]
                FirstUtils.assert_deep_almost_equal(test_case, v1, v2, *args, **kwargs)
        elif isinstance(expected, dict):
            test_case.assertEqual(set(expected), set(actual))
            for key in expected:
                FirstUtils.assert_deep_almost_equal(test_case, expected[key], actual[key], *args, **kwargs)
        else:
            test_case.assertEqual(expected, actual)


class XmlItem(object):

    """
    A simple XML builder
    """

    def __init__(self, single_line: bool = False, mute: bool = False):

        """
        XmlItem builder

        :param single_line: keep the item in a single line like '<b>Boldface</b>'
        :type single_line: bool
        :param mute: don't print this item and its children
        :type mute: bool
        """

        self.single_line = single_line
        self.mute = mute
        self.items = []

    def add(self, item) -> None:

        """
        Add to the list of items

        :param item: the item to add for now handles only strings and XmlItems
        :type item: Any
        """

        if isinstance(item, XmlItem) or isinstance(item, str):
            self.items.append(item)
        else:
            raise ValueError('Unexpected XML item type')  # for now just XmlItem and string

    def indented_str(self, level: int = 0) -> str:

        """
        Create an XML string

        :param level: Control indentation. Each line is indented level * INDENT
        :type level: int
        :return: The XML string
        :rtype: str
        """

        if level < 0:
            raise ValueError('level must be equal to or greater than 0')

        if self.mute:
            return ''

        contents = ''
        separator = '' if self.single_line else '\n'
        indent = '' if self.single_line else level * INDENT
        for item in self.items:
            if isinstance(item, str):
                contents += '{}{}{}'.format(indent, item, separator)
            elif isinstance(item, XmlItem):
                item_separator = '' if item.mute else separator
                child_level = 0 if self.single_line else level  # all children of a single line tag don't need indent
                contents += '{}{}'.format(item.indented_str(level=child_level), item_separator)
            else:
                raise ValueError('Unexpected XML item type')  # for now just XmlItem and string

        return contents


class XmlTag(XmlItem):

    def __init__(self, name: str, attributes: Dict[str, str] = None, single_line: bool = False, mute: bool = False):

        """
        HXmlTag builder

        :param name: The XML tag name
        :type name: str
        :param attributes: XML tag attributes
        :type attributes: dict[str, str]
        :param single_line: keep the tag in a single line like '<b>Boldface</b>'
        :type single_line: bool
        :param mute: don't print this item and its children
        :type mute: bool
        """

        self.name = name
        self.attributes = attributes
        super().__init__(single_line=single_line, mute=mute)

    def indented_str(self, level: int = 0, doctype: str = None) -> str:

        """
        Create an XML string

        :param level: Control indentation. Each line is indented level * INDENT
        :type level: int
        :param doctype: Insert <!DOCTYPE html> or <?xml version...?> above the first tag
        :type doctype: str
        :return: The XML string
        :rtype: str
        """

        if level < 0:
            raise ValueError('level must be equal to or greater than 0')

        if self.mute:
            return ''

        separator = '' if self.single_line else '\n'
        indent = level * INDENT
        second_indent = '' if self.single_line else indent
        if doctype is not None:
            if doctype == 'html':
                first_line = '<!DOCTYPE html>\n'
            elif doctype == 'xml':
                first_line = '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n'
            else:
                raise ValueError('doctype must be "html" or "xml"')
        else:
            first_line = ''

        tag = self.name
        if self.attributes is not None:
            for option in self.attributes:
                tag += ' ' + option + '="' + self.attributes[option] + '"'
        if self.single_line and not self.items:
            closing_tag = ''
        else:
            closing_tag = '{}</{}>'.format(second_indent, self.name)
        return '{}{}<{}>{}{}{}'.format(first_line, indent, tag, separator,
                                       super().indented_str(level=level + 1), closing_tag)


# HTML Shortcuts:

class HtmlTable(XmlTag):

    """
    Shortcut for building simple tables
    Workflow:
    * Instantiate the table
    * add_header with a list of column names
    * add_row with value for each column
    * add_row ...
    """

    def __init__(self, attributes: Dict[str, str] = None, mute: bool = False):

        """
        HtmlTable builder
        :param attributes: HTML tag attributes
        :type attributes: dict[str, str]
        :param mute: don't print this item and its children
        :type mute: bool
        """

        super().__init__(name='table', attributes=attributes)
        self.add(XmlTag(name='tbody', mute=mute))

    def add_header(self, column_names: List[str], mute: bool = False) -> None:

        """
        Add table header with column names. Use it only once and before you add any row

        :param column_names:
        :type column_names: list[str]
        :param mute: don't print this item and its children
        :type mute: bool
        """

        tbody = self.items[0]
        if tbody.items:
            raise ValueError('Only one table header allowed')

        header = XmlTag(name='tr', mute=mute)
        tbody.add(item=header)
        for name in column_names:
            column = XmlTag(name='th', single_line=True)
            column.add(item=name)
            header.add(item=column)

    def add_row(self, values: List, mute: bool = False) -> None:

        """
        Add table row with values for all columns. Use it after creating the header.
        The number of values must match the number of columns

        :param values:
        :type values: list
        :param mute: don't print this item and its children
        :type mute: bool
        """

        tbody = self.items[0]
        if not tbody.items:
            raise ValueError('Table header not yet defined')
        header = tbody.items[0]
        if len(header.items) != len(values):
            raise ValueError('Number of values must match number of columns')

        row = XmlTag(name='tr', mute=mute)
        tbody.add(item=row)
        for value in values:
            column = XmlTag(name='td', single_line=True)
            column.add(item=value)
            row.add(item=column)


class HtmlBold(XmlTag):

    def __init__(self, text: str):
        """
        shortcut for boldface text

        :param text: the text
        :type text: str
        """
        super().__init__(name='b', single_line=True)
        self.add(text)
