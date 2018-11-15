import urllib.request
from typing import List, Dict

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


class HtmlItem(object):

    """
    A simple HTML builder
    """

    def __init__(self, single_line: bool = False):

        """
        HtmlItem builder

        :param single_line: keep the item in a single line like '<b>Boldface</b>'
        :type single_line: bool
        """

        self.single_line = single_line
        self.items = []

    def add(self, item) -> None:

        """
        Add to the list of items

        :param item: the item to add for now handles only strings and HtmlItems
        :type item: Any
        """

        if isinstance(item, HtmlItem) or isinstance(item, str):
            self.items.append(item)
        else:
            raise ValueError('Unexpected HTML item type')  # for now just HtmlItem and string

    def indented_str(self, level: int = 0) -> str:

        """
        Create an HTML string

        :param level: Control indentation. Each line is indented level * INDENT
        :type level: int
        :return: The HTML string
        :rtype: str
        """

        if level < 0:
            raise ValueError('level must be equal to or greater than 0')

        contents = ''
        separator = '' if self.single_line else '\n'
        indent = '' if self.single_line else level * INDENT
        for item in self.items:
            if isinstance(item, str):
                contents += '{}{}{}'.format(indent, item, separator)
            elif isinstance(item, HtmlItem):
                contents += '{}{}'.format(item.indented_str(level=level), separator)
            else:
                raise ValueError('Unexpected HTML item type')  # for now just HtmlItem and string

        return contents


class HtmlTag(HtmlItem):

    def __init__(self, name: str, attributes: Dict[str, str] = None, single_line: bool = False):

        """
        HtmlTag builder

        :param name: The HTML tag name
        :type name: str
        :param attributes: HTML tag attributes
        :type attributes: dict[str, str]
        :param single_line: keep the tag in a single line like '<b>Boldface</b>'
        :type single_line: bool
        """

        self.name = name
        self.attributes = attributes
        super().__init__(single_line=single_line)

    def indented_str(self, level: int = 0, doctype: bool = False) -> str:

        """
        Create an HTML string

        :param level: Control indentation. Each line is indented level * INDENT
        :type level: int
        :param doctype: Insert <!DOCTYPE html> above the first tag
        :type doctype: bool
        :return: The HTML string
        :rtype: str
        """

        if level < 0:
            raise ValueError('level must be equal to or greater than 0')

        separator = '' if self.single_line else '\n'
        indent = level * INDENT
        second_indent = '' if self.single_line else indent
        first_line = '<!DOCTYPE html>\n' if doctype else ''
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


class HtmlTable(HtmlTag):

    """
    Shortcut for building simple tables
    Workflow:
    * Instantiate the table
    * add_header with a list of column names
    * add_row with value for each column
    * add_row ...
    """

    def __init__(self, attributes: Dict[str, str] = None):

        """
        HtmlTable builder
        :param attributes: HTML tag attributes
        :type attributes: dict[str, str]
        """

        super().__init__(name='table', attributes=attributes)
        self.add(HtmlTag(name='tbody'))

    def add_header(self, column_names: List[str]) -> None:

        """
        Add table header with column names. Use it only once and before you add any row

        :param column_names:
        :type column_names: list[str]
        """

        tbody = self.items[0]
        if tbody.items:
            raise ValueError('Only one table header allowed')

        header = HtmlTag(name='tr')
        tbody.add(item=header)
        for name in column_names:
            column = HtmlTag(name='th', single_line=True)
            column.add(item=name)
            header.add(item=column)

    def add_row(self, values: List[str]) -> None:

        """
        Add table row with values for all columns. Use it after creating the header.
        The number of values must match the number of columns

        :param values:
        :type values: list[str]
        """

        tbody = self.items[0]
        if not tbody.items:
            raise ValueError('Table header not yet defined')
        header = tbody.items[0]
        if len(header.items) != len(values):
            raise ValueError('Number of values must match number of columns')

        row = HtmlTag(name='tr')
        tbody.add(item=row)
        for value in values:
            column = HtmlTag(name='td', single_line=True)
            column.add(item=value)
            row.add(item=column)
