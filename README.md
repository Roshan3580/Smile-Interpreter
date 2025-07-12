# Smile Language Interpreter

A modern, modular implementation of a BASIC-like programming language interpreter with clean architecture and comprehensive error handling.

## Overview

Smile is a complete rewrite of a BASIC-like language interpreter that provides a robust execution environment for simple programming tasks. The interpreter features a modular design with clear separation of concerns, making it both maintainable and extensible.

### Key Features

- **Modular Architecture**: Clean separation of concerns across multiple modules
- **Type Safety**: Comprehensive type hints throughout the codebase
- **Error Handling**: Detailed error messages with precise location information
- **Extensibility**: Easy to add new language features and operations
- **Compatibility**: Full compatibility with the original Grin language specification

## Architecture

The Smile interpreter is organized into a clean, modular structure with the module responsibilities being as follows:

- **`tokens.py`**: Defines token types, categories, and position tracking
- **`exceptions.py`**: Custom exception classes for error handling
- **`state.py`**: Manages global program state (variables, labels)
- **`lexer.py`**: Converts source code text into structured tokens
- **`parser.py`**: Validates syntax and creates instruction sequences
- **`runtime.py`**: Executes instructions and manages program flow

## Installation and Usage

### Prerequisites
- Python 3.7 or higher
- No additional dependencies required

### Running the Interpreter

1. **Clone or download the project files**
2. **Navigate to the project directory**
3. **Run the interpreter**:
   ```bash
   python3 smile_interpreter.py
   ```

## Technical Details

### Error Handling
The interpreter provides detailed error messages including:
- Lexical errors (invalid characters, unterminated strings)
- Parse errors (invalid syntax, missing tokens)
- Runtime errors (undefined variables, division by zero)
- Control flow errors (invalid jumps, unmatched returns)

### Performance Features
- **Efficient Tokenization**: Optimized lexical analysis
- **Streaming Parsing**: Memory-efficient processing of large programs
- **Fast Execution**: Optimized instruction processing loop

### Code Quality
- **Type Safety**: Comprehensive type hints for all functions
- **Documentation**: Extensive docstrings and inline comments
- **Modularity**: Clear separation of concerns
- **Testability**: Well-structured code for unit testing

## Development

### Project Structure
```
Grin/
├── smile/                 # Core interpreter package
│   ├── __init__.py
│   ├── tokens.py
│   ├── exceptions.py
│   ├── state.py
│   ├── lexer.py
│   ├── parser.py
│   └── runtime.py
├── smile_interpreter.py   # Main entry point
└── README.md             # This file
```

### Adding New Features
The modular architecture makes it easy to extend the language:

1. **New Tokens**: Add to `tokens.py`
2. **New Operations**: Implement in `runtime.py`
3. **New Syntax**: Update `parser.py` and `lexer.py`
4. **New Error Types**: Add to `exceptions.py`

## Compatibility

This implementation maintains full compatibility with the original Grin language specification. All valid Grin programs will execute identically on this interpreter while benefiting from improved error handling and maintainability.

---

## Contact Information

**Developer**: Roshan Raj  
**Email**: raj.roshan2005@gmail.com  
**Institution**: University of California, Irvine 