import unittest
from unittest.mock import patch
from grin.token import GrinToken, GrinTokenKind, GrinLocation
import grin

class TestBasic(unittest.TestCase):

    def setUp(self):
        grin.Basic._variables = {}


    def test_let_statement_with_integer(self):
        tokens = [
            GrinToken(kind=GrinTokenKind.LET, text="LET", location=GrinLocation(1, 1)),
            GrinToken(kind=GrinTokenKind.IDENTIFIER, text="x", location=GrinLocation(1, 5)),
            GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="10", location=GrinLocation(1, 7))
        ]
        grin.let_statement(tokens)
        self.assertEqual(grin.Basic.variables['x'], 10)

    def test_let_statement_with_string(self):
        tokens = [
            GrinToken(kind=GrinTokenKind.LET, text="LET", location=GrinLocation(1, 1)),
            GrinToken(kind=GrinTokenKind.IDENTIFIER, text="y", location=GrinLocation(1, 5)),
            GrinToken(kind=GrinTokenKind.LITERAL_STRING, text="\"hello\"", location=GrinLocation(1, 7))
        ]
        grin.let_statement(tokens)
        self.assertEqual(grin.Basic.variables['y'], 'hello')

    def test_let_statement_with_float(self):
        tokens = [
            GrinToken(kind=GrinTokenKind.LET, text="LET", location=GrinLocation(1, 1)),
            GrinToken(kind=GrinTokenKind.IDENTIFIER, text="z", location=GrinLocation(1, 5)),
            GrinToken(kind=GrinTokenKind.LITERAL_FLOAT, text="3.14", location=GrinLocation(1, 7))
        ]
        grin.let_statement(tokens)
        self.assertEqual(grin.Basic.variables['z'], 3.14)

    def test_let_statement_with_float_value(self):
        tokens = [
            GrinToken(kind=GrinTokenKind.LET, text="LET", location=GrinLocation(1, 1)),
            GrinToken(kind=GrinTokenKind.IDENTIFIER, text="z", location=GrinLocation(1, 5)),
            GrinToken(kind=GrinTokenKind.LITERAL_FLOAT, text= "6.4", location=GrinLocation(1, 7))
        ]
        grin.let_statement(tokens)
        self.assertEqual(grin.Basic.variables['z'], 6.4)

    def test_let_statement_with_none_variable_value(self):
        tokens = [
            GrinToken(kind=GrinTokenKind.LET, text="LET", location=GrinLocation(1, 1)),
            GrinToken(kind=GrinTokenKind.IDENTIFIER, text="M", location=GrinLocation(1, 5)),
        ]
        grin.let_statement(tokens)
        self.assertNotIn('M', grin.Basic.variables)


    def test_let_statement_with_both_none(self):
        tokens = [
            GrinToken(kind=GrinTokenKind.LET, text="LET", location=GrinLocation(1, 1)),
        ]
        grin.let_statement(tokens)
        self.assertEqual(grin.Basic.variables, {})


    @patch('builtins.print')
    def test_print_statement_with_existing_variable(self, mock_print):
        tokens = [
            GrinToken(kind=GrinTokenKind.PRINT, text="PRINT", location=GrinLocation(1, 1)),
            GrinToken(kind=GrinTokenKind.IDENTIFIER, text="x", location=GrinLocation(1, 7))
        ]
        grin.Basic.variables['x'] = '10'
        grin.print_statement(tokens)
        mock_print.assert_called_once_with('10')

    @patch('builtins.print')
    def test_print_statement_with_string(self, mock_print):
        tokens = [
            GrinToken(kind=GrinTokenKind.PRINT, text="PRINT", location=GrinLocation(1, 1)),
            GrinToken(kind=GrinTokenKind.LITERAL_STRING, text='"Hello Boo!"', location=GrinLocation(1, 7))
        ]
        grin.print_statement(tokens)
        mock_print.assert_called_once_with("Hello Boo!")


    @patch('builtins.print')
    def test_print_statement_with_non_existing_variable(self, mock_print):
        tokens = [
            GrinToken(kind=GrinTokenKind.PRINT, text="PRINT", location=GrinLocation(1, 1)),
            GrinToken(kind=GrinTokenKind.IDENTIFIER, text="non_existing", location=GrinLocation(1, 7))
        ]
        grin.print_statement(tokens)
        mock_print.assert_called_once_with(0)

    @patch('builtins.exit')
    def test_end_statement(self, mock_exit):
        grin.end_statement()
        mock_exit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
