"""
pycycle  - Crupy DSL parser
"""
from pyimportcheck.cli import pyimportcheck_cli_entry

#---
# Public
#---

# since click will automatically inject missing parameters, allow pylint
# to skip prototype analysis
# pylint: disable=locally-disabled,E1120
pyimportcheck_cli_entry()
