# tox-delay - run some Tox tests after others have completed

The `tox-delay` tool postpones the run of the specified Tox environments
after the run of all the others has completed successfully. This may be
useful if e.g. there are unit or functional test environments, which
it would make no sense to run if the static checkers (pylint, mypy, etc)
find problems.

## Using tox-delay

The mandatory `-e envlist` parameter to `tox-delay` specifies
the comma-separated list of environment names to delay. The tool runs Tox,
instructing it to skip these specific environments, and if the run is
successful, `tox-delay` then runs Tox again only for the specified ones.

For example, if a `tox.ini` file declares the `black`, `pep8`, `mypy`,
`pylint`, `unit-tests`, and `functional` environments, the following
invocation:

    tox-delay -e unit-tests,functional

...would result in Tox running the `black`, `pep8`, `mypy`, and `pylint`
environments and, if this is successful, a second Tox run for `unit-tests`
and `functional`.

Any positional arguments to `tox-delay` are passed along to Tox for both
runs. This allows both specifying more Tox options (`--workdir`,
`--skip-missing-interpreters`, etc) and specifying more positional
arguments to be expanded using the `{posargs}` setting in `tox.ini`.
Thus, the `-k all` arguments in the following invocation will be used as
`{posargs}`, maybe for `pytest` or something similar:

    tox-delay -e unit-tests,functional -- --workdir /tmp/tox -- -k all

The `-p` command-line option, along with its argument, is passed on to Tox
only for the first run. Thus, the following invocation would run
the `black`, `pep8`, `mypy`, and `pylint` environments in parallel and
then run the `unit-tests` and `functional` ones sequentially:

    tox-delay -p all -e unit-tests,functional

If the second run should also be done in parallel, this may be achieved by
passing `-p all` once again, but this time in the "general Tox options"
section as described above:

    tox-delay -p all -e unit-tests,functional -- -p all

## Querying the command-line tool for supported features

All the `tox-delay` implementations support the `--features` command-line
option to output a single line of text in a format that can be parsed
using [the `feature-check` tool][feature-check].

### Program version (tox-delay)

The version advertised for this feature is the `tox-delay` program's
version number, the same as in the `--version` output.

### Ignore some Tox environments (ignore)

The only version advertised so far is `1.0`: support the `-i envlist`
(or, if the `longopts` feature is at version `1.0` or above, also
`--ignore envlist`) command-line option to specify a comma-separated
list of environment name substrings. Any Tox environments with names
that match the values on this list will not be invoked at any stage.

### Long options support (longopts)

- `0.1`: limited support for long command-line options, only
  `--help`, `--version`, and `--features` are recognized
- `1.0`: other long options are also recognized, depending on
  the version of the `tox-delay` tool (reported via the `tox-delay`
  feature's version):
  - `0.1.2` or higher: `--ignore envlist`, `--parallel envlist`

### Run first-stage test environments in parallel (parallel)

The only version advertised so far is `1.0`: support the `-p envlist`
(or, if the `longopts` feature is at version `1.0` or above, also
`--parallel envlist`) command-line option to specify a comma-separated
list of environment name substrings or the special value "all".
This option will be passed to Tox in the first stage, so that some
(or all) of the validation checks (in the standard use case of `tox-delay`)
will be run in parallel.

## Contact

For comments and suggestions, please contact [Peter Pentchev][roam].

[feature-check]: https://devel.ringlet.net/misc/feature-check/ (Query a program for supported features)
[roam]: mailto:roam@ringlet.net (Peter Pentchev)
