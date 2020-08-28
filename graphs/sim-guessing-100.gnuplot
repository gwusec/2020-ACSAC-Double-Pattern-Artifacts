#!/usr/bin/env gnuplot

set style fill transparent solid 0.2 noborder

set output "sim-guessing-100.pdf"
set term pdf color rounded dl 1
#set style line linespoints


set key at 65,.195 box opaque

set xrange [0:100]
set yrange [0:.20]
set xlabel "Number of Guesses"
set ylabel "Fraction Guessed"

set xtics 10

set arrow from 10,0 to 10,.2 nohead back ls 5 lw 1.4 dt "."
set arrow from 30,0 to 30,.2 nohead back ls 5 lw 1.4 dt "."
set label "10 guesses" at 10.5,0.1 font "Helvitica,10"
set label "30 guesses" at 18.5,0.11 font "Helvitica,10"


set label "6-Digit PINs" at 80,0.115 font "Helvitica,10"
set label "4-Digit PINs" at 82,0.165 font "Helvitica,10"
set label "3x3 Patterns" at 15,0.16 font "Helvitica,10"
set label "BL-first/-both DPatt" at 60,0.01 font "Helvitica,10"
set label "Control DPatt" at 40,0.065 font "Helvitica,10"




plot "../res/dpatt/control.txt" w lp lw 2 lt 8 dt 1 pt 5 ps 0.5 pi 5 t "Control DPatt", \
     "../res/dpatt/first.txt" w lp lw 2 lt 4 dt 4 pt 6 ps 0.5 pi 5 t "BL-first DPatt", \
     "../res/dpatt/both.txt" w lp lw 2 lt 3 dt 3 pt 8 ps 0.5 pi 5 t "BL-both DPatt", \
     "../res/pat/3x3-pat.txt" w lp lw 2 lt 6 dt 5 pt 2 ps 0.5 pi 5 t "3x3 Patterns", \
     "../res/pin/pin-4.txt" w lp lw 2 lt 7 dt 4 pt 3 ps 0.5 pi 5 t "4-Digit PINs", \
     "../res/pin/pin-6.txt" w lp lw 2 lt 1 dt 3 pt 4 ps 0.5 pi 5 t "6-Digit PINs"\


