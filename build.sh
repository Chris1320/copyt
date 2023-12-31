#!/usr/bin/env bash

./venv/bin/python -m nuitka \
    --no-deployment-flag=self-execution \
    --output-dir=./build-nuitka \
    ./copyt
