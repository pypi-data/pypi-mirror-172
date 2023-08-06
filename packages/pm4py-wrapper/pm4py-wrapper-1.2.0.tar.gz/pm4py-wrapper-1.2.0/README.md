# pm4py-wrapper

![Build & Test](https://github.com/AutomatedProcessImprovement/pm4py-wrapper/actions/workflows/build_test.yml/badge.svg)

CLI wrapper for pm4py.

## Installation

Install using [pip](https://pip.pypa.io/en/stable/installation/):

```shell
pip install pm4py-wrapper
```

### Known Issues for macOS with M1

#### cvxopt@1.3.0: umfpack.h is missing

- Discussion is at https://github.com/cvxopt/cvxopt/issues/78.
- Solution:
  - Install `suite-sparse`
  - Specify `CPPFLAGS` and `LDFLAGS`
  - Run `pip install cvxopt`
- More details at http://cvxopt.org/install/index.html

```shell
$ brew info suite-sparse
$ export CPPFLAGS="-I/opt/homebrew/include/"
$ export LDFLAGS="-L/opt/homebrew/lib"
$ pip install cvxopt
```

#### scipy@1.6.1

- Discussion is at https://github.com/scipy/scipy/issues/13409
- Solution: use a newer version starting from 1.7.0

## Usage

```
Usage: pm4py_wrapper [OPTIONS] COMMAND [ARGS]...

Options:
  -i, --input_log PATH   Path to the input event log.  [required]
  -o, --output_dir PATH  Path to the output directory.
  --help                 Show this message and exit.

Commands:
  csv-to-xes
  xes-to-csv

```

Examples:

```shell
$ pm4py_wrapper -i tests/assets/input/Production.xes -o tests/assets/output xes-to-csv
$ pm4py_wrapper -i tests/assets/input/Production.csv -o tests/assets/output csv-to-xes
```

## Links

- A helpful [answer](https://stackoverflow.com/questions/57628064/automating-python-package-release-process#answer-57676367) on StackOverflow on how to do CI/CD with Poetry.
