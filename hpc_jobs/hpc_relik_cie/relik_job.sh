#!/bin/bash

#SBATCH --job-name=relik-weights        # Job name
#SBATCH --output=relik.%j.out           # Name of output file (%j is job ID)
#SBATCH --error=relik.%j.err            # Error file
#SBATCH --cpus-per-task=4               # Number of CPU cores per task
#SBATCH --mem=48G                       # Memory
#SBATCH --gres=gpu:1                    # request one GPU
#SBATCH --time=12:00:00                 # Run time (hh:mm:ss)
#SBATCH --partition=scavenge			# Specifies the partition (queue) to submit the job to
#SBATCH --mail-type=BEGIN,END,FAIL		# E-mail when status changes

# Prints the name of the node (computer) where the job is running.
echo "Running on $(hostname):" 

#pip install relik

# Move to folder
cd ~/hpc_relik_cie/

python napoleon_in.py
python napoleon_out.py
