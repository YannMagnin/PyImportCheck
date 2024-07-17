"""
pyimportcheck.core.stdout   - display the report in stdout
"""
__all__ = [
    'pic_output_stdout',
]

from pyimportcheck.core.detect import PicDetectReport

#---
# Public
#---

def pic_output_stdout(report: PicDetectReport) -> int:
    """ display the report in stdout and return the exit status
    """
    #if error['total'] > 0:
    #    log_info('==========================')
    #for desc, total in error.items():
    #    if desc == 'total':
    #        continue
    #    if total > 0:
    #        log_info(f"Detected {total} {desc} error")
    #return error['total']
    print(report)
    return 0
