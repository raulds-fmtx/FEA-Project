# FEA_Project

## Description

An FEA Python Program for structural analysis of Euler-Bernoulli Beams. Each element has 4 degrees of freedom and uses a cubic approximation.

## Usage 

To use this program, execute the command `python -m FEA_Project input_file.txt output_file.txt` in an environment with an Anaconda3 enabled interpreter and in the outer `FEA_Project` directory.

`input_file.txt` MUST be formatted as follows:

[example.txt](./input/example.txt)

`output_file.txt` will contain formatted output of all data contained within `input_file.txt` and the nodal displacements solved for by the FEA program.

## Packages

This project uses the `numpy` and `copy` packages.

## Credits 

Created by Raul Santos

## License

Please refer to the LICENSE in the repo
