#!/bin/bash
#SBATCH --job-name=GPU3(PN)
#SBATCH --output=Disc_lifing_paper_v2/GPU3.log
#SBATCH --error=Disc_lifing_paper_v2/GPU3.log
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

echo "===============================Edge_10_PointNetMLPJoint==============================="
python -u Disc_lifing_paper_v2/Zonal/Edge_10/PointNetMLPJoint_FP/GPUL2.py --preset S_full_ln_pos12_fp --initial-batch 2

echo "===============================Edge_25_PointNetMLPJoint==============================="
python -u Disc_lifing_paper_v2/Zonal/Edge_25/PointNetMLPJoint_FP/GPUL2.py --preset S_full_ln_pos12_fp --initial-batch 2

echo "===============================Edge_50_PointNetMLPJoint==============================="
python -u Disc_lifing_paper_v2/Zonal/Edge_50/PointNetMLPJoint_FP/GPUL2.py --preset S_full_ln_pos12_fp --initial-batch 2

echo "===============================Edge_75_PointNetMLPJoint==============================="
python -u Disc_lifing_paper_v2/Zonal/Edge_75/PointNetMLPJoint_FP/GPUL2.py --preset S_full_ln_pos12_fp --initial-batch 2


echo "DONE"
