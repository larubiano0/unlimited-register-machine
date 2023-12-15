# Unilimited Register Machine Interpreter

A Python3 interpreter of the unlimited register machine, introduced by Nigel Cutland in Computability: an introduction to recursive function theory, 1980.  ISBN-10
0521294657.

An unlimited register machine is a theoretical model of computation that consists of an infinite number of registers, each one containing a natural number, by default all set to 0 at the beginning, except for the n first registers, which receive an input by the user. The machine can perform the following operations:

* Z(n): Set the value of the nth register to 0.
* S(n): Increment the value of the nth register by 1.
* T(n, m): Copy the value of the nth register to the mth register.
* J(n, m, l): If the values of the nth and mth registers are equal, jump to the lth instruction.

## Installation

Be shure to have Python3.10+ installed in your system. It can be found [here](https://www.python.org/downloads/).

(Optional) Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pygame to use the visual interface.

```bash
pip install pygame
```

## Usage

Download the zip file or clone the repository. Then cd to the folder where the files are located.

Run the interpreter with the following command:

```shell
python3 urminterpreter.py <urm_file.urm>
```

To use the visual interface (requires pygame), run the following command:

```shell
python3 urminterpreter.py <urm_file.urm> -v
```

You may need to use python instead of python3 depending on your system.

The file config.py contains some configuration variables that can be changed to modify the behaviour of the interpreter. The following variables can be changed: 

* **MAX_LENGTH**: The maximum length of the register machine (it also changes the size of the window if the visual interface is on). The default value is 16.

* **DELAY**: The delay between each instruction in the visual interface. The default value is 0.5 seconds.

* **ARROW_COLOR**: The color of the arrows and lines in the visual interface. Its default value is black, and can be changed to any color supported by pygame.

## Examples

The examples folder contains some examples of URM programs. The following command runs the x_plus_1.urm program:

```shell
python3 urminterpreter.py examples/x_plus_1.urm
```

The following command runs the x_plus_1.urm program with the visual interface:

```shell
python3 urminterpreter.py examples/x_plus_1.urm -v
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)


## TO DO:

* Separate the interpreter from the visualizer
* Add a debugger

## YouTube video:
[![YouTube video](https://img.youtube.com/vi/PLMU1lKPtMc/0.jpg)](https://www.youtube.com/watch?v=PLMU1lKPtMc)

<div align="center">
  <video src="example_video.mp4" width="400" />
</div>
