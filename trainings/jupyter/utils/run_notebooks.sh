  #!/usr/bin/env bash
cd /app/notebooks

jupyter nbconvert \
    --to notebook \
    --execute \
    --inplace \
    --ExecutePreprocessor.timeout=-1 \
    --allow-errors \
    /app/notebooks/*.ipynb