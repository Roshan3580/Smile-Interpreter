from .tokens import CodePosition

class SmileLexException(Exception):
    def __init__(self, message: str, position: CodePosition):
        formatted = f'Lexical error at {position}: {message}'
        super().__init__(formatted)
        self._position = position
    def location(self) -> CodePosition:
        return self._position

class SmileParseException(Exception):
    def __init__(self, message: str, position: CodePosition):
        formatted = f'Parse error at {position}: {message}'
        super().__init__(formatted)
        self._position = position
    def location(self) -> CodePosition:
        return self._position 