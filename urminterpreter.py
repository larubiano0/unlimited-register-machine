import sys
from commands import *
from special_characters import *

MAX_LENGTH = 16

def file_to_commands(file_code: list) -> list:
    """Takes a list with the lines of the script and returns a list with the commands."""
    instruction_number = 1
    cmds = []

    for line in file_code:
        c = 0
        current_instruction_number = 0
        current_command = ""
        parameters = []
        
        if not line[c]==I:
            raise SyntaxError(f"Error at line {instruction_number}. Each line must start with I.")
        
        c += 1

        while line[c].isdigit():
            current_instruction_number = current_instruction_number*10 + int(line[c])
            c += 1

        if not current_instruction_number:
            raise SyntaxError(f"Error at line {instruction_number}. Each line must have an instruction number.")
        
        if current_instruction_number != instruction_number:
            raise SyntaxError(f"Error at line {instruction_number}. Instruction numbers must be consecutive and start at one.")
        
        c += 1
        if line[c] not in COMMAND_NAMES:
            raise SyntaxError(f"Error at line {instruction_number}. Unknown command.")
        
        current_command = line[c]
        
        c += 1
        if line[c] != LEFT_PARENTHESIS:
            raise SyntaxError(f"Error at line {instruction_number}. Each command must be followed by a left parenthesis.")

        c += 1
        if current_command == ZERO or current_command == SUCCESSOR:
            if not line[c].isdigit():
                raise SyntaxError(f"Error at line {instruction_number}. Check that the parameters of the command are numbers.")
            param1 = 0
            while line[c].isdigit():
                param1 = param1*10 + int(line[c])
                c += 1
            parameters.append(param1)
        elif current_command == TRANSFER:
            if not line[c].isdigit():
                raise SyntaxError(f"Error at line {instruction_number}. Check that the parameters of the command are numbers.")
            param1 = 0
            while line[c].isdigit():
                param1 = param1*10 + int(line[c])
                c += 1
            
            if line[c] != COMA:
                raise SyntaxError(f'''Error at line {instruction_number}.
                                   Check that the parameters of the command are separated by comas.''')
            
            c += 1
            if not line[c].isdigit():
                raise SyntaxError(f"Error at line {instruction_number}. Check that the parameters of the command are numbers.")
            param2 = 0
            while line[c].isdigit():
                param2 = param2*10 + int(line[c])
                c += 1
            parameters.append(param1)
            parameters.append(param2)
        elif current_command == JUMP:
            if not line[c].isdigit():
                raise SyntaxError(f"Error at line {instruction_number}. Check that the parameters of the command are numbers.")
            param1 = 0
            while line[c].isdigit():
                param1 = param1*10 + int(line[c])
                c += 1

            if line[c] != COMA:
                raise SyntaxError(f"Error at line {instruction_number}. Check that the parameters of the command are separated by comas.")
            c += 1
            if not line[c].isdigit():
                raise SyntaxError(f"Error at line {instruction_number}. Check that the parameters of the command are numbers.")
            param2 = 0
            while line[c].isdigit():
                param2 = param2*10 + int(line[c])
                c += 1

            if line[c] != COMA:
                raise SyntaxError(f"Error at line {instruction_number}. Check that the parameters of the command are separated by comas.")
            c += 1
            if not line[c].isdigit():
                raise SyntaxError(f"Error at line {instruction_number}. Check that the parameters of the command are numbers.")
            param3 = 0
            while line[c].isdigit():
                param3 = param3*10 + int(line[c])
                c += 1
            parameters.append(param1)
            parameters.append(param2)
            parameters.append(param3)
        
        if line[c] != RIGHT_PARENTHESIS:
            raise SyntaxError(f"Error at line {instruction_number}. Each command must end with a right parenthesis.")
        
        cmds.append([current_command, parameters])
        
        instruction_number += 1

    return cmds

def execute_program(cmds: list, parameters: list) -> None:
    """Takes a list with the commands and a list with the parameters and executes the program."""
    register = [0 for _ in range(MAX_LENGTH)]
    for i in range(len(parameters)):
        register[i] = parameters[i]

    number_of_instructions = len(cmds)
    
    c = 0
    while c < number_of_instructions:
        current_command, parameters = cmds[c]
        if current_command == ZERO:
            if not 1 <= parameters[0] <= MAX_LENGTH:
                raise SyntaxError(f"Error at instruction {c+1}. The register must be in the range [1, {MAX_LENGTH}].")
            register[parameters[0]-1] = 0
        elif current_command == SUCCESSOR:
            if not 1 <= parameters[0] <= MAX_LENGTH:
                raise SyntaxError(f"Error at instruction {c+1}. The register must be in the range [1, {MAX_LENGTH}].")
            register[parameters[0]-1] += 1
        elif current_command == TRANSFER:
            if not 1 <= parameters[0] <= MAX_LENGTH or not 1 <= parameters[1] <= MAX_LENGTH:
                raise SyntaxError(f"Error at instruction {c+1}. The registers must be in the range [1, {MAX_LENGTH}].")
            register[parameters[1]-1] = register[parameters[0]-1]
        elif current_command == JUMP:
            if register[parameters[0]-1] == register[parameters[1]-1]:
                c = parameters[2] - 2
        c += 1
    
    return register

def interpretate(path: str) -> None:
    """Takes a string with the path to the script and interpretates it."""
    try:
        with open(path, "r", encoding='utf-8') as script:
            file_code = script.read().lower().split("\n")
        
        cmds = file_to_commands(file_code)

    except OSError as e:
        print(f"Could not open {path}:\n{e}\n", file=sys.stderr)


    parameters_raw = input("Enter the parameters of f separated by comas: ").replace(" ","").split(',')
    for i in parameters_raw:
        if not i.isdigit():
            raise SyntaxError("Parameters must be numbers.")
        
    parameters = [int(i) for i in parameters_raw]

    if len(parameters)>20:
        raise SyntaxError(f"The register has a maximum length of {MAX_LENGTH}.")

    register = execute_program(cmds, parameters)

    print(f"f({str(parameters)[1:-1]})⭣ {register[0]}")


if __name__ == "__main__":
    interpretate(sys.argv[1])
