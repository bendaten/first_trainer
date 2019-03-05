import unittest

from first_utils import XmlTag, HtmlTable, HtmlBold


class TestHtmlBuilder(unittest.TestCase):

    def test_hello(self):

        try:  # happy path
            d1 = XmlTag(name='html')
            b1 = XmlTag(name='body')
            p1 = XmlTag(name='p', single_line=True)
            p1.add(item='Hello HTML')
            b1.add(item=p1)
            d1.add(item=b1)

            expected = '<html>\n' + \
                       '  <body>\n' + \
                       '    <p>Hello HTML</p>\n' + \
                       '  </body>\n' + \
                       '</html>'
            self.assertEqual(expected, d1.indented_str())
        except ValueError as ex:
            self.fail(str(ex))

        try:  # bad item
            d1 = XmlTag(name='abc')
            d1.add(item=123)
            self.fail('Expected to raise exception')
        except ValueError as ex:
            self.assertEqual('Unexpected XML item type', str(ex))

        try:  # bad item level
            d1 = XmlTag(name='abc')
            d1.add(item='def')
            _ = d1.indented_str(level=-1)
            self.fail('Expected to raise exception')
        except ValueError as ex:
            self.assertEqual('level must be equal to or greater than 0', str(ex))

    def test_table(self):

        try:  # happy path
            d1 = XmlTag(name='html')

            h1 = XmlTag(name='head')
            d1.add(item=h1)
            s1 = XmlTag(name='style')
            h1.add(item=s1)
            s1.add(item='table { border-collapse: collapse }')
            s1.add(item='td, th { border: 1px solid black; text-align: left; padding: 4px }')

            b1 = XmlTag(name='body')
            d1.add(item=b1)
            message = XmlTag(name='h2', single_line=True)
            message.add(item='The following tables have an auto-increment field that is over 25% of its type capacity:')
            b1.add(item=message)
            t1 = HtmlTable()
            b1.add(item=t1)
            t1.add_header(column_names=['Table', 'Field', 'Type', 'of type cap'])
            t1.add_row(values=['abc', 'id', 'int', '26%'])
            t1.add_row(values=['efg', 'id', 'int', '36%'])

            expected = '<!DOCTYPE html>\n' + \
                       '<html>\n' + \
                       '  <head>\n' + \
                       '    <style>\n' + \
                       '      table { border-collapse: collapse }\n' + \
                       '      td, th { border: 1px solid black; text-align: left; padding: 4px }\n' + \
                       '    </style>\n' + \
                       '  </head>\n' + \
                       '  <body>\n' + \
                       '    <h2>' + \
                       'The following tables have an auto-increment field that is over 25% of its type capacity:' + \
                       '</h2>\n' + \
                       '    <table>\n' + \
                       '      <tbody>\n' + \
                       '        <tr>\n' + \
                       '          <th>Table</th>\n' + \
                       '          <th>Field</th>\n' + \
                       '          <th>Type</th>\n' + \
                       '          <th>of type cap</th>\n' + \
                       '        </tr>\n' + \
                       '        <tr>\n' + \
                       '          <td>abc</td>\n' + \
                       '          <td>id</td>\n' + \
                       '          <td>int</td>\n' + \
                       '          <td>26%</td>\n' + \
                       '        </tr>\n' + \
                       '        <tr>\n' + \
                       '          <td>efg</td>\n' + \
                       '          <td>id</td>\n' + \
                       '          <td>int</td>\n' + \
                       '          <td>36%</td>\n' + \
                       '        </tr>\n' + \
                       '      </tbody>\n' + \
                       '    </table>\n' + \
                       '  </body>\n' + \
                       '</html>'
            self.assertEqual(expected, d1.indented_str(doctype='html'))
        except ValueError as ex:
            self.fail(str(ex))

        try:  # headless table
            t1 = HtmlTable()
            t1.add_header(column_names=['a', 'b', 'c'], mute=True)
            t1.add_row(values=[HtmlBold('Item 1'), 'type 1', 'value 1'])
            t1.add_row(values=[HtmlBold('Item 2'), 'type 2', 'value 2'])
            t1.add_row(values=[HtmlBold('Item 3'), 'type 3', 'value 3'])
            expected = '<table>\n' + \
                       '  <tbody>\n' + \
                       '    <tr>\n' + \
                       '      <td><b>Item 1</b></td>\n' + \
                       '      <td>type 1</td>\n' + \
                       '      <td>value 1</td>\n' + \
                       '    </tr>\n' + \
                       '    <tr>\n' + \
                       '      <td><b>Item 2</b></td>\n' + \
                       '      <td>type 2</td>\n' + \
                       '      <td>value 2</td>\n' + \
                       '    </tr>\n' + \
                       '    <tr>\n' + \
                       '      <td><b>Item 3</b></td>\n' + \
                       '      <td>type 3</td>\n' + \
                       '      <td>value 3</td>\n' + \
                       '    </tr>\n' + \
                       '  </tbody>\n' + \
                       '</table>'
            self.assertEqual(expected, t1.indented_str())
        except ValueError as ex:
            self.fail(str(ex))

        try:  # row before header
            t1 = HtmlTable()
            t1.add_row(values=['a', 'b'])
            self.fail('Expected to raise exception')
        except ValueError as ex:
            self.assertEqual('Table header not yet defined', str(ex))

        try:  # more than one header
            t1 = HtmlTable()
            t1.add_header(column_names=['a', 'b'])
            t1.add_header(column_names=['c', 'd'])
            self.fail('Expected to raise exception')
        except ValueError as ex:
            self.assertEqual('Only one table header allowed', str(ex))

        try:  # mismatched row values
            t1 = HtmlTable()
            t1.add_header(column_names=['a', 'b'])
            t1.add_row(values=['1', '2', '3'])
            self.fail('Expected to raise exception')
        except ValueError as ex:
            self.assertEqual('Number of values must match number of columns', str(ex))

    def test_attributes(self):

        try:
            html = XmlTag(name='html')
            body = XmlTag(name='body')
            html.add(body)
            link = XmlTag(name='a', attributes={'href': 'https://www.w3schools.com'}, single_line=True)
            body.add(link)
            link.add('This is the link to W3Schools')
            body.add(XmlTag(name='br', single_line=True))
            img_attr = {'src': 'https://www.w3schools.com/html/w3schools.jpg',
                        'alt': 'W3Schools.com',
                        'width': '104',
                        'height': '142'}
            image = XmlTag(name='img', attributes=img_attr, single_line=True)
            body.add(image)

            expected = '<html>\n' + \
                       '  <body>\n' + \
                       '    <a href="https://www.w3schools.com">This is the link to W3Schools</a>\n' + \
                       '    <br>\n' + \
                       '    <img src="https://www.w3schools.com/html/w3schools.jpg" ' + \
                       'alt="W3Schools.com" width="104" height="142">\n' + \
                       '  </body>\n' + \
                       '</html>'
            self.assertEqual(expected, html.indented_str())
        except ValueError as ex:
            self.fail(str(ex))

    def test_bold(self):

        try:
            bf = HtmlBold('this should be bold faced')
            self.assertEqual('<b>this should be bold faced</b>', bf.indented_str())
        except ValueError as ex:
            self.fail(str(ex))

        try:
            par = XmlTag(name='p')
            par.add('Plain and ')
            par.add(HtmlBold('Bold'))
            par.add(' are here.')
            expected = '<p>\n  Plain and \n  <b>Bold</b>\n   are here.\n</p>'
            self.assertEqual(expected, par.indented_str())
        except ValueError as ex:
            self.fail(str(ex))

        try:
            par = XmlTag(name='p', single_line=True)
            par.add('Plain and ')
            par.add(HtmlBold('Bold'))
            par.add(' are here.')
            expected = '<p>Plain and <b>Bold</b> are here.</p>'
            self.assertEqual(expected, par.indented_str())
        except ValueError as ex:
            self.fail(str(ex))
