#!/bin/bash

mkdir -p ../res/dpatt 2> /dev/null

## Double pattern guessing commands

./sim_guess_2patt.py -m 100000 -n 1  --b1 ../patts/bl/bl_first.txt -o ../res/dpatt/first.txt ../patts/dpatt/first.txt ../patts/dpatt/sim-all-rel-freq.txt 

./sim_guess_2patt.py -m 100000 -n 1 --b2 ../patts/bl/bl_both.txt -o ../res/dpatt/both.txt ../patts/dpatt/both.txt ../patts/dpatt/sim-all-rel-freq.txt 

./sim_guess_2patt.py -m 100000 -n 1  -o ../res/dpatt/control.txt ../patts/dpatt/control.txt ../patts/dpatt/sim-all-rel-freq.txt 

