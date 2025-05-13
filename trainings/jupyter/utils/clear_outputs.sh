#!/usr/bin/env bash
cd /app/notebooks

jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace --clear-output /app/notebooks/*.ipynb