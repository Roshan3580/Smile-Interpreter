# math.py
#
# ICS 33 Spring 2024
# Project 3: Why Not Smile?
#
# Roshan Raj
# roshar1@uci.edu

import grin


class MathHandler:
    """
    Class to handle mathematical operations in Grin.
    """

    @classmethod
    def add_statement(cls, line):
        """
        Add values to a variable.

        Args:
            line (list): List of tokens representing the ADD statement.
        """
        var_name, operand = cls._extract_operands(line)
        if var_name is not None and operand is not None:
            cls._perform_operation(var_name, operand, 'ADD')
        else:
            print("Error: None values were provided")
            exit(1)

    @classmethod
    def sub_statement(cls, line):
        """
        Subtract values from a variable.

        Args:
            line (list): List of tokens representing the SUB statement.
        """
        var_name, operand = cls._extract_operands(line)
        if var_name is not None and operand is not None:
            cls._perform_operation(var_name, operand, 'SUB')
        else:
            print("Error: None values were provided")
            exit(1)

    @classmethod
    def mult_statement(cls, line):
        """
        Multiply values to a variable.

        Args:
            line (list): List of tokens representing the MULT statement.
        """
        var_name, operand = cls._extract_operands(line)
        if var_name is not None and operand is not None:
            cls._perform_operation(var_name, operand, 'MULT')
        else:
            print("Error: None values were provided")
            exit(1)

    @classmethod
    def div_statement(cls, line):
        """
        Divide values from a variable.

        Args:
            line (list): List of tokens representing the DIV statement.
        """
        var_name, operand = cls._extract_operands(line)
        if var_name is not None and operand is not None:
            cls._perform_operation(var_name, operand, 'DIV')
        else:
            print("Error: None values were provided")
            exit(1)

    @classmethod
    def _extract_operands(cls, line):
        """
        Extract variable name and operand from a line of tokens.

        Args:
            line (list): List of tokens representing a mathematical operation statement.

        Returns:
            tuple: A tuple containing variable name and operand.
        """
        var_name = None
        operand = None
        tokens = list(line)
        if len(tokens) < 3:
            print("Error: Incorrect Format")
            exit(1)


        if tokens[1].kind() == grin.GrinTokenKind.IDENTIFIER:
            var_name = tokens[1].text()
        if tokens[2].kind() in (
        grin.GrinTokenKind.LITERAL_INTEGER, grin.GrinTokenKind.LITERAL_FLOAT,
        grin.GrinTokenKind.LITERAL_STRING):
            operand = tokens[2].value()
        elif tokens[2].kind() == grin.GrinTokenKind.IDENTIFIER:
            operand = grin.Basic.variables.get(tokens[2].text(), None)

        return var_name, operand


    @classmethod
    def _perform_operation(cls, var_name, operand, operation):
        """
        Perform mathematical operation and update the variable value.

        Args:
            var_name (str): Name of the variable.
            operand: Operand value.
            operation (str): Type of mathematical operation.
        """
        result = None
        var_value = grin.Basic.variables.get(var_name, None)

        if var_value is None:
            print(f"Error: Variable {var_name} not found")
            exit(1)

        if operation == 'ADD':
            if isinstance(var_value, str) and isinstance(operand, str):
                result = var_value + operand
            elif isinstance(var_value, (int, float)) and isinstance(operand, (int, float)):
                result = var_value + operand


        elif operation == 'SUB':
            if isinstance(var_value, (int, float)) and isinstance(operand, (int, float)):
                result = var_value - operand


        elif operation == 'MULT':
            if isinstance(var_value, str) and isinstance(operand, int) and operand >= 0:
                result = var_value * operand
            elif isinstance(var_value, int) and isinstance(operand, str) and var_value >= 0:
                result = operand * var_value
            elif isinstance(var_value, (int, float)) and isinstance(operand, (int, float)):
                result = var_value * operand
            else:
                print("Error: Incorrect Multiplication")
                exit(1)

        elif operation == 'DIV':
            if isinstance(var_value, int) and isinstance(operand, int) and operand != 0:
                result = var_value // operand
            elif isinstance(var_value, (int, float)) and isinstance(operand, (int, float)) and operand != 0:
                result = var_value / operand
            else:
                print("Error: Incorrect Division")
                exit(1)

        grin.Basic.variables[var_name] = result



__all__ = ["MathHandler"]
