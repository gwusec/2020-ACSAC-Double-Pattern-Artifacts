# Graphs

To generate the graphs, you must first populate the `res` directory. Then

```
find . -name "*.gnuplot" -exec gnuplot {} \;
```

This will produce the following graphs in used in the paper:

* Figure 4: `sim-guessing-100.pdf`
* Figure 5: `sim-guessing-100000.pdf`
* Figure 6: `sim-guessing-100-fcomp.pdf`
* Figure 7: `sim-guessing-100-scomp.pdf`
