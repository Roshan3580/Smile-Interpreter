# project3.py
#
# ICS 33 Spring 2024
# Project 3: Why Not Smile?
#
# The main module that executes your Grin interpreter.
#
# WHAT YOU NEED TO DO: You'll need to implement the outermost shell of your
# program here, but consider how you can keep this part as simple as possible,
# offloading as much of the complexity as you can into additional modules in
# the 'grin' package, isolated in a way that allows you to unit test them.

import grin


def read_input():
    lines = []
    label_indices = {}
    line_number = 1
    while True:
        line = input().strip()
        if line == '.':
            break
        if ':' in line:
            label_name, line = line.split(':', 1)
            label_name = label_name.strip()
            label_indices[label_name] = line_number
        lines.append(line.strip())
        line_number += 1
    grin.Basic.labels.update(label_indices)
    return lines


def main():
    lines = read_input()

    try:
        parsed_lines = list(grin.parse(lines))
    except grin.GrinParseError as e:
        print(e)
        return

    line_index = 0
    call_stack = []
    while line_index < len(parsed_lines):
        line = parsed_lines[line_index]

        for token in line:
            if token.kind() == grin.GrinTokenKind.LET:
                grin.let_statement(line)
            elif token.kind() == grin.GrinTokenKind.PRINT:
                grin.print_statement(line)
            elif token.kind() == grin.GrinTokenKind.END:
                grin.end_statement()
                return

            elif token.kind() == grin.GrinTokenKind.INNUM:
                grin.InputHandler.innum_statement(line)
            elif token.kind() == grin.GrinTokenKind.INSTR:
                grin.InputHandler.instr_statement(line)

            elif token.kind() == grin.GrinTokenKind.ADD:
                grin.MathHandler.add_statement(line)
            elif token.kind() == grin.GrinTokenKind.SUB:
                grin.MathHandler.sub_statement(line)
            elif token.kind() == grin.GrinTokenKind.MULT:
                grin.MathHandler.mult_statement(line)
            elif token.kind() == grin.GrinTokenKind.DIV:
                grin.MathHandler.div_statement(line)
            elif token.kind() == grin.GrinTokenKind.GOTO:
                line_index = grin.GotoHandler.go_to_type(line, parsed_lines, line_index)
                break
            elif token.kind() == grin.GrinTokenKind.GOSUB:
                line_index, call_stack = grin.GosubHandler.go_sub_type(line,parsed_lines,line_index, call_stack)
                break
            elif token.kind() == grin.GrinTokenKind.RETURN:
                line_index = grin.GosubHandler.return_statement(call_stack)
                break

        else:
            line_index += 1


if __name__ == '__main__':
    main()
