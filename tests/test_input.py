import unittest
from unittest.mock import patch
import grin

class TestInputHandler(unittest.TestCase):

    def setUp(self):
        grin.Basic.variables = {}

    def test_innum_statement_non_identifier_token(self):
        line = [
            grin.GrinToken(kind = grin.GrinTokenKind.LET, text = "LET",
                           location = grin.GrinLocation(1, 1)),
            grin.GrinToken(kind = grin.GrinTokenKind.LITERAL_INTEGER, text = "42",
                           location = grin.GrinLocation(1, 5))
        ]
        with patch('builtins.input', return_value = '100'):
            grin.InputHandler.innum_statement(line)
        self.assertNotIn("42", grin.Basic.variables)

    def test_innum_statement_valid_integer(self):
        line = [grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 1))]
        with patch('builtins.input', return_value='42'):
            grin.InputHandler.innum_statement(line)
        self.assertEqual(grin.Basic.variables["X"], 42)

    def test_innum_statement_valid_float(self):
        line = [grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="Y", location=grin.GrinLocation(1, 1))]
        with patch('builtins.input', return_value='3.14'):
            grin.InputHandler.innum_statement(line)
        self.assertEqual(grin.Basic.variables["Y"], 3.14)

    def test_innum_statement_invalid_number(self):
        line = [grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="Z", location=grin.GrinLocation(1, 1))]
        with patch('builtins.input', return_value='not_a_number'), self.assertRaises(SystemExit):
            with patch('sys.stdout') as fake_out:
                grin.InputHandler.innum_statement(line)
            self.assertIn("Error: Invalid number input for Z", fake_out.getvalue())

    def test_instr_statement_valid_string(self):
        line = [grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text='"message"', location=grin.GrinLocation(1, 1))]
        with patch('builtins.input', return_value='Hello, World!'):
            grin.InputHandler.instr_statement(line)
        self.assertEqual(grin.Basic.variables["message"], "Hello, World!")

    def test_instr_statement_non_identifier_token(self):
        line = [
            grin.GrinToken(kind = grin.GrinTokenKind.LET, text = "LET",
                           location = grin.GrinLocation(1, 1)),
            grin.GrinToken(kind = grin.GrinTokenKind.LITERAL_STRING, text = '"message"',
                           location = grin.GrinLocation(1, 5))
        ]
        with patch('builtins.input', return_value = 'Hello, World!'):
            grin.InputHandler.instr_statement(line)
        self.assertNotIn("message", grin.Basic.variables)


if __name__ == '__main__':
    unittest.main()
