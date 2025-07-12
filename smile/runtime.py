from typing import List, Any, Tuple, Optional
from .tokens import SmileToken, SmileTokenType
from .state import ProgramState
import sys

class VariableManager:
    @classmethod
    def assign_value(cls, instruction: List[SmileToken]):
        var_name = None
        var_value = None
        for token in instruction:
            if token.kind() == SmileTokenType.VARIABLE_NAME:
                var_name = token.text()
            elif token.kind() in [SmileTokenType.INTEGER_DATA, SmileTokenType.FLOAT_DATA]:
                var_value = token.value()
            elif token.kind() == SmileTokenType.STRING_DATA:
                var_value = token.value()
        if var_name and var_value is not None:
            ProgramState.variable_storage[var_name] = var_value

class OutputManager:
    @classmethod
    def display_content(cls, instruction: List[SmileToken]):
        for token in instruction:
            if token.kind() == SmileTokenType.VARIABLE_NAME:
                var_name = token.text()
                if var_name in ProgramState.variable_storage:
                    print(ProgramState.variable_storage[var_name])
                else:
                    print(0)
            elif token.kind() == SmileTokenType.STRING_DATA:
                print(token.value())

class InputProcessor:
    @classmethod
    def handle_numeric_input(cls, instruction: List[SmileToken]):
        var_name = None
        for token in instruction:
            if token.kind() == SmileTokenType.VARIABLE_NAME:
                var_name = token.text()
                break
        if var_name:
            try:
                user_input = input().strip()
                if '.' in user_input:
                    converted_value = float(user_input)
                else:
                    converted_value = int(user_input)
                ProgramState.variable_storage[var_name] = converted_value
            except ValueError:
                print(f"Error: Invalid numeric input for variable {var_name}")
                sys.exit(1)
    @classmethod
    def handle_text_input(cls, instruction: List[SmileToken]):
        var_name = None
        for token in instruction:
            if token.kind() == SmileTokenType.VARIABLE_NAME:
                var_name = token.text()
                break
        if var_name:
            user_input = input().strip()
            ProgramState.variable_storage[var_name] = user_input

class ArithmeticEngine:
    @classmethod
    def perform_addition(cls, instruction: List[SmileToken]):
        var_name, operand = cls._extract_operation_components(instruction)
        if var_name and operand is not None:
            cls._execute_arithmetic_operation(var_name, operand, 'addition')
    @classmethod
    def perform_subtraction(cls, instruction: List[SmileToken]):
        var_name, operand = cls._extract_operation_components(instruction)
        if var_name and operand is not None:
            cls._execute_arithmetic_operation(var_name, operand, 'subtraction')
    @classmethod
    def perform_multiplication(cls, instruction: List[SmileToken]):
        var_name, operand = cls._extract_operation_components(instruction)
        if var_name and operand is not None:
            cls._execute_arithmetic_operation(var_name, operand, 'multiplication')
    @classmethod
    def perform_division(cls, instruction: List[SmileToken]):
        var_name, operand = cls._extract_operation_components(instruction)
        if var_name and operand is not None:
            cls._execute_arithmetic_operation(var_name, operand, 'division')
    @classmethod
    def _extract_operation_components(cls, instruction: List[SmileToken]) -> Tuple[Optional[str], Optional[Any]]:
        if len(instruction) < 3:
            print("Error: Invalid operation format")
            sys.exit(1)
        var_name = None
        operand = None
        if instruction[1].kind() == SmileTokenType.VARIABLE_NAME:
            var_name = instruction[1].text()
        if instruction[2].kind() in [SmileTokenType.INTEGER_DATA, SmileTokenType.FLOAT_DATA, SmileTokenType.STRING_DATA]:
            operand = instruction[2].value()
        elif instruction[2].kind() == SmileTokenType.VARIABLE_NAME:
            operand = ProgramState.variable_storage.get(instruction[2].text())
        return var_name, operand
    @classmethod
    def _execute_arithmetic_operation(cls, var_name: str, operand: Any, operation: str):
        current_value = ProgramState.variable_storage.get(var_name)
        if current_value is None:
            print(f"Error: Variable {var_name} not defined")
            sys.exit(1)
        result = None
        if operation == 'addition':
            if isinstance(current_value, str) and isinstance(operand, str):
                result = current_value + operand
            elif isinstance(current_value, (int, float)) and isinstance(operand, (int, float)):
                result = current_value + operand
            else:
                print("Error: Invalid addition operation")
                sys.exit(1)
        elif operation == 'subtraction':
            if isinstance(current_value, (int, float)) and isinstance(operand, (int, float)):
                result = current_value - operand
            else:
                print("Error: Invalid subtraction operation")
                sys.exit(1)
        elif operation == 'multiplication':
            if isinstance(current_value, str) and isinstance(operand, int) and operand >= 0:
                result = current_value * operand
            elif isinstance(current_value, int) and isinstance(operand, str) and current_value >= 0:
                result = operand * current_value
            elif isinstance(current_value, (int, float)) and isinstance(operand, (int, float)):
                result = current_value * operand
            else:
                print("Error: Invalid multiplication operation")
                sys.exit(1)
        elif operation == 'division':
            if isinstance(current_value, int) and isinstance(operand, int) and operand != 0:
                result = current_value // operand
            elif isinstance(current_value, (int, float)) and isinstance(operand, (int, float)) and operand != 0:
                result = current_value / operand
            else:
                print("Error: Invalid division operation")
                sys.exit(1)
        ProgramState.variable_storage[var_name] = result

class FlowController:
    @classmethod
    def execute_jump(cls, instruction: List[SmileToken], all_instructions: List[List[SmileToken]], current_position: int) -> int:
        if len(instruction) == 2:
            return cls._execute_simple_jump(instruction, all_instructions, current_position)
        elif len(instruction) == 6:
            return cls._execute_conditional_jump(instruction, all_instructions, current_position)
        else:
            print("Error: Invalid jump format")
            sys.exit(1)
    @classmethod
    def execute_subroutine_call(cls, instruction: List[SmileToken], all_instructions: List[List[SmileToken]], current_position: int, call_stack: List[int]) -> Tuple[int, List[int]]:
        if len(instruction) == 2:
            return cls._execute_simple_subroutine_call(instruction, all_instructions, current_position, call_stack)
        elif len(instruction) == 6:
            return cls._execute_conditional_subroutine_call(instruction, all_instructions, current_position, call_stack)
        else:
            print("Error: Invalid subroutine call format")
            sys.exit(1)
    @classmethod
    def execute_subroutine_return(cls, call_stack: List[int]) -> int:
        if not call_stack:
            print("Error: RETURN without matching subroutine call")
            sys.exit(1)
        return call_stack.pop()
    @classmethod
    def _execute_simple_jump(cls, instruction: List[SmileToken], all_instructions: List[List[SmileToken]], current_position: int) -> int:
        target = cls._extract_jump_target(instruction)
        return cls._resolve_jump_target(target, all_instructions, current_position)
    @classmethod
    def _execute_conditional_jump(cls, instruction: List[SmileToken], all_instructions: List[List[SmileToken]], current_position: int) -> int:
        condition_met = cls._evaluate_condition(instruction[2:])
        if condition_met:
            return cls._execute_simple_jump(instruction[:2], all_instructions, current_position)
        return current_position + 1
    @classmethod
    def _execute_simple_subroutine_call(cls, instruction: List[SmileToken], all_instructions: List[List[SmileToken]], current_position: int, call_stack: List[int]) -> Tuple[int, List[int]]:
        target = cls._extract_jump_target(instruction)
        target_position = cls._resolve_jump_target(target, all_instructions, current_position)
        call_stack.append(current_position + 1)
        return target_position, call_stack
    @classmethod
    def _execute_conditional_subroutine_call(cls, instruction: List[SmileToken], all_instructions: List[List[SmileToken]], current_position: int, call_stack: List[int]) -> Tuple[int, List[int]]:
        condition_met = cls._evaluate_condition(instruction[2:])
        if condition_met:
            return cls._execute_simple_subroutine_call(instruction[:2], all_instructions, current_position, call_stack)
        return current_position + 1, call_stack
    @classmethod
    def _extract_jump_target(cls, instruction: List[SmileToken]) -> str:
        for token in instruction:
            if token.kind() in [SmileTokenType.INTEGER_DATA, SmileTokenType.STRING_DATA]:
                return token.text()
        print("Error: Jump target not specified")
        sys.exit(1)
    @classmethod
    def _resolve_jump_target(cls, target: str, all_instructions: List[List[SmileToken]], current_position: int) -> int:
        if target.isdigit() or (target.startswith('-') and target[1:].isdigit()):
            offset = int(target)
            if offset == 0:
                print("Error: Jump offset of 0 causes infinite loop")
                sys.exit(1)
            target_position = current_position + offset
            if 0 <= target_position < len(all_instructions):
                return target_position
            else:
                print(f"Error: Jump target position {target_position} out of range")
                sys.exit(1)
        elif target.startswith('"') and target.endswith('"'):
            label_name = target[1:-1]
            if label_name in ProgramState.label_registry:
                label_position = ProgramState.label_registry[label_name]
                if 0 <= label_position - 1 < len(all_instructions):
                    return label_position - 1
                else:
                    print(f"Error: Label position {label_position} out of range")
                    sys.exit(1)
            else:
                print(f"Error: Label '{label_name}' not found")
                sys.exit(1)
        else:
            print(f"Error: Invalid jump target '{target}'")
            sys.exit(1)
    @classmethod
    def _evaluate_condition(cls, condition_tokens: List[SmileToken]) -> bool:
        if len(condition_tokens) != 4:
            print("Error: Invalid conditional expression")
            sys.exit(1)
        left_operand = cls._get_operand_value(condition_tokens[0])
        operator = condition_tokens[1].text()
        right_operand = cls._get_operand_value(condition_tokens[2])
        if left_operand is None or right_operand is None:
            print("Error: Undefined variable in condition")
            sys.exit(1)
        if operator == '=':
            return left_operand == right_operand
        elif operator == '<>':
            return left_operand != right_operand
        elif operator == '<':
            return left_operand < right_operand
        elif operator == '<=':
            return left_operand <= right_operand
        elif operator == '>':
            return left_operand > right_operand
        elif operator == '>=':
            return left_operand >= right_operand
        else:
            print(f"Error: Unknown comparison operator '{operator}'")
            sys.exit(1)
    @classmethod
    def _get_operand_value(cls, token: SmileToken) -> Any:
        if token.kind() in [SmileTokenType.INTEGER_DATA, SmileTokenType.FLOAT_DATA]:
            return token.value()
        elif token.kind() == SmileTokenType.VARIABLE_NAME:
            return ProgramState.variable_storage.get(token.text())
        return None 