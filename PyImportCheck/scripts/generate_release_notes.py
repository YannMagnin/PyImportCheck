"""
generate_release_notes  - generate release note for a particular version

@notes
This script (and all of the release notes mechanism) is grandly inspired
from `pytest` (pytest-dev/pytest/scripts/generate-gh-release-notes.py).

But, instead of using RST format and `pandoc`, I use raw markdown parsing with
small rules to reparate version information:

    1. each version information must be surround by a line separator "---"
    2. each version information must have a title "# <version>"
    3. each "section" of the body should start as a subtitle "## ..."
"""
from typing import NoReturn
from pathlib import Path
import sys

#---
# Internals
#---

_CHANGELOG_FILE = (Path(__file__)/'../changelog.md').resolve()

def _log_error(text: str, status_code: int) -> NoReturn:
    """ display error in stderr and exit
    """
    print(text, file=sys.stderr)
    sys.exit(status_code)

def _generate_output_file(pathname: Path, body: str) -> int:
    """ try to generate the output
    """
    if pathname.exists():
        pathname.unlink()
    with open(pathname, 'w', encoding='utf-8') as outfd:
        outfd.write(body)
    return 0

def _find_release_content(version: str) -> str:
    """ try to find release content
    """
    if not _CHANGELOG_FILE.exists():
        _log_error(
            f"unable to find the changelog file at '{_CHANGELOG_FILE}'",
            2,
        )
    with open(_CHANGELOG_FILE, 'r', encoding='utf-8') as changelogfd:
        full_changelog = changelogfd.read()
    for shard in full_changelog.split('---'):
        for i, line in enumerate(shard.split('\n')):
            if not line.startswith('# '):
                continue
            if line[2:] != version:
                continue
            return '\n'.join(shard.split('\n')[i+1:]).strip()
    _log_error(f"unable to find release notes for version '{version}'", 3)

#---
# Public
#---

if __name__ == "__main__":
    if len(sys.argv) != 3:
        _log_error("Usage: {Path(__file__).name} VERSION FILE", 1)
    sys.exit(
        _generate_output_file(
            pathname    = Path(sys.argv[2]),
            body        = _find_release_content(sys.argv[1]),
        ),
    )
