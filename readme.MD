# Unilimited Register Machine Interpreter

A Python3 interpreter of the unlimited register machine, introduced by Nigel Cutland in Computability: an introduction to recursive function theory, 1980.  

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

To use the visual interface, run the following command:

```shell
python3 urminterpreter.py <urm_file.urm> -v
```

You may need to use python instead of python3 depending on your system.

## Examples

The examples folder contains some examples of URM programs. The following command runs the x_plus_1.urm program:

```shell
python3 urminterpreter.py examples/x_plus_1.urm
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)


## TODO

* Separate the interpreter from the visualizer
* Add a debugger