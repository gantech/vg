How to submit job arrays

This will submit 1 job for each in the `listOfCases` file

```
find ../ -name aoa_* | sort -n > listOfCases
sbatch airfoil_vg.slurm
```




