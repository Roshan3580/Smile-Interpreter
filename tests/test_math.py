import unittest
from unittest.mock import patch
import grin


class TestMathHandler(unittest.TestCase):
    def setUp(self):
        grin.Basic.variables["X"] = 10

    def test_incorrect_format(self):
        line = [
            grin.GrinToken(kind = grin.GrinTokenKind.IDENTIFIER, text = "X", location = grin.GrinLocation(1, 1)),
            grin.GrinToken(kind = grin.GrinTokenKind.LITERAL_INTEGER, text = "5", value = 5,
                           location = grin.GrinLocation(1, 3))
        ]
        with self.assertRaises(SystemExit):
            grin.MathHandler.add_statement(line)


    def test_add_statement_integer(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.ADD, text="ADD", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 5)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="5", value = 5, location=grin.GrinLocation(1, 7))
        ]
        grin.MathHandler.add_statement(line)
        self.assertEqual(grin.Basic.variables["X"], 15)


    def test_add_statement_float(self):
        grin.Basic.variables['X'] = 5.0
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="ADD", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 5)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_FLOAT, text="10.0", value = 10.0, location=grin.GrinLocation(1, 7))
        ]
        grin.MathHandler.add_statement(line)
        self.assertEqual(grin.Basic.variables["X"], 15.0)


    def test_add_statement_string(self):
        grin.Basic.variables["X"] = "Hello "
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="ADD", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 5)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_STRING, text='"World!"', value="World!", location=grin.GrinLocation(1, 7))
        ]
        grin.MathHandler.add_statement(line)
        self.assertEqual(grin.Basic.variables["X"], "Hello World!")


    def test_sub_statement_integer(self):
        grin.Basic.variables['X'] = 20
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="SUB", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 5)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="10", value=10, location=grin.GrinLocation(1, 7))
        ]
        grin.MathHandler.sub_statement(line)
        self.assertEqual(grin.Basic.variables["X"], 10)

    def test_sub_statement_float(self):
        grin.Basic.variables['X'] = 20.5
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="SUB", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 5)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_FLOAT, text="10.5", value=10.5, location=grin.GrinLocation(1, 7))
        ]
        grin.MathHandler.sub_statement(line)
        self.assertEqual(grin.Basic.variables["X"], 10.0)


    def test_mult_statement_integer(self):
        grin.Basic.variables['X'] = 5
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="MULT", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 6)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="4", value=4, location=grin.GrinLocation(1, 8))
        ]
        grin.MathHandler.mult_statement(line)
        self.assertEqual(grin.Basic.variables["X"], 20)

    def test_mult_statement_float(self):
        grin.Basic.variables['X'] = 5.0
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="MULT", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 6)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_FLOAT, text="4.0", value=4.0, location=grin.GrinLocation(1, 8))
        ]
        grin.MathHandler.mult_statement(line)
        self.assertEqual(grin.Basic.variables["X"], 20.0)

    def test_mult_statement_string(self):
        grin.Basic.variables['X'] = "Boo"
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="MULT", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 6)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="3", value=3, location=grin.GrinLocation(1, 8))
        ]
        grin.MathHandler.mult_statement(line)
        self.assertEqual(grin.Basic.variables["X"], "BooBooBoo")

    def test_mult_statement_integer_string(self):
        grin.Basic.variables['X'] = 3
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="MULT", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 6)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_STRING, text='"Boo"',value="Boo", location=grin.GrinLocation(1, 8))
        ]
        grin.MathHandler.mult_statement(line)
        self.assertEqual(grin.Basic.variables["X"], "BooBooBoo")

    def test_extract_operands_no_identifier(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.ADD, text="ADD", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="10", value=10, location=grin.GrinLocation(1, 5)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_FLOAT, text="2.5", value=2.5, location=grin.GrinLocation(1, 10))
        ]
        var_name, operand = grin.MathHandler._extract_operands(line)
        self.assertIsNone(var_name)
        self.assertEqual(operand, 2.5)

    def test_extract_operands_no_valid_operand(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.ADD, text="ADD", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 5)),
            grin.GrinToken(kind=grin.GrinTokenKind.ADD, text="ADD", location=grin.GrinLocation(1, 10))
        ]
        var_name, operand = grin.MathHandler._extract_operands(line)
        self.assertEqual(var_name, "X")
        self.assertIsNone(operand)

    def test_extract_operands_incorrect_format(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.ADD, text="ADD", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="10", value=10, location=grin.GrinLocation(1, 5))
        ]
        with self.assertRaises(SystemExit) as cm:
            grin.MathHandler._extract_operands(line)
        self.assertEqual(cm.exception.code, 1)


    def test_div_statement_integer(self):
        grin.Basic.variables['X'] = 7
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="DIV", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 5)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="2", value=2, location=grin.GrinLocation(1, 7))
        ]
        grin.MathHandler.div_statement(line)
        self.assertEqual(grin.Basic.variables["X"], 3)

    def test_div_statement_float(self):
        grin.Basic.variables['X'] = 7.0
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="DIV", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 5)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_FLOAT, text="2.0", value=2.0, location=grin.GrinLocation(1, 7))
        ]
        grin.MathHandler.div_statement(line)
        self.assertEqual(grin.Basic.variables["X"], 3.5)

    def test_add_statement_variable(self):
        grin.Basic.variables['X'] = 5
        grin.Basic.variables['Y'] = 10
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="ADD", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 5)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="Y", location=grin.GrinLocation(1, 7))
        ]
        grin.MathHandler.add_statement(line)
        self.assertEqual(grin.Basic.variables["X"], 15)

    def test_sub_statement_variable(self):
        grin.Basic.variables['X'] = 20
        grin.Basic.variables['Y'] = 10
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="SUB", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 5)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="Y", location=grin.GrinLocation(1, 7))
        ]
        grin.MathHandler.sub_statement(line)
        self.assertEqual(grin.Basic.variables["X"], 10)

    def test_mult_statement_variable(self):
        grin.Basic.variables['X'] = 5
        grin.Basic.variables['Y'] = 4
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="MULT", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 6)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="Y", location=grin.GrinLocation(1, 8))
        ]
        grin.MathHandler.mult_statement(line)
        self.assertEqual(grin.Basic.variables["X"], 20)


    def test_div_statement_variable(self):
        grin.Basic.variables['X'] = 8
        grin.Basic.variables['Y'] = 2
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="DIV", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 5)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="Y", location=grin.GrinLocation(1, 7))
        ]
        grin.MathHandler.div_statement(line)
        self.assertEqual(grin.Basic.variables["X"], 4)

    def test_add_statement_var_name_none_operand_none(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.ADD, text="ADD", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text=None, location=grin.GrinLocation(1, 5)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text=None, location=grin.GrinLocation(1, 7))
        ]
        with self.assertRaises(SystemExit):
            grin.MathHandler.add_statement(line)

    def test_no_value_for_perform_operation(self):
        with self.assertRaises(SystemExit):
            grin.MathHandler._perform_operation("P", 5, "ADD")

    def test_sub_statement_var_name_none_operand_none(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.SUB, text="SUB", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text=None, location=grin.GrinLocation(1, 5)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text=None, location=grin.GrinLocation(1, 7))
        ]
        with self.assertRaises(SystemExit):
            grin.MathHandler.sub_statement(line)

    def test_mult_statement_var_name_none_operand_none(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.MULT, text="MULT", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text=None, location=grin.GrinLocation(1, 6)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text=None, location=grin.GrinLocation(1, 8))
        ]
        with self.assertRaises(SystemExit):
            grin.MathHandler.mult_statement(line)


    @patch('builtins.exit')
    @patch('builtins.print')
    def test_incorrect_multiplication(self, mock_print, mock_exit):
        grin.Basic.variables['X'] = "hello"
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="MULT", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 6)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_FLOAT, text="2.5", value=2.5, location=grin.GrinLocation(1, 8))
        ]
        grin.MathHandler.mult_statement(line)
        mock_print.assert_called_once_with("Error: Incorrect Multiplication")
        mock_exit.assert_called_once_with(1)


    @patch('builtins.exit')
    @patch('builtins.print')
    def test_incorrect_division(self, mock_print, mock_exit):
        grin.Basic.variables['X'] = "hello"
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="DIV", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 5)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_FLOAT, text="2.5", value=2.5, location=grin.GrinLocation(1, 7))
        ]
        grin.MathHandler.div_statement(line)
        mock_print.assert_called_once_with("Error: Incorrect Division")
        mock_exit.assert_called_once_with(1)


    def test_div_statement_var_name_none_operand_none(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.DIV, text="DIV", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text=None, location=grin.GrinLocation(1, 5)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text=None, location=grin.GrinLocation(1, 7))
        ]
        with self.assertRaises(SystemExit):
            grin.MathHandler.div_statement(line)

if __name__ == '__main__':
    unittest.main()
