#!/usr/bin/env bash
cd /app/notebooks
# Convert all Jupyter notebooks in the current directory to markdown files
# and save them in the /app/markdown directory
jupyter nbconvert --to markdown /app/notebooks/*.ipynb --output-dir=/app/markdown