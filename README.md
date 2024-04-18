# Installation
Note that because the tausworthe random number generator is a .so file the
program can currently only run on Linux systems - Windows is not supported
at the moment. The program can be installed 

```console
$ pip install ained
```

# ained Usage

**Usage**:

```console
$ ained [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `generate-numbers`: Generate a file with random numbers from 0...
* `gui`: Create a visual representation of the...
* `process-file`: Read in a json file (input_file) with...

## `ained generate-numbers`

Generate a file with random numbers from 0 to 100. Used for reproducible results.

**Usage**:

```console
$ ained generate-numbers [OPTIONS] COUNT FILEPATH
```

**Arguments**:

* `COUNT`: Number of random numbers to generate.  [required]
* `FILEPATH`: File to save the random numbers to.  [required]

**Options**:

* `--help`: Show this message and exit.

## `ained gui`

Create a visual representation of the dipole grid that you can interact with via a GUI.

**Usage**:

```console
$ ained gui [OPTIONS] ROWS COLUMNS
```

**Arguments**:

* `ROWS`: Number of rows of the dipole grid.  [required]
* `COLUMNS`: Number of columns of the dipole grid.  [required]

**Options**:

* `--probability FLOAT`: Strength of co-varying effect  [default: 0.7]
* `--help`: Show this message and exit.

## `ained process-file`

Read in a json file (input_file) with board properties and a series of writes. Perform each write operation
and propagate the results to neighboring bits. Save the entire history of writes and board states to (output_file)

**Usage**:

```console
$ ained process-file [OPTIONS] INPUT_FILE OUTPUT_FILE
```

**Arguments**:

* `INPUT_FILE`: File path to JSON file to process.  [required]
* `OUTPUT_FILE`: File path to save results to.  [required]

**Options**:

* `--help`: Show this message and exit.


## Fixed Point Arithmetic ##

Because this software is intended to be a functional model for simulating calculations
on an FPGA the goal was to avoid floating point arithmetic since DSPs are limited on
an FPGA. Thus the [fxpmath](https://github.com/francof2a/fxpmath)  library was used to
enforce 16-bit fixed point arithmetic. Specifically the following precision was used:

```
dtype = fxp-u16/16
Signed = False
Word bits = 16
Fract bits = 16
Int bits = 0
Val data type = <class 'float'>

Upper = 0.9999847412109375
Lower = 0.0
Precision = 1.52587890625e-05
Overflow = saturate
Rounding = trunc
Shifting = expand
```

To understand what this all means, please refer to the fxpmath library documentation.
To change the precision change this line
`DTYPE = "fxp-u16/16"` in the `fixedpoint_config.py` file.

# Running from Source Code
Because the source code is organized into a package structure, one cannot
simply call 

```console
python3 main.py gui 7 7
```
as this will result in relative import errors. Instead you must run the following
from the top level directory:

```console
python3 -m ained.main gui 7 7
```

The `-m` tells python to load `main` as a module inside the package `ained`
instead of loading it as a top-level script.

Similarly, you can run all the tests by doing the following:
```console
python3 -m pytest
```