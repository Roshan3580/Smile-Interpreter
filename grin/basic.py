# basic.py
#
# ICS 33 Spring 2024
# Project 3: Why Not Smile?
#
# Roshan Raj
# roshar1@uci.edu

import grin


class Basic:
    """
    Class to interpret basic Grin statements.
    """
    variables = {}  # Store variables
    labels = {}     # Store labels
    gosub_return = {}  # Store return addresses for GOSUB


    @classmethod
    def let_statement(cls, line):
        """
        Allows LET to statements assign values to variables.

        Args:
            line (list): List of tokens representing the LET statement.
        """
        variable_name = None
        variable_value = None

        for token in line:
            if token.kind() == grin.GrinTokenKind.IDENTIFIER:
                variable_name = token.text()
            elif token.kind() == grin.GrinTokenKind.LITERAL_INTEGER:
                variable_value = int(token.text())
            elif token.kind() == grin.GrinTokenKind.LITERAL_FLOAT:
                variable_value = float(token.text())
            elif token.kind() == grin.GrinTokenKind.LITERAL_STRING:
                variable_value = token.text()[1:-1]


        if variable_name is not None:
            if variable_value is not None:
                cls.variables[variable_name] = variable_value



    @classmethod
    def print_statement(cls, line):
        """
        Allows PRINT statements to display values or strings.

        Args:
            line (list): List of tokens representing the PRINT statement.
        """

        for token in line:
            if token.kind() == grin.GrinTokenKind.IDENTIFIER:
                variable_or_literal = token.text()
                if variable_or_literal in cls.variables:
                    print(cls.variables[variable_or_literal])
                else:
                    print(0)

            elif token.kind() == grin.GrinTokenKind.LITERAL_STRING:
                literal_string = token.text()[1:-1]
                print(literal_string)


    @classmethod
    def end_statement(cls):
        """
        End program execution.
        """
        exit()


let_statement = Basic.let_statement
print_statement = Basic.print_statement
end_statement = Basic.end_statement

__all__ = ['Basic', 'let_statement', 'print_statement', 'end_statement']
