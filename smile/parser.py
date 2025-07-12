from typing import List, Iterable
from .tokens import SmileToken, SmileTokenType, CodePosition
from .lexer import Tokenizer
from .exceptions import SmileParseException

class Parser:
    @classmethod
    def parse_source(cls, source_lines: List[str]) -> Iterable[List[SmileToken]]:
        for line_num, source_line in enumerate(source_lines, 1):
            tokens = cls._parse_single_line(source_line, line_num)
            if len(tokens) == 1 and tokens[0].kind() == SmileTokenType.PERIOD:
                return
            yield tokens
    @classmethod
    def _parse_single_line(cls, source_line: str, line_number: int) -> List[SmileToken]:
        tokens = Tokenizer.tokenize_line(source_line, line_number)
        if not tokens:
            raise SmileParseException('Empty program lines are not allowed', CodePosition(line_number, len(source_line) + 1))
        token_index = 0
        if token_index < len(tokens) and tokens[token_index].kind() == SmileTokenType.VARIABLE_NAME:
            token_index += 1
            if token_index < len(tokens) and tokens[token_index].kind() == SmileTokenType.COLON:
                token_index += 1
            else:
                raise SmileParseException('Label must be followed by colon', tokens[token_index - 1].location())
        if token_index >= len(tokens):
            raise SmileParseException('Statement body required', CodePosition(line_number, len(source_line) + 1))
        statement_token = tokens[token_index]
        token_index += 1
        cls._validate_statement_arguments(tokens, token_index, statement_token.kind())
        return tokens
    @classmethod
    def _validate_statement_arguments(cls, tokens: List[SmileToken], start_index: int, statement_type: SmileTokenType):
        if statement_type in [SmileTokenType.ASSIGN, SmileTokenType.ADDITION, SmileTokenType.SUBTRACTION, SmileTokenType.MULTIPLICATION, SmileTokenType.DIVISION]:
            cls._validate_assignment_statement(tokens, start_index)
        elif statement_type == SmileTokenType.OUTPUT:
            cls._validate_output_statement(tokens, start_index)
        elif statement_type in [SmileTokenType.NUMERIC_INPUT, SmileTokenType.TEXT_INPUT]:
            cls._validate_input_statement(tokens, start_index)
        elif statement_type in [SmileTokenType.JUMP, SmileTokenType.SUBROUTINE_CALL]:
            cls._validate_jump_statement(tokens, start_index)
        elif statement_type in [SmileTokenType.TERMINATE, SmileTokenType.SUBROUTINE_RETURN]:
            pass
        else:
            raise SmileParseException(f'Invalid statement type: {statement_type}', tokens[start_index - 1].location())
    @classmethod
    def _validate_assignment_statement(cls, tokens: List[SmileToken], start_index: int):
        if start_index >= len(tokens):
            raise SmileParseException('Variable name expected', CodePosition(1, 1))
        if tokens[start_index].kind() != SmileTokenType.VARIABLE_NAME:
            raise SmileParseException('Variable name expected', tokens[start_index].location())
        if start_index + 1 >= len(tokens):
            raise SmileParseException('Value expected', CodePosition(1, 1))
        cls._validate_value(tokens[start_index + 1])
    @classmethod
    def _validate_output_statement(cls, tokens: List[SmileToken], start_index: int):
        if start_index < len(tokens):
            cls._validate_value(tokens[start_index])
    @classmethod
    def _validate_input_statement(cls, tokens: List[SmileToken], start_index: int):
        if start_index >= len(tokens):
            raise SmileParseException('Variable name expected', CodePosition(1, 1))
        if tokens[start_index].kind() != SmileTokenType.VARIABLE_NAME:
            raise SmileParseException('Variable name expected', tokens[start_index].location())
    @classmethod
    def _validate_jump_statement(cls, tokens: List[SmileToken], start_index: int):
        if start_index >= len(tokens):
            raise SmileParseException('Jump target expected', CodePosition(1, 1))
        cls._validate_jump_target(tokens[start_index])
        if start_index + 1 < len(tokens) and tokens[start_index + 1].kind() == SmileTokenType.CONDITIONAL:
            if start_index + 4 >= len(tokens):
                raise SmileParseException('Incomplete conditional expression', tokens[start_index + 1].location())
            cls._validate_value(tokens[start_index + 2])
            cls._validate_comparison_operator(tokens[start_index + 3])
            cls._validate_value(tokens[start_index + 4])
    @classmethod
    def _validate_value(cls, token: SmileToken):
        valid_types = [SmileTokenType.INTEGER_DATA, SmileTokenType.FLOAT_DATA, SmileTokenType.STRING_DATA, SmileTokenType.VARIABLE_NAME]
        if token.kind() not in valid_types:
            raise SmileParseException('Invalid value type', token.location())
    @classmethod
    def _validate_jump_target(cls, token: SmileToken):
        valid_types = [SmileTokenType.INTEGER_DATA, SmileTokenType.STRING_DATA, SmileTokenType.VARIABLE_NAME]
        if token.kind() not in valid_types:
            raise SmileParseException('Invalid jump target', token.location())
    @classmethod
    def _validate_comparison_operator(cls, token: SmileToken):
        valid_types = [SmileTokenType.EQUALS, SmileTokenType.NOT_EQUALS, SmileTokenType.LESS, SmileTokenType.LESS_EQUAL, SmileTokenType.GREATER, SmileTokenType.GREATER_EQUAL]
        if token.kind() not in valid_types:
            raise SmileParseException('Invalid comparison operator', token.location())

def process_source(source_lines: List[str]) -> Iterable[List[SmileToken]]:
    return Parser.parse_source(source_lines) 