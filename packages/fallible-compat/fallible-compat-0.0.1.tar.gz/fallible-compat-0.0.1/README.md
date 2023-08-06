# fallible-compat

This package is effectively a meta package that provides `ansible*` compatibility entrypoints (CLI commands) for `fallible`.

The goal is to provide an easy compat layer for tooling that expects the ansible CLI utilities to be present for it's functionality, to allow easily testing `fallible` in those environments.

This package can be installed explicitly via:

```shell
$ pip install fallible-compat
```

or as an `extras` for the `fallible` package via:

```shell
$ pip install fallible[compat]
```
