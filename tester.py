import unittest
import json
import parser

class TestParser(unittest.TestCase):

    def test_parse_value(self):
        self.assertEqual(parser.parse_value('123'), 123)
        self.assertEqual(parser.parse_value('(1,2,3)'), [1, 2, 3])  # Удаление пробелов
        self.assertEqual(parser.parse_value('$[a: 1, b: (2, 3)]'), {'a': 1, 'b': [2, 3]})

    def test_parse_constant(self):
        self.assertEqual(parser.parse_constant('@{1 + 2}'), 3)
        self.assertEqual(parser.parse_constant('@{max((1, 2, 3))}'), 3)
        self.assertEqual(parser.parse_constant('@{sort((3, 1, 2))}'), [1, 2, 3])

    def test_parse_file(self):
        parser.parse_file('input_files/config1.txt', 'output_files/output1.json')
        with open('output_files/output1.json', 'r') as file:
            data = json.load(file)
            self.assertEqual(data['var1'], 123)
            self.assertEqual(data['var2'], 'hello')  # Удаление кавычек
            self.assertEqual(data['var3'], [1, 2, 3])
            
if __name__ == '__main__':
    unittest.main()