for i in `find . -name rey_*  | sort -n`
do
    echo $i
    cd $i
    for aoa in {-10..25}
    do
        cd aoa_$aoa.0
        echo $aoa.0
        timeout 5s pvpython ../../../../../utilities/extract_cp_cf.py $aoa.0
        cd -
    done
    cd /lustre/eaglefs/scratch/gvijayak/CurrentProjects/RAAW/OpenSourceAirfoils/nalu_runs
done
