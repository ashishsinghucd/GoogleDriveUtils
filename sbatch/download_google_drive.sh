#!/bin/bash -l
#SBATCH -N 1
#SBATCH -n 8
#SBATCH -t 06:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=ashish.singh@ucdconnect.ie
#SBATCH --job-name=download_raw_videos_ashish

export SLURM_SUBMIT_DIR=/home/people/19205522/Research/Codes/google_drive/src/

cd $SLURM_SUBMIT_DIR

module load anaconda/3.5.2.0
conda activate /home/people/19205522/.conda/envs/google_drive/

time python download_multiprocessing.py /home/people/19205522/Research/Codes/google_drive/src/files_id.csv /home/people/19205522/scratch/GoogleDriveVideos/RawVideos /home/people/19205522/Research/Codes/google_drive/src/token.pickle 6 
date;
