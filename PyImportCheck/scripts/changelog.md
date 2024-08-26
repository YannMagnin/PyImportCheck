# v0.1.4

First beta release of the `PyImportCheck` project which provides elementary scanners and detectors. Please note that there is still some work to do to remove some limitation (like circular dependency detected multiple times), see the [roadmap issue](https://github.com/YannMagnin/PyImportCheck/issues/1) for more information !

## Features

- support circular import detection
- support missing `__init__.py` file in submodule
- support missing or partial magical `__all__` declaration
- support single file or full package analysis

## Fixes

- fix release pipeline
- fix PyPI deployment
- remove readme version information
- ensure versioning information

---
