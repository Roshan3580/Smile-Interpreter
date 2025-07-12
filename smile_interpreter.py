import smile


def collect_program_lines():
    """Gather program lines from user input until termination marker"""
    program_lines = []
    label_mappings = {}
    current_line_num = 1
    
    while True:
        user_input = input().strip()
        if user_input == '.':
            break
            
        # Handle label definitions
        if ':' in user_input:
            label_part, code_part = user_input.split(':', 1)
            label_name = label_part.strip()
            label_mappings[label_name] = current_line_num
            user_input = code_part.strip()
            
        program_lines.append(user_input)
        current_line_num += 1
    
    # Update global label registry
    smile.ProgramState.label_registry.update(label_mappings)
    return program_lines


def execute_program():
    """Main program execution loop"""
    source_lines = collect_program_lines()
    
    try:
        processed_instructions = list(smile.process_source(source_lines))
    except smile.SmileParseException as parse_error:
        print(parse_error)
        return
    
    instruction_pointer = 0
    subroutine_stack = []
    
    while instruction_pointer < len(processed_instructions):
        current_instruction = processed_instructions[instruction_pointer]
        
        for instruction_token in current_instruction:
            token_type = instruction_token.kind()
            
            # Variable assignment operations
            if token_type == smile.SmileTokenType.ASSIGN:
                smile.VariableManager.assign_value(current_instruction)
            elif token_type == smile.SmileTokenType.OUTPUT:
                smile.OutputManager.display_content(current_instruction)
            elif token_type == smile.SmileTokenType.TERMINATE:
                smile.ProgramState.terminate_execution()
                return
            
            # Input operations
            elif token_type == smile.SmileTokenType.NUMERIC_INPUT:
                smile.InputProcessor.handle_numeric_input(current_instruction)
            elif token_type == smile.SmileTokenType.TEXT_INPUT:
                smile.InputProcessor.handle_text_input(current_instruction)
            
            # Arithmetic operations
            elif token_type == smile.SmileTokenType.ADDITION:
                smile.ArithmeticEngine.perform_addition(current_instruction)
            elif token_type == smile.SmileTokenType.SUBTRACTION:
                smile.ArithmeticEngine.perform_subtraction(current_instruction)
            elif token_type == smile.SmileTokenType.MULTIPLICATION:
                smile.ArithmeticEngine.perform_multiplication(current_instruction)
            elif token_type == smile.SmileTokenType.DIVISION:
                smile.ArithmeticEngine.perform_division(current_instruction)
            
            # Control flow operations
            elif token_type == smile.SmileTokenType.JUMP:
                instruction_pointer = smile.FlowController.execute_jump(
                    current_instruction, processed_instructions, instruction_pointer)
                break
            elif token_type == smile.SmileTokenType.SUBROUTINE_CALL:
                instruction_pointer, subroutine_stack = smile.FlowController.execute_subroutine_call(
                    current_instruction, processed_instructions, instruction_pointer, subroutine_stack)
                break
            elif token_type == smile.SmileTokenType.SUBROUTINE_RETURN:
                instruction_pointer = smile.FlowController.execute_subroutine_return(subroutine_stack)
                break
        
        else:
            instruction_pointer += 1


if __name__ == '__main__':
    execute_program() 