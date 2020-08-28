#!/usr/bin/env gnuplot

set style fill transparent solid 0.2 noborder

set output "sim-guessing-100-scomp.pdf"
set term pdf color rounded dl 1
#set style line linespoints


set key at 32,.74 box opaque

set xrange [0:100]
set yrange [0:.75]
set xlabel "Number of Guesses"
set ylabel "Fraction Guessed"

set xtics 10

set arrow from 10,0 to 10,.75 nohead back ls 5 lw 1.4 dt "."
set arrow from 30,0 to 30,.75 nohead back ls 5 lw 1.4 dt "."
set label "10 guesses" at 10.5,0.46 font "Helvitica,10"
set label "30 guesses" at 18.5,0.38 font "Helvitica,10"

plot "../res/dpatt/control.txt" w lp lw 2 lt 8 dt 1 pt 5 ps 0.5 pi 5 t "Control DPatt", \
     "../res/dpatt/first.txt" w lp lw 2 lt 4 dt 4 pt 6 ps 0.5 pi 5 t "BL-first DPatt", \
     "../res/dpatt/both.txt" w lp lw 2 lt 3 dt 3 pt 8 ps 0.5 pi 5 t "BL-both DPatt", \
     "../res/pat/3x3-pat.txt" w lp lw 2 lt 6 dt 5 pt 2 ps 0.5 pi 5 t "3x3 Patterns", \
     "../res/pin/pin-4.txt" w lp lw 2 lt 7 dt 4 pt 3 ps 0.5 pi 5 t "4-Digit PINs", \
     "../res/pin/pin-6.txt" w lp lw 2 lt 1 dt 3 pt 4 ps 0.5 pi 5 t "6-Digit PINs"\



