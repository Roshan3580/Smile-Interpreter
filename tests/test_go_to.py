import unittest
import grin


class TestGotoHandler(unittest.TestCase):
    def setUp(self):
        grin.Basic.variables = {"X": 10, "Y": 20}
        grin.Basic.labels = {"start": 1, "end": 10}

    def test_goto_statement_with_missing_target(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.GOTO, text="GOTO", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_FLOAT, text="2.4", location=grin.GrinLocation(1, 5))
        ]
        parsed_lines = [""] * 10
        current_index = 3
        with self.assertRaises(SystemExit) as cm:
            grin.GotoHandler.goto_statement(line, parsed_lines, current_index)
        self.assertEqual(cm.exception.code, 1)

    def test_goto_conditional_statement_not_equal(self):
        line = [
            grin.GrinToken(kind = grin.GrinTokenKind.GOTO, text = "GOTO",
                           location = grin.GrinLocation(1, 1)),
            grin.GrinToken(kind = grin.GrinTokenKind.LITERAL_INTEGER, text = "2",
                           location = grin.GrinLocation(1, 5)),
            grin.GrinToken(kind = grin.GrinTokenKind.IDENTIFIER, text = "X",
                           location = grin.GrinLocation(1, 10)),
            grin.GrinToken(kind = grin.GrinTokenKind.NOT_EQUAL, text = "<>",
                           location = grin.GrinLocation(1, 15)),
            grin.GrinToken(kind = grin.GrinTokenKind.IDENTIFIER, text = "Y",
                           location = grin.GrinLocation(1, 20))
        ]
        parsed_lines = [""] * 10
        current_index = 3
        grin.Basic.variables = {"X": 10, "Y": 10}
        target_line = grin.GotoHandler.goto_conditional_statement(line, parsed_lines, current_index)
        self.assertEqual(target_line, 4)

    def test_goto_conditional_statement_less_than_or_equal(self):
        line = [
            grin.GrinToken(kind = grin.GrinTokenKind.GOTO, text = "GOTO",
                           location = grin.GrinLocation(1, 1)),
            grin.GrinToken(kind = grin.GrinTokenKind.LITERAL_INTEGER, text = "2",
                           location = grin.GrinLocation(1, 5)),
            grin.GrinToken(kind = grin.GrinTokenKind.IDENTIFIER, text = "X",
                           location = grin.GrinLocation(1, 10)),
            grin.GrinToken(kind = grin.GrinTokenKind.LESS_THAN_OR_EQUAL, text = "<=",
                           location = grin.GrinLocation(1, 15)),
            grin.GrinToken(kind = grin.GrinTokenKind.IDENTIFIER, text = "Y",
                           location = grin.GrinLocation(1, 20))
        ]
        parsed_lines = [""] * 10
        current_index = 3
        grin.Basic.variables = {"X": 5, "Y": 10}
        target_line = grin.GotoHandler.goto_conditional_statement(line, parsed_lines, current_index)
        self.assertEqual(target_line, 5)

    def test_goto_conditional_statement_greater_than_or_equal(self):
        line = [
            grin.GrinToken(kind = grin.GrinTokenKind.GOTO, text = "GOTO",
                           location = grin.GrinLocation(1, 1)),
            grin.GrinToken(kind = grin.GrinTokenKind.LITERAL_INTEGER, text = "2",
                           location = grin.GrinLocation(1, 5)),
            grin.GrinToken(kind = grin.GrinTokenKind.IDENTIFIER, text = "X",
                           location = grin.GrinLocation(1, 10)),
            grin.GrinToken(kind = grin.GrinTokenKind.GREATER_THAN_OR_EQUAL, text = ">=",
                           location = grin.GrinLocation(1, 15)),
            grin.GrinToken(kind = grin.GrinTokenKind.IDENTIFIER, text = "Y",
                           location = grin.GrinLocation(1, 20))
        ]
        parsed_lines = [""] * 10
        current_index = 3
        grin.Basic.variables = {"X": 15, "Y": 10}
        target_line = grin.GotoHandler.goto_conditional_statement(line, parsed_lines, current_index)
        self.assertEqual(target_line, 5)

    def test_goto_conditional_statement_invalid_operator(self):
        line = [
            grin.GrinToken(kind = grin.GrinTokenKind.GOTO, text = "GOTO",
                           location = grin.GrinLocation(1, 1)),
            grin.GrinToken(kind = grin.GrinTokenKind.LITERAL_INTEGER, text = "2",
                           location = grin.GrinLocation(1, 5)),
            grin.GrinToken(kind = grin.GrinTokenKind.IDENTIFIER, text = "X",
                           location = grin.GrinLocation(1, 10)),
            grin.GrinToken(kind = grin.GrinTokenKind.LITERAL_STRING, text = "invalid",
                           location = grin.GrinLocation(1, 15)),
            grin.GrinToken(kind = grin.GrinTokenKind.IDENTIFIER, text = "Y",
                           location = grin.GrinLocation(1, 20))
        ]
        parsed_lines = [""] * 10
        current_index = 3
        with self.assertRaises(SystemExit) as cm:
            grin.GotoHandler.goto_conditional_statement(line, parsed_lines, current_index)
        self.assertEqual(cm.exception.code, 1)

    def test_goto_statement_out_of_range_target_line(self):
        line = [
            grin.GrinToken(kind = grin.GrinTokenKind.GOTO, text = "GOTO",
                           location = grin.GrinLocation(1, 1)),
            grin.GrinToken(kind = grin.GrinTokenKind.LITERAL_INTEGER, text = "20",
                           location = grin.GrinLocation(1, 6))
        ]
        parsed_lines = [""] * 10
        current_index = 3

        with self.assertRaises(SystemExit) as cm:
            grin.GotoHandler.goto_statement(line, parsed_lines, current_index)
        self.assertEqual(cm.exception.code, 1)


    def test_goto_statement_with_out_of_range_target_label(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.GOTO, text="GOTO", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_STRING, text='"CCP"', location=grin.GrinLocation(1, 6))
        ]
        parsed_lines = [""] * 3
        current_index = 2
        grin.Basic.labels["CCP"] = 25
        with self.assertRaises(SystemExit) as cm:
            grin.GotoHandler.goto_statement(line, parsed_lines, current_index)
        self.assertEqual(cm.exception.code, 1)


    def test_goto_statement_with_integer_target(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.GOTO, text="GOTO", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="2", location=grin.GrinLocation(1, 5))
        ]
        parsed_lines = [""] * 10
        current_index = 3
        target_line = grin.GotoHandler.goto_statement(line, parsed_lines, current_index)
        self.assertEqual(target_line, 5)

    def test_goto_statement_with_label_target(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.GOTO, text="GOTO", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_STRING, text='"start"', location=grin.GrinLocation(1, 5))
        ]
        parsed_lines = [""] * 10
        current_index = 3
        target_line = grin.GotoHandler.goto_statement(line, parsed_lines, current_index)
        self.assertEqual(target_line, 0)

    def test_goto_statement_with_nonexistent_label(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.GOTO, text="GOTO", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_STRING, text="missing", location=grin.GrinLocation(1, 5))
        ]
        parsed_lines = [""] * 10
        current_index = 3
        with self.assertRaises(SystemExit) as cm:
            grin.GotoHandler.goto_statement(line, parsed_lines, current_index)
        self.assertEqual(cm.exception.code, 1)

    def test_goto_statement_with_out_of_range_integer_target(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.GOTO, text="GOTO", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="20", location=grin.GrinLocation(1, 5))
        ]
        parsed_lines = [""] * 10
        current_index = 3
        with self.assertRaises(SystemExit) as cm:
            grin.GotoHandler.goto_statement(line, parsed_lines, current_index)
        self.assertEqual(cm.exception.code, 1)

    def test_goto_conditional_statement_true(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.GOTO, text="GOTO", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="2", location=grin.GrinLocation(1, 5)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 10)),
            grin.GrinToken(kind=grin.GrinTokenKind.GREATER_THAN, text=">", location=grin.GrinLocation(1, 15)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="Y", location=grin.GrinLocation(1, 20))
        ]
        parsed_lines = [""] * 10
        current_index = 3
        target_line = grin.GotoHandler.goto_conditional_statement(line, parsed_lines, current_index)
        self.assertEqual(target_line, 4)

    def test_goto_conditional_statement_false(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.GOTO, text="GOTO", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="2", location=grin.GrinLocation(1, 5)),

            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 10)),
            grin.GrinToken(kind=grin.GrinTokenKind.LESS_THAN, text="<", location=grin.GrinLocation(1, 15)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="Y", location=grin.GrinLocation(1, 20))
        ]
        parsed_lines = [""] * 10
        current_index = 3
        target_line = grin.GotoHandler.goto_conditional_statement(line, parsed_lines, current_index)
        self.assertEqual(target_line, 5)

    def test_goto_conditional_statement_variable_not_found(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.GOTO, text="GOTO", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="2", location=grin.GrinLocation(1, 5)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="Z", location=grin.GrinLocation(1, 10)),
            grin.GrinToken(kind=grin.GrinTokenKind.EQUAL, text="=", location=grin.GrinLocation(1, 15)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="10", location=grin.GrinLocation(1, 20))
        ]
        parsed_lines = [""] * 10
        current_index = 3
        with self.assertRaises(SystemExit) as cm:
            grin.GotoHandler.goto_conditional_statement(line, parsed_lines, current_index)
        self.assertEqual(cm.exception.code, 1)


    def test_goto_conditional_statement_missing_elements(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.GOTO, text="GOTO", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="2", location=grin.GrinLocation(1, 5))
        ]
        parsed_lines = [""] * 10
        current_index = 3
        with self.assertRaises(SystemExit) as cm:
            grin.GotoHandler.goto_conditional_statement(line, parsed_lines, current_index)
        self.assertEqual(cm.exception.code, 1)

    def test_goto_statement_infinite_loop(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.GOTO, text="GOTO", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="0", value = 0, location=grin.GrinLocation(1, 6))
        ]
        parsed_lines = [""] * 10
        current_index = 3

        with self.assertRaises(SystemExit) as cm:
            grin.GotoHandler.goto_statement(line, parsed_lines, current_index)
        self.assertEqual(cm.exception.code, 1)


class TestGotoTypeHandler(unittest.TestCase):
    def setUp(self):
        grin.Basic.variables = {"X": 10, "Y": 20}
        grin.Basic.labels = {"start": 1, "end": 5}

    def test_goto_type_with_goto_statement(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.GOTO, text="GOTO", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="2", location=grin.GrinLocation(1, 5))
        ]
        parsed_lines = [""] * 10
        current_index = 3
        target_line = grin.GotoHandler.go_to_type(line, parsed_lines, current_index)
        self.assertEqual(target_line, 5)

    def test_goto_type_with_goto_conditional_statement(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.GOTO, text="GOTO", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="2", location=grin.GrinLocation(1, 5)),
            grin.GrinToken(kind=grin.GrinTokenKind.IDENTIFIER, text="X", location=grin.GrinLocation(1, 7)),
            grin.GrinToken(kind=grin.GrinTokenKind.EQUAL, text="=", location=grin.GrinLocation(1, 9)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="10", location=grin.GrinLocation(1, 11)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="2", location=grin.GrinLocation(1, 13))
        ]
        parsed_lines = [""] * 10
        current_index = 3
        target_line = grin.GotoHandler.go_to_type(line, parsed_lines, current_index)
        self.assertEqual(target_line, 4)

    def test_goto_type_with_wrong_format(self):
        line = [
            grin.GrinToken(kind=grin.GrinTokenKind.GOTO, text="GOTO", location=grin.GrinLocation(1, 1)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="2", location=grin.GrinLocation(1, 5)),
            grin.GrinToken(kind=grin.GrinTokenKind.LITERAL_INTEGER, text="3", location=grin.GrinLocation(1, 7))
        ]
        parsed_lines = [""] * 10
        current_index = 3
        with self.assertRaises(SystemExit) as cm:
            grin.GotoHandler.go_to_type(line, parsed_lines, current_index)
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
