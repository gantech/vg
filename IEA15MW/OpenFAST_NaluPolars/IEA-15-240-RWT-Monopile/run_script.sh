mkdir output_files
for n in {4..24};
do
    prepref="input_files/"
    pref="IEA-15-240-RWT_"
    suff="mps.fst"
    suff_out="mps.out"
    path="$prepref$pref$n$suff"
    fin="$pref$n$suff"
    fout="$pref$n$suff_out"
    cp $path .
    ~/openfast/spack-build-7k5k5lt/bin/openfast $fin
    mv $fout output_files/
    echo "$n m/s complete"
done
    
