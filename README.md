# `Awesome-cli`

**Usage**:

```console
$ Awesome-cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `generate-numbers`: Generate a file with random numbers from 0...
* `gui`: Create a visual representation of the...
* `process-file`: Read in a json file (input) with a board...

## `Awesome-cli generate-numbers`

Generate a file with random numbers from 0 to 100. Used for reproducible results.

**Usage**:

```console
$ Awesome-cli generate-numbers [OPTIONS] COUNT FILEPATH
```

**Arguments**:

* `COUNT`: Number of random numbers to generate.  [required]
* `FILEPATH`: File to save the random numbers to.  [required]

**Options**:

* `--help`: Show this message and exit.

## `Awesome-cli gui`

Create a visual representation of the dipole grid that you can interact with via a GUI.

**Usage**:

```console
$ Awesome-cli gui [OPTIONS] ROWS COLUMNS
```

**Arguments**:

* `ROWS`: Number of rows of the dipole grid.  [required]
* `COLUMNS`: Number of columns of the dipole grid.  [required]

**Options**:

* `--probability FLOAT`: Strength of co-varying effect  [default: 0.7]
* `--seed INTEGER`: Seed to use for random numbers  [default: 123456]
* `--help`: Show this message and exit.

## `Awesome-cli process-file`

Read in a json file (input) with a board properties and a series of writes. Save results to output.

**Usage**:

```console
$ Awesome-cli process-file [OPTIONS] INPUT_FILE OUTPUT_FILE RANDOM_FILE
```

**Arguments**:

* `INPUT_FILE`: File path to JSON file to process.  [required]
* `OUTPUT_FILE`: File path to save results to.  [required]
* `RANDOM_FILE`: File with random numbers to use for file processing. Note that such a file can be generated using the generatenumbes command  [required]

**Options**:

* `--help`: Show this message and exit.
