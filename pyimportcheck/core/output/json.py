"""
pyimportcheck.core.output.json  - JSON output
"""
__all__ = [
    'pic_output_json',
]
from pathlib import Path
import json

from pyimportcheck.core.detect import PicDetectReport

#---
# Public
#---

def pic_output_json(
    pathname:   Path,
    report:     PicDetectReport,
) -> int:
    """ export the report in a JSON file
    """
    if pathname.exists():
        pathname.unlink()
    with open(pathname, 'w', encoding = 'utf8') as outfd:
        json.dump(report.export_json(), outfd)
    return report.error + report.warning
