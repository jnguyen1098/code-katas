#!/usr/bin/env sh

if [ $# -ne 1 ]; then
    echo "Usage: $0 pythonfile"
    exit 1
fi

set -e

THING="$1"

isort --diff "$THING"
mypy --strict --show-error-context --show-column-numbers --show-error-codes --ignore-missing-imports --pretty "$THING"
black --diff --check -l 100 "$THING"
flake8 --count --show-source --statistic --max-line-length 100 "$THING"
pycodestyle --max-line-length=89 --show-source --statistics --count --max-line-length=100 "$THING"
pylint "$THING"
pydocstyle -e -s --count "$THING"
echo "Success"
