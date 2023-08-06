#!/bin/bash

rm -r .pytest_cache

black .

python -m pytest \
    --cov=blockutils \
    --durations=0
    #--mypy \
    #--mypy-ignore-missing-imports \
    #--pylint \
    #--pylint-rcfile=../../pylintrc \

