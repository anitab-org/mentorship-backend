#!/bin/bash

python -m unittest discover tests -v

# Some `duplicate-code` (R0801) must be fixed/removed, 
# but this check cannot be disabled directly in the codebase.
pylint --disable=R0801 ./*.py app tests
