# Included Data

## Notes
Note that all data files are gzipped. To uncompress all at once

```
find . -name "*.gz" | xargs gunzip -k 
```

Uncompressed, there is 81M worth of data.

## List of Data Files

* `bl`: contains the blocklist used in the BL-first and BL-both treatment
   * `bl_both.txt`: blocklist for the BL-both treatment
   * `bl_first.txt`: blocklist for the BL-first treatment
   
* `dpatt`: contains the double patterns
  * `control.txt`: control treatment
  * `first.txt`: BL-first treatment
  * `both.txt`: BL-both treatment
  * `sim-all-rel-freq.txt`: Simulated frequency list of double patterns generated from the `pat/all_related.txt` data
  
* `fcomp`: first component pattern of double patterns
  * `control-0.txt`: control treatment first component pattern
  * `first-0.txt`: BL-first treatment first component pattern
  * `both-0.txt`: BL-both treatment first component pattern

* `scomp`: second component pattern of double patterns
  * `control-0.txt`: control treatment second component pattern
  * `first-0.txt`: BL-first treatment second component pattern
  * `both-0.txt`: BL-both treatment second component pattern

  
* `pat` : other relevant pattern files
  * `all_3x3-patterns.txt` : a list of all 389,112 patterns
  * `all_related.txt` : list of 4637 patterns collected from users in other research
  * `all_related_freq.txt` : a frequency list of the all_related.text
  
* `pin` : relevant PIN data
  * `6-rockyou.txt` : frequncy counts for the most common 6-digit PINs
  * `amitay.4digit-withcount.txt` : Amitay data set of 4-digit PINs
  * `allfirstentry.4digit.txt` : 4-digit PINs collected Markert et al.
  * `allfirstentry.6digit.txt` : 6-digit PINs collected Markert et al.


