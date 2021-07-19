#!/bin/bash

find . -mindepth 2 -maxdepth 3 -name "*.csv" -print -exec python3 visualizer/viz.py {} \;
find . -mindepth 2 -maxdepth 3 -name "*.gr"  -print -exec python3 visualizer/viz.py {} \;
