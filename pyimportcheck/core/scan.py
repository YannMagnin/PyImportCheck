"""
pyimportcheck.core.scan   - python package scanner
"""
__all__ = [
    'pycycle_scan_package',
]
from typing import Dict, List, Any
from pathlib import Path
import re

from pyimportcheck.core.exception import PycycleException
from pyimportcheck.core._logger import (
    log_warning,
    log_error,
)

#---
# Internals
#---

def _pic_validate_export(
    file_info: Any,
    stream: Any,
) -> None:
    """ analyse the __all__ declaration

    @notes
    - check __all__ declaration
    - check validity or missing symbols
    """
    symbols = re.search(
        "__all__ = \\[(\n)?(?P<raw>("
        "    ['\"][A-Za-z0-9_]+['\"](,)?(\n)?)*"
        ")\\]",
        stream,
    )
    symbols_raw: List[str] = []
    if symbols:
        symbols_raw = symbols['raw'].split()
    symbols_raw = [x.replace('\'', '') for x in symbols_raw]
    symbols_raw = [x for y in symbols_raw for x in y.split(',') if x]
    exported_symbol = []
    for x in symbols_raw:
        x.replace(',', '')
        x.replace('\'','')
        exported_symbol.append(x)
    file_symbols = file_info['symbols'].copy()
    for sym in exported_symbol:
        if (
                file_info['path'].name[0] == '_'
            and file_info['path'].name[1] != '_'
            and sym.startswith('_')
        ):
            log_warning(
                f"{file_info['path']}: avoid exposing private "
                f"symbol '{sym}'"
            )
        if sym in file_symbols:
            file_symbols.pop(sym)
            continue
        if sym in file_info['symbols']:
            log_warning(
                f"{file_info['path']}: multiple exposition of the "
                f"symbol '{sym}'"
            )
            continue
        log_error(f"{file_info['path']}: unable to find the symbol '{sym}'")
    if file_symbols:
        workaround = '\n  - '.join([x for x in file_symbols if x[0] != '_'])
        log_error(
            f"{file_info['path']}: missing some symbol to expose:\n"
            f"  - {workaround}"
        )

def _pic_check_symbols(
    info: Dict[str,Any],
    lineno: int,
    record: str,
) -> None:
    """ check and update symbols information

    @notes
    - check symbols definition (global and function)
    """
    symbols = []
    if func := re.match(r"^def (?P<symbol>([1-9a-zA-Z_]+))\(", record):
        symbols.append(func['symbol'])
    if assign := re.match("^(?P<var>([a-zA-Z0-9_]+( )?=( )?)+)", record):
        symbols += [x.replace(' ', '') for x in assign['var'].split('=')]
    if not symbols:
        return
    for sym in symbols:
        if not sym:
            continue
        if sym in info['symbols']:
            continue
        if sym == '__all__':
            continue
        info['symbols'][sym] = lineno

def _pic_check_import(
    info:    Dict[str,Any],
    lineno:  int,
    record:  str,
    package: str,
) -> None:
    """ check and update import information

    @notes
    - check `from <package> import ...`
    - check `import <package>`
    """
    import_info = re.match(
        rf'^from (?P<pypath>{package}((\.[a-z_]+)?)+)',
        record,
    )
    if not import_info:
        import_info = re.match(
            rf'^import (?P<pypath>{package}((\.[a-z_]+)?)+)$',
            record,
        )
        if import_info:
            log_warning(
                f"{info['path']}:{lineno}: avoid using raw `import`, "
                'prefer using `from ... import ...` instead'
            )
    if import_info:
        info['imports'].append((lineno, import_info['pypath']))

def _pycycle_analyse_file(
    file_info: Dict[str,Any],
    prefix: Path,
    package: str,
) -> None:
    """ load the file and manually parse import
    """
    file_info['imports'] = []
    file_info['symbols'] = {}
    with open(prefix, 'r', encoding='utf8') as pyfile:
        for i, line in enumerate(pyfile):
            _pic_check_import(file_info, i + 1, line, package)
            _pic_check_symbols(file_info, i + 1, line)
        pyfile.seek(0)
        _pic_validate_export(file_info, pyfile.read())

def _pycycle_scan_package(
    info: Dict[str,Any],
    prefix: Path,
    package: str,
) -> None:
    """ recursively scan package folders
    """
    for filepath in prefix.iterdir():
        if filepath.name in ['__pycache__', 'py.typed']:
            continue
        if filepath.name.startswith('.'):
            continue
        if filepath.is_dir():
            info[filepath.name] = {
                'type': 'module',
                'modules': {}
            }
            _pycycle_scan_package(
                info[filepath.name]['modules'],
                filepath,
                package,
            )
            continue
        if not filepath.name.endswith('.py'):
            log_warning(f"file '{str(filepath)}' is not a valid")
            continue
        info[filepath.stem] = {
            'type': 'file',
            'path': filepath,
        }
        _pycycle_analyse_file(
            info[filepath.stem],
            filepath,
            package,
        )

#---
# Public
#---

def pycycle_scan_package(prefix: Path) -> Dict[str,Any]:
    """ package scanner
    """
    if not (prefix/'__init__.py').exists():
        raise PycycleException(
            'The provided package prefix do not have __init__.py file'
        )
    info: Dict[str,Any] = {
        'prefix':   prefix,
        'package':  prefix.name,
        'type':     'module',
        'modules':  {},
    }
    _pycycle_scan_package(info['modules'], prefix, prefix.name)
    return info
