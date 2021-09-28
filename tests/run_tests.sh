#!/bin/bash

DIR="${0%/*}"

echo "Generating test data..."
$DIR/test_data/generate_test_data.sh
echo "Running tests..."
pytest $DIR
