# input_num_string.py
#
# ICS 33 Spring 2024
# Project 3: Why Not Smile?
#
# Roshan Raj
# roshar1@uci.edu

import grin

class InputHandler:
    """
    Class to handle input operations in Grin.
    """
    @classmethod
    def innum_statement(cls, line):
        """
        Take numerical input and assign it to a variable.

        Args:
            line (list): List of tokens representing the INNUM statement.
        """
        variable_name = None

        for token in line:
            if token.kind() == grin.GrinTokenKind.IDENTIFIER:
                variable_name = token.text()

        if variable_name is not None:
            try:
                value = input().strip()
                if '.' in value:
                    converted_value = float(value)
                else:
                    converted_value = int(value)
                grin.Basic.variables[variable_name] = converted_value
            except ValueError:
                print(f"Error: Invalid number input for {variable_name}")
                exit(1)


    @classmethod
    def instr_statement(cls, line):
        """
        Take string input and assign it to a variable.

        Args:
            line (list): List of tokens representing the INSTR statement.
        """
        variable_name = None

        for token in line:
            if token.kind() == grin.GrinTokenKind.IDENTIFIER:
                variable_name = token.text()[1:-1]


        if variable_name is not None:
            value = input().strip()
            grin.Basic.variables[variable_name] = value



__all__ = ["InputHandler"]
