#!/bin/bash
# This is a bash script for running pytest tests

# navigate to the directory with the tests
cd ../data

# install pytest, if it's not installed yet
pip install pytest

# run the tests with pytest
python -m pytest
