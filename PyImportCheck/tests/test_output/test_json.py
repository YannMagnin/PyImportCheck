"""
tests.test_output.test_json - test json output
"""
from typing import Dict, Any
from pathlib import Path
import json

from pyimportcheck.core.scan import pic_scan_package
from pyimportcheck.core.detect import pic_detect_all
from pyimportcheck.core.output import pic_output_json

#---
# Internals
#---

_PREFIX_PKG = Path(f"{__file__}/../../_data/fakepkg").resolve()
_JSON_OUT: Dict[str,Any] = {
    'version': 1,
    'total': {
        'all': 4,
        'error': 3,
        'warning': 1,
    },
    'notifications': [
        {
            'type': 'error',
            'path': 'fakepkg/test/__init__.py',
            'log': \
                '(fakepkg/test/__init__.py) '
                'fakepkg.test.__init__:8 -> fakepkg.a:17 -> '
                'fakepkg.__init__:10 -> fakepkg.a:17 -> ...',
        },
        {
            'type': 'error',
            'path': 'fakepkg/a.py',
            'log': \
                '(fakepkg/a.py) '
                'fakepkg.a:17 -> fakepkg.__init__:10 -> fakepkg.a:17 -> '
                '...',
        },
        {
            'type': 'error',
            'path': 'fakepkg/__init__.py',
            'log': \
                '(fakepkg/__init__.py) '
                'fakepkg.__init__:10 -> fakepkg.a:17 -> '
                'fakepkg.__init__:10 -> fakepkg.a:17 -> ...',
        },
        {
            'type': 'warning',
            'path': 'fakepkg/b.py',
            'log': \
                'fakepkg/b.py: missing the `__all__` symbol, which can be '
                'declared as follows:\n'
                '>>> __all__ = [\n'
                '>>>     \'b_test1\',\n'
                '>>>     \'b_test2\',\n'
                '>>> ]',
        },
    ],
}

#---
# Public
#---

def test_json_output() -> None:
    """ check json output
    """
    fakefile = Path('./fakeoutput.json')
    scaninfo = pic_scan_package(_PREFIX_PKG)
    detectinfo = pic_detect_all(scaninfo)
    total = pic_output_json(fakefile, detectinfo)
    assert fakefile.exists()
    with open(fakefile, 'r', encoding='utf-8') as testfd:
        export = json.load(testfd)
    fakefile.unlink()
    assert total == _JSON_OUT['total']['all']
    for info in _JSON_OUT['notifications']:
        print(f"looking for ==> {info}")
        assert info in export['notifications']
        export['notifications'].remove(info)
    assert len(export['notifications']) == 0
