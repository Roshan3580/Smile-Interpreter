from collections import defaultdict
from .tokens import SmileTokenType, SmileToken, CodePosition, SmileTokenCategory
from .exceptions import SmileLexException

class Tokenizer:
    _COMMAND_MAPPING = defaultdict(
        lambda: SmileTokenType.VARIABLE_NAME,
        {
            'LET': SmileTokenType.ASSIGN,
            'PRINT': SmileTokenType.OUTPUT,
            'END': SmileTokenType.TERMINATE,
            'INNUM': SmileTokenType.NUMERIC_INPUT,
            'INSTR': SmileTokenType.TEXT_INPUT,
            'ADD': SmileTokenType.ADDITION,
            'SUB': SmileTokenType.SUBTRACTION,
            'MULT': SmileTokenType.MULTIPLICATION,
            'DIV': SmileTokenType.DIVISION,
            'GOTO': SmileTokenType.JUMP,
            'GOSUB': SmileTokenType.SUBROUTINE_CALL,
            'RETURN': SmileTokenType.SUBROUTINE_RETURN,
            'IF': SmileTokenType.CONDITIONAL
        }
    )
    _RESERVED_WORDS = frozenset(_COMMAND_MAPPING.keys())

    @classmethod
    def tokenize_line(cls, source_line: str, line_number: int):
        tokens = []
        char_index = 0
        while char_index < len(source_line):
            while char_index < len(source_line) and source_line[char_index].isspace():
                char_index += 1
            if char_index >= len(source_line):
                break
            token_start = char_index
            if source_line[char_index].isalpha():
                char_index += 1
                while char_index < len(source_line) and source_line[char_index].isalnum():
                    char_index += 1
                word = source_line[token_start:char_index]
                token_type = cls._COMMAND_MAPPING[word]
                tokens.append(SmileToken(token_type, word, CodePosition(line_number, token_start + 1), word))
            elif source_line[char_index] == '"':
                char_index += 1
                string_start = char_index
                while char_index < len(source_line) and source_line[char_index] != '"':
                    char_index += 1
                if char_index >= len(source_line):
                    raise SmileLexException('Unterminated string literal', CodePosition(line_number, token_start + 1))
                string_content = source_line[string_start:char_index]
                char_index += 1
                tokens.append(SmileToken(SmileTokenType.STRING_DATA, f'"{string_content}"', CodePosition(line_number, token_start + 1), string_content))
            elif source_line[char_index] == '-' or source_line[char_index].isdigit():
                is_negative = source_line[char_index] == '-'
                if is_negative:
                    char_index += 1
                if char_index >= len(source_line) or not source_line[char_index].isdigit():
                    if is_negative:
                        raise SmileLexException('Negative sign must be followed by digits', CodePosition(line_number, token_start + 1))
                while char_index < len(source_line) and source_line[char_index].isdigit():
                    char_index += 1
                if char_index < len(source_line) and source_line[char_index] == '.':
                    char_index += 1
                    while char_index < len(source_line) and source_line[char_index].isdigit():
                        char_index += 1
                    number_value = float(source_line[token_start:char_index])
                    token_type = SmileTokenType.FLOAT_DATA
                else:
                    number_value = int(source_line[token_start:char_index])
                    token_type = SmileTokenType.INTEGER_DATA
                tokens.append(SmileToken(token_type, source_line[token_start:char_index], CodePosition(line_number, token_start + 1), number_value))
            elif source_line[char_index] == ':':
                char_index += 1
                tokens.append(SmileToken(SmileTokenType.COLON, ':', CodePosition(line_number, token_start + 1)))
            elif source_line[char_index] == '.':
                char_index += 1
                tokens.append(SmileToken(SmileTokenType.PERIOD, '.', CodePosition(line_number, token_start + 1)))
            elif source_line[char_index] == '=':
                char_index += 1
                tokens.append(SmileToken(SmileTokenType.EQUALS, '=', CodePosition(line_number, token_start + 1)))
            elif source_line[char_index] == '<':
                char_index += 1
                if char_index < len(source_line) and source_line[char_index] == '>':
                    char_index += 1
                    tokens.append(SmileToken(SmileTokenType.NOT_EQUALS, '<>', CodePosition(line_number, token_start + 1)))
                elif char_index < len(source_line) and source_line[char_index] == '=':
                    char_index += 1
                    tokens.append(SmileToken(SmileTokenType.LESS_EQUAL, '<=', CodePosition(line_number, token_start + 1)))
                else:
                    tokens.append(SmileToken(SmileTokenType.LESS, '<', CodePosition(line_number, token_start + 1)))
            elif source_line[char_index] == '>':
                char_index += 1
                if char_index < len(source_line) and source_line[char_index] == '=':
                    char_index += 1
                    tokens.append(SmileToken(SmileTokenType.GREATER_EQUAL, '>=', CodePosition(line_number, token_start + 1)))
                else:
                    tokens.append(SmileToken(SmileTokenType.GREATER, '>', CodePosition(line_number, token_start + 1)))
            else:
                raise SmileLexException(f'Invalid character: {source_line[char_index]}', CodePosition(line_number, char_index + 1))
        return tokens 