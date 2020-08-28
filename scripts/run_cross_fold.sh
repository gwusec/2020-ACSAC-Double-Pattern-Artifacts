#!/bin/bash

# Do a cross fold validation of guessing 3x3 patterns

mkdir -p ../res/pat 2>/dev/null

./sim_cross_fold.py -f 5 -r 5  -g ../patts/pat/all_3x3-patterns.txt ../patts/pat/all_related.txt  > ../res/pat/3x3-pat.txt
