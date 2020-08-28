# Guessing Scripts

## Simulated Guesser

Provided are a series of bash script that will run with the correct arguments to populate the results `../res` directory.

* `run_1patt.sh` : run all the first and second component guessing
   * results placed in `../res/fcomp` and `../res/scomp`
* `run_2patt.sh` : run all the dpatt guessing
   * results placed in `../res/dpatt`
* `run_pin.sh` : run all the pin guessing
   * results placed in `../res/pin`
* `run_cross_fold.sh` : run a cross fold validation on 3x3 patterns 
   * results placed in `../res/pat`


Individual scripts (all have `-h` option for argument listing)

* `sim_guess_1patt.py` : first or second component pattern guessers
* `sim_guess_2patt.py` : double pattern guesser
* `sim_guess_pin.py` : pin guesser
* `sim_cross_fold.py` : a cross fold validation guesser for 3x3 patterns

## Perfect Knowledge Guesser

Provide is a bash script that will output a latex tabular of the perfect knowledge guessing results

* `run_perfect_knowledge.sh`

This script runs `perfect_guess.py` that calculates the perfect knowledge statistics with a randomized downsample to 207 samples. Note due to randomizations the 100th place in the decimal may vary. 
