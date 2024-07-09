"""
pyimportcheck.core.scan._exports    - analyse the `__all__` declaration
"""
__all__ = [
    'pic_scan_exports',
]
from typing import Dict, Any
import re

from pyimportcheck.core._logger import log_warning

#---
# Public
#---

def pic_scan_exports(
    file_info: Dict[str,Any],
    stream: Any,
) -> None:
    """ analyse `__all__` declaration

    @notes
    - fetch all exposed symbols
    - notify warning if it use "(" instead of "]"
    """
    symbols = re.search(
        "__all__ = (?P<enclose>\\(|\\[)(\n)?(?P<raw>("
        "    ['\"][A-Za-z0-9_]+['\"](,)?(\n)?)*"
        ")(\\)|\\])",
        stream,
    )
    if not symbols:
        return
    lineno = stream[:symbols.start()].count('\n')
    if symbols['enclose'] == '(':
        log_warning(
            f"{file_info['path']}:{lineno}: the `__all__` declaration "
            'should use square brackets for declaration as implicitly '
            'described in the PEP-8'
        )
    symbols_raw = symbols['raw'].split()
    symbols_raw = [x.replace('\'', '') for x in symbols_raw]
    symbols_raw = [x for y in symbols_raw for x in y.split(',') if x]
    file_info['exported'] = []
    for x in symbols_raw:
        x.replace(',', '')
        x.replace('\'','')
        file_info['exported'].append(x)
