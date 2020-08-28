#!/bin/bash

mkdir -p ../res/fcomp 2> /dev/null
mkdir -p ../res/scomp 2> /dev/null

# Single pattern guessing commands

# first component pattern guessing
./sim_guess_1patt.py -1 -n 1 --b1 ../patts/bl/bl_first.txt -o ../res/fcomp/first.txt  ../patts/fcomp/first-0.txt ../patts/pat/all_related_freq.txt
./sim_guess_1patt.py -1 -n 1 --b2 ../patts/bl/bl_both.txt -o ../res/fcomp/both.txt  ../patts/fcomp/both-0.txt ../patts/pat/all_related_freq.txt
./sim_guess_1patt.py -1 -n 1 -o ../res/fcomp/control.txt  ../patts/fcomp/control-0.txt ../patts/pat/all_related_freq.txt

# second component pattern guessing
./sim_guess_1patt.py -2 -n 1 --b1 ../patts/bl/bl_first.txt -o ../res/scomp/first.txt  ../patts/scomp/first-1.txt ../patts/pat/all_related_freq.txt
./sim_guess_1patt.py -2 -n 1 --b2 ../patts/bl/bl_both.txt -o ../res/scomp/both.txt  ../patts/scomp/both-1.txt ../patts/pat/all_related_freq.txt
./sim_guess_1patt.py -2 -n 1 -o ../res/scomp/control-1.txt  ../patts/scomp/control-1.txt ../patts/pat/all_related_freq.txt


