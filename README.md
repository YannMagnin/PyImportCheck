# PyCircularImport - detect python circular import

> [!WARNING]
> This project is very limited and designed for my personal use to quickly
> detect circular import errors in some "big" project.
> You probably want to use [CodeQL](https://github.com/github/codeql) with
> [default python query](https://github.com/github/codeql/blob/main/python/ql/src/Imports/CyclicImport.ql)
> that performs exactly the same job, probably better, rather than using my
> tool.

This project aims to provide quick detection of circular imports in python
packages. This is achieved by opening each python file of the package,
analysing all `from <package> ... import ...` and `import <package> ...` lines
and manually trying to resolve all imports. If a circular import is detected,
the import flow will be displayed with module and line information.

Here is an example of an hypothetical `test` project:
```txt
> pycycle -p ../../poc/python_import/test/
[ERROR] (test/a.py) test.a:12 -> test:12 -> test.a:10
[ERROR] (test/__init__.py) test.__init__:10 -> test.a:10 -> test:12
[ERROR] Detected 2 cyclic import
```
So, with this example, we can see that we have a circular dependency in the
file `test/a.py` line `12` and `test/__init__.py` line `10`.

> [!TIP]
> I recommend you to resolve each circular dependency in the order that they
> are displayed. This is because I do not detect if a circular import has
> already been detected. So, resolving one circular import can clear, at
> least, two errors (or more if you have a long loop)

> [!CAUTION]
> This project only supports `from <package> ... import ...` and
> `import <package> ...`. Local import (like `from .<module> ... import ...`)
> and special workarounds, like with `typing.TYPE_CHEKING`, are not supported
> (ignored for now).

## Install

Install and update using [pip](https://pip.pypa.io/en/stable/getting-started/):
```bash
pip install pycircularimport
```

Or you can install manually using [poetry](https://python-poetry.org/docs/):
```bash
# create virtual env (optional)
# poetry shell

# install the project
poetry install

# check installation
pycircularimport --version
```

## How to use

You can use the `--help` flag to display information, but (for now) only one
argument is required : `(-p|--prefix) <package path>` which is the path of the
package sources
```bash
crupycircularimport -p /path/to/local/package
```
