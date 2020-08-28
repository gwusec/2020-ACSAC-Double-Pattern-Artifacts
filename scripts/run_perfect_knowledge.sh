#!/bin/bash


echo "\\begin{tabular}{c | c | c c c | c | c c c}"
echo " & \$n\$ & \$\\beta_3$ & \$\\beta_{10}\$ & \$\\beta_{30}$ & \$H_\\infty\$ & \$\\widetilde{G}_{0.05}\$ & \$\\widetilde{G}_{0.10}\$ & \$\\widetilde{G}_{0.20}\$ \\\\ \\hline"

./perfect_guess.py ../patts/dpatt/control.txt Control
./perfect_guess.py ../patts/dpatt/first.txt BL-First
./perfect_guess.py ../patts/dpatt/both.txt BL-Both

echo "\hline"

./perfect_guess.py ../patts/pat/all_related.txt "3x3 Patterns"
./perfect_guess.py  ../patts/pin/allfirstentry.4digit.txt "4-digit PINs"
./perfect_guess.py  ../patts/pin/allfirstentry.6digit.txt "6-digit PINs"
echo "\hline"




echo "\end{tabular}"
