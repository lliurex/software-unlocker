#!/bin/bash

PYTHON_FILES="../src/*.py ../src/stacks/*.py"

mkdir -p software-unlocker/

xgettext $PYTHON_FILES -o software-unlocker/software-unlocker.pot

echo '' >> software-unlocker/software-unlocker.pot
