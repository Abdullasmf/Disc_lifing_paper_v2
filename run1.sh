#!/bin/bash
#SBATCH --job-name=GPU1(PN)
#SBATCH --output=Disc_lifing_paper/GPU1.log
#SBATCH --error=Disc_lifing_paper/GPU1.log
#SBATCH --time=90:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:1
#SBATCH --mem-per-cpu=8G
#SBATCH --cpus-per-task=1
echo "PN model training!"
echo "loading modules"

. /home/spack/share/spack/setup-env.sh
#spack load py-torch
spack load /j5cepfd
spack load anaconda3

source /usr1/software/miniconda3/etc/profile.d/conda.sh
conda activate /usr1/home/abdulla.fathalla/.aixvipmap/envs/MLEnv

echo "starting script"

echo "===============================Uniform-Edge-FP-PointNetMLPJoint==============================="
python -u Disc_lifing_paper/Uniform/Edge/PointNetMLPJoint_FP/GPUL2.py --preset S_full_ln_pos12_fp --initial-batch 2

echo "===============================Uniform-Edge-weighted-PointNetMLPJoint==============================="
python -u Disc_lifing_paper/Uniform/Edge/PointNetMLPJoint_weighted/GPUL2_weighted.py --preset S_full_ln_pos12 --initial-batch 2

echo "DONE"
