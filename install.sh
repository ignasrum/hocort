#!/bin/bash

CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh

conda env create -f environment.yml
conda activate hocort && 
pip install "git+https://github.com/ignasrum/hocort.git"
