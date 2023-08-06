# Changelog for the tox-delay tool

## 0.1.3

- Python test suite:
  - adapt to the `Version` objects returned by `feature-check` 2.x
  - use `utf8-locale` 1.x with no changes

## 0.1.2

- New features for all implementations:
  - add the `-i` / `--ignore` command-line option to skip some Tox
    test environments altogether
  - advertise the degree to which long command-line options are
    supported in the `--features` list
- Python implementation:
  - reformat the source code using the non-beta version of black 22
  - drop support for Python 3.6
  - use deferred type annotations
  - use dataclasses instead of named tuples
  - drop the flake8 + hacking test environment
  - specify both lower and upper version constraints for the used
    Python libraries in the Tox test environment definitions
- Python test suite:
  - use `pytest.mark.parametrize()` instead of ddt and bump the minimal
    version of the pytest dependency to 7
  - move the mypy type cache to the Tox subdirectory

## 0.1.1

- Python test suite:
  - use the utf8-locale library's UTF8Detect builder class instead of
    the individual functions
  - set upper version limits for the feature-check and utf8-locale
    libraries in the tox.ini test environments

## 0.1.0

- First public release.

Comments: Peter Pentchev <roam@ringlet.net>
