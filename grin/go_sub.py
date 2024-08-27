# go_sub.py
#
# ICS 33 Spring 2024
# Project 3: Why Not Smile?
#
# Roshan Raj
# roshar1@uci.edu

import grin


class GosubHandler:
    """
    Class to handle GOSUB and RETURN statements in Grin.
    """
    @classmethod
    def go_sub_type(cls, line, parsed_lines, current_index, call_stack):
        """
        Determine the type of GOSUB statement and handle accordingly.

        Args:
            line (list): List of tokens representing the GOSUB statement.
            parsed_lines (list): List of parsed lines.
            current_index (int): Index of the current line.
            call_stack (list): Stack to keep track of GOSUB calls.

        Returns:
            tuple: Index of the target line to jump to and updated call stack.
        """
        if len(line) == 2:
            return cls.gosub_statement(line, parsed_lines, current_index, call_stack)
        elif len(line) == 6:
            return cls.gosub_conditional_statement(line, parsed_lines, current_index, call_stack)
        else:
            print("Wrong Format")
            exit(1)

    @classmethod
    def gosub_statement(cls, line, parsed_lines, current_index, call_stack):
        """
        Handle basic GOSUB statements.

        Args:
            line (list): List of tokens representing the GOSUB statement.
            parsed_lines (list): List of parsed lines.
            current_index (int): Index of the current line.
            call_stack (list): Stack to keep track of GOSUB calls.

        Returns:
            tuple: Index of the target line to jump to and updated call stack.
        """
        target = None
        for token in line:
            if token.kind() in (
            grin.GrinTokenKind.LITERAL_INTEGER, grin.GrinTokenKind.LITERAL_STRING):
                target = token.text()
                break

        if target is None:
            print("Error: GOSUB target not specified")
            exit(1)

        if target.isdigit() or (target.startswith('-') and target[1:].isdigit()):
            if int(target) != 0:
                target_line = current_index + int(target)
                if 0 <= target_line < len(parsed_lines):
                    call_stack.append(current_index + 1)
                    return target_line, call_stack
                else:
                    print(f"Error: GOSUB target line {target_line} is out of range")
                    exit(1)
            else:
                print(f"Error: GOSUB 0 causes an infinite loop!")
                exit(1)

        elif target.startswith('"') and target.endswith('"'):
            target = target[1:-1]
            if target in grin.Basic.labels:
                target_line = grin.Basic.labels[target]
                if 0 <= target_line <= len(parsed_lines):
                    call_stack.append(current_index + 1)
                    return target_line - 1, call_stack
                else:
                    print(f"Error: GOSUB target line {target_line} is out of range")
                    exit(1)

        else:
            print(f"Error: Label '{target}' not found")
            exit(1)

    @classmethod
    def gosub_conditional_statement(cls, line, parsed_lines, current_index, call_stack):
        """
        Handle conditional GOSUB statements.

        Args:
            line (list): List of tokens representing the conditional GOSUB statement.
            parsed_lines (list): List of parsed lines.
            current_index (int): Index of the current line.
            call_stack (list): Stack to keep track of GOSUB calls.

        Returns:
            tuple: Index of the target line to jump to and updated call stack.
        """
        variable1 = None
        variable2 = None
        operator = None
        condition = False
        new_line = line[2:]
        for token in new_line:
            if token.kind() == grin.GrinTokenKind.IDENTIFIER:
                if variable1 is None:
                    variable1 = token.text()
                else:
                    variable2 = token.text()
            elif token.kind() in (grin.GrinTokenKind.GREATER_THAN, grin.GrinTokenKind.EQUAL, grin.GrinTokenKind.NOT_EQUAL,
                                  grin.GrinTokenKind.GREATER_THAN_OR_EQUAL, grin.GrinTokenKind.LESS_THAN, grin.GrinTokenKind.LESS_THAN_OR_EQUAL):
                operator = token.text()
            elif token.kind() in (grin.GrinTokenKind.LITERAL_INTEGER, grin.GrinTokenKind.LITERAL_FLOAT):
                if variable1 is None:
                    variable1 = float(token.text())
                else:
                    variable2 = float(token.text())

        if None in (variable1, variable2, operator):
            print("Error: GOSUB target not specified")
            exit(1)

        if isinstance(variable1, str):
            variable1 = grin.Basic.variables.get(variable1)
        if isinstance(variable2, str):
            variable2 = grin.Basic.variables.get(variable2)

        if variable1 is None or variable2 is None:
            print("Error: Variable not found in data")
            exit(1)

        if operator == '=':
            condition = variable1 == variable2
        elif operator == '<>':
            condition = variable1 != variable2
        elif operator == '<':
            condition = variable1 < variable2
        elif operator == '<=':
            condition = variable1 <= variable2
        elif operator == '>':
            condition = variable1 > variable2
        elif operator == '>=':
            condition = variable1 >= variable2


        if condition:
            return cls.gosub_statement(line[0:2], parsed_lines, current_index, call_stack)
        else:
            return current_index + 1


    @classmethod
    def return_statement(cls, call_stack):
        """
        Handle the RETURN statement by popping the call stack.

        Args:
            call_stack (list): Stack to keep track of GOSUB calls.

        Returns:
            int: Index of the line to return to.
        """
        if not call_stack:
            print("Error: RETURN statement without matching GOSUB")
            exit(1)

        return call_stack.pop()


__all__ = ["GosubHandler"]