import sys
import time

from commands import *
from special_characters import *
from config import *


def file_to_commands(file_code: list) -> list:
    """Takes a list with the lines of the script and returns a list with the commands."""
    instruction_number = 1
    cmds = []

    for line in file_code:
        c = 0
        current_instruction_number = 0
        current_command = ""
        parameters = []

        if not line[c] == I:
            raise SyntaxError(
                f"Error at line {instruction_number}. Each line must start with I.")

        c += 1

        while line[c].isdigit():
            current_instruction_number = current_instruction_number * \
                10 + int(line[c])
            c += 1

        if not current_instruction_number:
            raise SyntaxError(
                f"Error at line {instruction_number}. Each line must have an instruction number.")

        if current_instruction_number != instruction_number:
            raise SyntaxError(
                f"Error at line {instruction_number}. Instruction numbers must be consecutive and start at one.")

        c += 1
        if line[c] not in COMMAND_NAMES:
            raise SyntaxError(
                f"Error at line {instruction_number}. Unknown command.")

        current_command = line[c]

        c += 1
        if line[c] != LEFT_PARENTHESIS:
            raise SyntaxError(
                f"Error at line {instruction_number}. Each command must be followed by a left parenthesis.")

        c += 1
        if current_command == ZERO or current_command == SUCCESSOR:
            if not line[c].isdigit():
                raise SyntaxError(
                    f"Error at line {instruction_number}. Check that the parameters of the command are numbers.")
            param1 = 0
            while line[c].isdigit():
                param1 = param1 * 10 + int(line[c])
                c += 1
            parameters.append(param1)
        elif current_command == TRANSFER:
            if not line[c].isdigit():
                raise SyntaxError(
                    f"Error at line {instruction_number}. Check that the parameters of the command are numbers.")
            param1 = 0
            while line[c].isdigit():
                param1 = param1 * 10 + int(line[c])
                c += 1

            if line[c] != COMA:
                raise SyntaxError(f'''Error at line {instruction_number}.
                                   Check that the parameters of the command are separated by comas.''')

            c += 1
            if not line[c].isdigit():
                raise SyntaxError(
                    f"Error at line {instruction_number}. Check that the parameters of the command are numbers.")
            param2 = 0
            while line[c].isdigit():
                param2 = param2 * 10 + int(line[c])
                c += 1
            parameters.append(param1)
            parameters.append(param2)
        elif current_command == JUMP:
            if not line[c].isdigit():
                raise SyntaxError(
                    f"Error at line {instruction_number}. Check that the parameters of the command are numbers.")
            param1 = 0
            while line[c].isdigit():
                param1 = param1 * 10 + int(line[c])
                c += 1

            if line[c] != COMA:
                raise SyntaxError(
                    f"Error at line {instruction_number}. Check that the parameters of the command are separated by comas.")
            c += 1
            if not line[c].isdigit():
                raise SyntaxError(
                    f"Error at line {instruction_number}. Check that the parameters of the command are numbers.")
            param2 = 0
            while line[c].isdigit():
                param2 = param2 * 10 + int(line[c])
                c += 1

            if line[c] != COMA:
                raise SyntaxError(
                    f"Error at line {instruction_number}. Check that the parameters of the command are separated by comas.")
            c += 1
            if not line[c].isdigit():
                raise SyntaxError(
                    f"Error at line {instruction_number}. Check that the parameters of the command are numbers.")
            param3 = 0
            while line[c].isdigit():
                param3 = param3 * 10 + int(line[c])
                c += 1
            parameters.append(param1)
            parameters.append(param2)
            parameters.append(param3)

        if line[c] != RIGHT_PARENTHESIS:
            raise SyntaxError(
                f"Error at line {instruction_number}. Each command must end with a right parenthesis.")

        cmds.append([current_command, parameters])

        instruction_number += 1

    return cmds


def draw_arrow(pointer, square_size, label_height, screen):
    arrow_shaft_start = (
        pointer * square_size + square_size / 2,
        1.5 * square_size + label_height)
    arrow_shaft_end = (
        pointer *
        square_size +
        square_size /
        2,
        square_size +
        label_height)
    arrow_head_tip = (
        pointer *
        square_size +
        square_size /
        2,
        square_size +
        label_height)
    arrow_head_left = (pointer * square_size +
                       square_size /
                       2 -
                       square_size /
                       10,
                       square_size +
                       label_height +
                       square_size /
                       10)
    arrow_head_right = (pointer * square_size +
                        square_size / 2 + square_size / 10,
                        square_size + label_height + square_size / 10)
    # Define the color of the arrow
    # Draw the arrow shaft
    pygame.draw.line(
        screen,
        ARROW_COLOR,
        arrow_shaft_start,
        arrow_shaft_end,
        3)

    # Draw the arrow head
    pygame.draw.polygon(
        screen, ARROW_COLOR, [
            arrow_head_tip, arrow_head_left, arrow_head_right])

    return arrow_shaft_start, arrow_shaft_end


def draw_bold_horizontal_arrow(
        screen,
        SCREENWIDTH: int,
        SCREENHEIGHT: int,
        square_size: int):
    x_center = 2 * SCREENWIDTH / 7
    y_center = 2 * square_size + (SCREENHEIGHT - 2 * square_size) / 2

    # Draw triangle that points to the right, and the right corner is at
    # (x_center, y_center)
    pygame.draw.polygon(screen,
                        ARROW_COLOR,
                        [(x_center,
                          y_center),
                         (x_center - square_size,
                          y_center + square_size / 2),
                            (x_center - square_size,
                             y_center - square_size / 2)])

    return y_center


def instructions_to_labels(font, cmds: list):
    '''For each instruction in cmds draw on the screen Ii COMMAND(parameters)
    where i is the instruction number (starting at 1) and COMMAND is the command and parameters is the list of parameter'''

    instruction_number = 1
    labels = []
    for line in cmds:
        current_command, parameters = line
        label = font.render(
            f"I{instruction_number} {current_command.upper()}({','.join(map(str, parameters))})",
            1,
            ARROW_COLOR)
        labels.append(label)
        instruction_number += 1

    return labels


def draw_labels(
        screen,
        labels: list,
        square_size: int,
        SCREENWIDTH: int,
        SCREENHEIGHT: int,
        y_height: int,
        c: int):
    k = 0

    while k < len(labels):
        # Verify the label [c+k] exists
        if c + k < len(labels):
            # Draw the label
            label_width = labels[c + k].get_width()
            label_height = labels[c + k].get_height()
            if (y_height + k * square_size + label_height / 2 <= SCREENHEIGHT):
                screen.blit(labels[c + k],
                            (SCREENWIDTH / 2 - label_width / 2,
                             y_height + k * square_size - label_height / 2))

        # Verify the label [c-k] exists
        if c - k >= 0:
            # Draw the label
            label_width = labels[c - k].get_width()
            label_height = labels[c - k].get_height()
            if (y_height - k * square_size - label_height / 2 >= 2 * square_size):
                screen.blit(labels[c - k],
                            (SCREENWIDTH / 2 - label_width / 2,
                             y_height - k * square_size - label_height / 2))

        k += 1


def refresh_screen(
        screen,
        square_size: int,
        visual_interface: bool,
        font,
        SCREENWIDTH: int,
        SCREENHEIGHT: int,
        register: list,
        labels: list,
        c: int,
        other: tuple = None):
    if visual_interface:
        screen.fill("white")
        for i in range(MAX_LENGTH):
            pygame.draw.rect(
                screen,
                "black",
                pygame.Rect(
                    i * square_size,
                    0,
                    square_size,
                    square_size),
                1)
            # Create a label for the square
            label = font.render(f"r{i+1}", 1, ARROW_COLOR)
            label_width = label.get_width()  # Get the width of the label
            label_height = label.get_height()  # Get the height of the label
            screen.blit(
                label,
                (i *
                 square_size +
                 square_size /
                 2 -
                 label_width /
                 2,
                 square_size))  # Draw the label on the screen

        # Add the numbers in register to each of the squares
        for i in range(MAX_LENGTH):
            label = font.render(str(register[i]), 1, ARROW_COLOR)
            label_width = label.get_width()
            label_height = label.get_height()
            screen.blit(
                label,
                (i *
                 square_size +
                 square_size /
                 2 -
                 label_width /
                 2,
                 square_size /
                 2 -
                 label_height /
                 2))

    if other:
        if other[0] == 'ARROW':
            pointer = other[1]
            draw_arrow(pointer, square_size, label_height, screen)

        elif other[0] == 'TRANSFER':
            pointer1, pointer2 = other[1]
            arrow_shaft_start_2, arrow_shaft_end_2 = draw_arrow(
                pointer2, square_size, label_height, screen)

            arrow_shaft_start_1 = (
                pointer1 * square_size + square_size / 2,
                1.5 * square_size + label_height)
            arrow_shaft_end_1 = (
                pointer1 * square_size + square_size / 2,
                square_size + label_height)

            # Draw the arrow shaft 1
            pygame.draw.line(
                screen,
                ARROW_COLOR,
                arrow_shaft_start_1,
                arrow_shaft_end_1,
                3)

            # Connect the two arrows shafts
            pygame.draw.line(
                screen,
                ARROW_COLOR,
                arrow_shaft_start_1,
                arrow_shaft_start_2,
                3)

        elif other[0] == 'JUMP':
            pointer1, pointer2 = other[1]
            arrow_shaft_start_1, arrow_shaft_end_1 = draw_arrow(
                pointer1, square_size, label_height, screen)
            arrow_shaft_start_2, arrow_shaft_end_2 = draw_arrow(
                pointer2, square_size, label_height, screen)

            # Connect the two arrows shafts
            pygame.draw.line(
                screen,
                ARROW_COLOR,
                arrow_shaft_start_1,
                arrow_shaft_start_2,
                3)

    # Draw bold horizontal arrow that points to the current instruction
    y_center = draw_bold_horizontal_arrow(
        screen, SCREENWIDTH, SCREENHEIGHT, square_size)

    # Draw the labels, centered in the element c of the list
    draw_labels(
        screen,
        labels,
        square_size,
        SCREENWIDTH,
        SCREENHEIGHT,
        y_center,
        c)

    pygame.display.update()


def execute_program(
        cmds: list,
        parameters: list,
        visual_interface: bool,
        SCREENWIDTH: int,
        SCREENHEIGHT: int,
        screen,
        font) -> None:
    """Takes a list with the commands and a list with the parameters and executes the program."""
    register = [0 for _ in range(MAX_LENGTH)]
    for i in range(len(parameters)):
        register[i] = parameters[i]

    number_of_instructions = len(cmds)

    c = 0
    if visual_interface:
        square_size = SCREENWIDTH // MAX_LENGTH
        labels = instructions_to_labels(
            pygame.font.Font(None, square_size), cmds)
        refresh_screen(
            screen,
            square_size,
            visual_interface,
            font,
            SCREENWIDTH,
            SCREENHEIGHT,
            register,
            labels,
            c,
            other=None)

    while c < number_of_instructions:
        current_command, parameters = cmds[c]
        other = None
        if current_command == ZERO:
            if not 1 <= parameters[0] <= MAX_LENGTH:
                raise SyntaxError(
                    f"Error at instruction {c+1}. The register must be in the range [1, {MAX_LENGTH}].")
            register[parameters[0] - 1] = 0
            if visual_interface:
                other = ('ARROW', parameters[0] - 1)
        elif current_command == SUCCESSOR:
            if not 1 <= parameters[0] <= MAX_LENGTH:
                raise SyntaxError(
                    f"Error at instruction {c+1}. The register must be in the range [1, {MAX_LENGTH}].")
            register[parameters[0] - 1] += 1
            if visual_interface:
                other = ('ARROW', parameters[0] - 1)
        elif current_command == TRANSFER:
            if not 1 <= parameters[0] <= MAX_LENGTH or not 1 <= parameters[1] <= MAX_LENGTH:
                raise SyntaxError(
                    f"Error at instruction {c+1}. The registers must be in the range [1, {MAX_LENGTH}].")
            register[parameters[1] - 1] = register[parameters[0] - 1]
            if visual_interface:
                other = ('TRANSFER', [parameters[0] - 1, parameters[1] - 1])
        elif current_command == JUMP:
            if register[parameters[0] - 1] == register[parameters[1] - 1]:
                c = parameters[2] - 2
            if visual_interface:
                other = ('JUMP', [parameters[0] - 1, parameters[1] - 1])

        if visual_interface:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            refresh_screen(
                screen,
                square_size,
                visual_interface,
                font,
                SCREENWIDTH,
                SCREENHEIGHT,
                register,
                labels,
                c,
                other=other)
            pygame.display.update()

            time.sleep(DELAY)

        c += 1

    return register


def interpretate(*args) -> None:
    """Takes a string with the path to the script and interpretates it."""
    path = args[1]
    arguments = args[2:]

    try:
        with open(path, "r", encoding='utf-8') as script:
            file_code = script.read().lower().split("\n")

        cmds = file_to_commands(
            file_code)

    except OSError as e:
        print(f"Could not open {path}:\n{e}\n", file=sys.stderr)

    parameters_raw = input(
        "Enter the parameters of f separated by comas: ").replace(" ", "").split(',')
    for i in parameters_raw:
        if not i.isdigit():
            raise SyntaxError("Parameters must be numbers.")

    parameters = [int(i) for i in parameters_raw]

    if len(parameters) > MAX_LENGTH:
        raise SyntaxError(
            f"The register has a maximum length of {MAX_LENGTH}.")

    visual_interface = False
    SCREENWIDTH = 0
    SCREENHEIGHT = 0
    screen = None
    font = None

    if len(arguments):
        visual_interface = arguments[0] == "-v"

    if visual_interface:
        global pygame
        import pygame
        pygame.init()
        SCREENWIDTH = 50 * MAX_LENGTH
        SCREENHEIGHT = 40 * MAX_LENGTH
        screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        # None means the default font
        font = pygame.font.Font(None, int(MAX_LENGTH * 3 / 2))

    register = execute_program(cmds, parameters, visual_interface,
                               SCREENWIDTH,
                               SCREENHEIGHT,
                               screen,
                               font)

    if visual_interface:
        time.sleep(5)
        pygame.quit()

    print(f"f({str(parameters)[1:-1]})⭣ {register[0]}")


if __name__ == "__main__":
    interpretate(*sys.argv)
