from enum import Enum
from typing import Any

class SmileTokenCategory(Enum):
    COMPARISON = 1
    VARIABLE = 2
    COMMAND = 3
    DATA = 4
    SYMBOL = 5

class SmileTokenType(Enum):
    ADDITION = (1, SmileTokenCategory.COMMAND)
    COLON = (2, SmileTokenCategory.SYMBOL)
    DIVISION = (3, SmileTokenCategory.COMMAND)
    PERIOD = (4, SmileTokenCategory.SYMBOL)
    TERMINATE = (5, SmileTokenCategory.COMMAND)
    EQUALS = (6, SmileTokenCategory.COMPARISON)
    SUBROUTINE_CALL = (7, SmileTokenCategory.COMMAND)
    JUMP = (8, SmileTokenCategory.COMMAND)
    GREATER = (9, SmileTokenCategory.COMPARISON)
    GREATER_EQUAL = (10, SmileTokenCategory.COMPARISON)
    VARIABLE_NAME = (11, SmileTokenCategory.VARIABLE)
    CONDITIONAL = (12, SmileTokenCategory.COMMAND)
    NUMERIC_INPUT = (13, SmileTokenCategory.COMMAND)
    TEXT_INPUT = (14, SmileTokenCategory.COMMAND)
    LESS = (15, SmileTokenCategory.COMPARISON)
    LESS_EQUAL = (16, SmileTokenCategory.COMPARISON)
    ASSIGN = (17, SmileTokenCategory.COMMAND)
    FLOAT_DATA = (18, SmileTokenCategory.DATA)
    INTEGER_DATA = (19, SmileTokenCategory.DATA)
    STRING_DATA = (20, SmileTokenCategory.DATA)
    MULTIPLICATION = (21, SmileTokenCategory.COMMAND)
    NOT_EQUALS = (22, SmileTokenCategory.COMPARISON)
    OUTPUT = (23, SmileTokenCategory.COMMAND)
    SUBROUTINE_RETURN = (24, SmileTokenCategory.COMMAND)
    SUBTRACTION = (25, SmileTokenCategory.COMMAND)

    def __init__(self, index: int, category: SmileTokenCategory):
        self._index = index
        self._category = category

    def index(self) -> int:
        return self._index

    def category(self) -> SmileTokenCategory:
        return self._category

class CodePosition:
    def __init__(self, line: int, column: int):
        if line < 1:
            raise ValueError(f'Line number must be positive, got {line}')
        if column < 1:
            raise ValueError(f'Column number must be positive, got {column}')
        self._line = line
        self._column = column
    def line(self) -> int:
        return self._line
    def column(self) -> int:
        return self._column
    def __str__(self) -> str:
        return f'Line {self._line} Column {self._column}'
    def __repr__(self) -> str:
        return f'CodePosition({self._line}, {self._column})'
    def __eq__(self, other):
        return (isinstance(other, CodePosition) and self._line == other._line and self._column == other._column)

class SmileToken:
    def __init__(self, token_type: SmileTokenType, text: str, position: CodePosition, value: Any = None):
        self._type = token_type
        self._text = text
        self._position = position
        self._value = value
    def kind(self) -> SmileTokenType:
        return self._type
    def text(self) -> str:
        return self._text
    def location(self) -> CodePosition:
        return self._position
    def value(self) -> Any:
        return self._value
    def __eq__(self, other):
        return (isinstance(other, SmileToken) and self._type == other._type and self._text == other._text and self._position == other._position and self._value == other._value) 