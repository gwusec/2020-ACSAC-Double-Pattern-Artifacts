#!/bin/bash

# Generate PIN results

mkdir -p ../res/pin 2> /dev/null

./sim_guess_pin.py -n 1  -m 100000 -o ../res/pin/pin-6.txt ../patts/pin/allfirstentry.6digit.txt ../patts/pin/6-rockyou.txt
./sim_guess_pin.py -n 1  -m 100000 -o ../res/pin/pin-4.txt ../patts/pin/allfirstentry.4digit.txt ../patts/pin/amitay.4digit-withcount.txt  

