#!/bin/bash

pip install pdoc3
pdoc3 -o docs --html --force hocort
mv docs/hocort/* docs/; rm -rf docs/hocort
