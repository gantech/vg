#!/bin/bash

#SBATCH --nodes=1
#SBATCH --time=24:00:00
#SBATCH --array=1-108
#SBATCH --account=hfm
#SBATCH --job-name=airfoil_vg
#SBATCH --output=out.%x_%j

source ~/spack-manager/start.sh
spack-start
quick-activate ~/spack-nalu-wind-gcc

ranks_per_node=36
mpi_ranks=$(expr $SLURM_JOB_NUM_NODES \* $ranks_per_node)
export OMP_NUM_THREADS=1  # Max hardware threads = 4
export OMP_PLACES=threads
export OMP_PROC_BIND=spread

nalu_exec=/home/mkuhn/spack-nalu-wind-gcc/nalu-wind/spack-build-lbd635v/naluX

echo "Job name       = $SLURM_JOB_NAME"
echo "Num. nodes     = $SLURM_JOB_NUM_NODES"
echo "Num. MPI Ranks = $mpi_ranks"
echo "Num. threads   = $OMP_NUM_THREADS"
echo "Working dir    = $PWD"

echo "task_id        = ${SLURM_ARRAY_TASK_ID}"



case=$(sed -n "${SLURM_ARRAY_TASK_ID}p" listOfCases)
cd $case
echo "case path      = $case"
srun -n ${mpi_ranks} ${nalu_exec} -i *static_aoa*.yaml -o log.inpfile
