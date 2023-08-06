# A common configuration-storage class with a .diag() method

## Description

This module provides four classes that may be used as base classes for
storing program runtime configuration with a `verbose` boolean field.
The classes provide a `.diag(func)` method that will check the object's
`verbose` field and, if it is set to a true value, invoke the specified
function and output the message that it returns. If the message is not
expensive to format (e.g. it does not include stringifying elaborate
data structures), the `.diag_(msg)` method may be used instead.

The `ConfigUnfrozen` and `ConfigUnfrozenStdOut` classes are
normal dataclasses, while the `Config` and `ConfigStdOut` ones
are frozen.

The `Config` and `ConfigUnfrozen` classes will output any
diagnostic messages to the standard error stream, while
the `ConfigStdOut` and `ConfigUnfrozenStdOut` ones will output
the diagnostic messages to the standard output stream.

For compatibility with `cfg-diag` versions 0.1.x and 0.2.x, there is
also a parallel `ConfigDiag*` class hierarchy; the classes there are
organized in exactly the same way as those in the `Config*` hierarchy,
but they only provide a single `.diag(msg)` method that accepts
a fixed, already-built, string instead of a callback function.
These classes are deprecated and will most probably be removed in
a future version of the `cfg-diag` library.

## Example

Subclass the frozen `Config` class, add a program-specific field:

    @dataclasses.dataclass(frozen=True)
    class Config(cfg_diag.Config):
        """Runtime configuration for the fribble program."""
        path: pathlib.Path

Initialize this class from an argument parser object:

    return Config(path=args.path, verbose=args.verbose)

Output a diagnostic message if requested:

    cfg.diag_("This will either appear or it will not")
    cfg.diag(lambda: f"Here's the thing: {thing!r}")

## Contact

This module is [developed in a GitHub repository][github].
Contact [the StorPool support team][support] for information.

[github]: https://github.com/storpool/python-cfg_diag
[support]: mailto:support@storpool.com
