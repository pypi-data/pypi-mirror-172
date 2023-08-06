# Recommended workflow for hacking on cfg-diag

## Source code formatting

The `cfg-diag` source is formatted automatically using the `black` tool.
Run `tox -e black-reformat` or `nox -s black-reformat -- do reformat` to
reformat the Python source files. Run `tox -e black` or `nox -s black` to
verify that the source files are formatted correctly.

The Nix expressions in the `nix/` subdirectory are formatted automatically
using the `nixpkgs-fmt` tool. Run `nix/reformat.sh` to invoke it.

## Coding style, type safety, etc

The `cfg-diag` source should pass static checks via the `flake8` and `pylint`
tools and type checks via the `mypy` tool.
Run `tox -p all -e pep8,pylint,mypy` or `nox -s pep8 pylint mypy` to run
the static checkers.

## Unit tests

The `cfg-diag` library has a set of trivial unit tests to ensure that
the `.diag()` and `.diag_()` methods of all the classes behave as
expected. Run `tox -e unit_tests` or `nox -s unit_tests` to run the tests.

## Doing it all in one step

All the tests defined in the `tox.ini` file can be run using
[the tox-delay tool][tox-delay]: `tox-delay -p all -e unit_tests`

All the tests defined in the `noxfile.py` file can be run using
[the nox-stages tool][nox-stages]: `nox-stages run '@check' '@tests'`

[tox-delay]: https://devel.ringlet.net/devel/tox-delay/ (Run some Tox tests after others have completed)
[nox-stages]: https://gitlab.com/ppentchev/nox-dump (Run Nox sessions in parallel, in stages)
