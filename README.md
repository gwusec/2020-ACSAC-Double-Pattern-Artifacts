# 2020 ACSAC Artifact Submission

**Double Patterns: A Usable Solution to Increase the Security of Android Unlock Patterns**. Timothy J. Forman and Adam J. Aviv

## Included Artifacts and Description

Provided in this git repo is the selected Double Patterns and related data needed to generate the simulated and perfect-knowledge guessing results. This includes Table 5, and Figure 4-7. Additional descriptions of this data is provided in the data directory [README.md](patts/README.md) file. 

## Extracting Data

To start you must unzip all the data files

```
cd patts
find . -name "*.gz" | xargs gunzip -k
```

## Generating Table 5

Proceed to the `scripts` directory and execute the perfect knowledge bash script

```
cd scripts
./run_perfect_knowledge.sh
```

The output will be a latex tabular that you can render to view the perfect knowledge guesser

## Generating Figures 4-7

Proceed to the `scripts` directory and run the simultad guessing scripts

```
cd scripts
./run_1patt.sh
./run_2patt.sh
./run_cross_fold.sh
./run_pin.sh
```

This will place the results in the `res` directory.  Then proceed to the `graphs` directory and execute

```
cd graphs
find . -name "*.gnuplot" -exec gnuplot {} \;
```

This will produce four graphs, as pdf files, that correspond to Figure 4-7.

## Requirements

* python2 (version >= 2.7)
* python3 (version >= 3.6)
* gnuplot (version >= 5.0)

