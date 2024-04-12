"""
pyimportcheck.core.logger - PycycleLogger object abstraction
"""
__all__ = [
    'log_error',
    'log_warning',
]
import sys

#---
# Public
#---

def log_error(text: str, end: str ='\n') -> None:
    """ display error """
    print(f"\033[31m[ERROR] {text}\033[0m", end=end, file=sys.stderr)

def log_warning(text: str, end: str ='\n') -> None:
    """ display warning """
    print(f"\033[32m[WARNING] {text}\033[0m", end=end)
