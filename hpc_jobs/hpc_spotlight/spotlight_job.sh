#!/bin/bash

#SBATCH --job-name=spotlight-weights    # Job name
#SBATCH --output=spotlight.%j.out       # Name of output file (%j is job ID)
#SBATCH --error=spotlight.%j.err        # Error file
#SBATCH --cpus-per-task=4               # Number of CPU cores per task
#SBATCH --mem=48G                       # Memory
#SBATCH --gres=gpu:1                    # request one GPU
#SBATCH --time=04:00:00                 # Run time (hh:mm:ss)
#SBATCH --partition=scavenge		      	# Specifies the partition (queue) to submit the job to
#SBATCH --mail-type=BEGIN,END,FAIL	  	# E-mail when status changes

# Prints the name of the node (computer) where the job is running.
echo "Running on $(hostname):" 

# Move to folder
cd ~/hpc_spotlight/

module load Java/11.0.20
module load Anaconda3/2024.02-1
export LD_LIBRARY_PATH=/opt/itu/easybuild/software/Anaconda3/2024.02-1/lib:$LD_LIBRARY_PATH

java -Dfile.encoding=UTF-8 -Xmx20G -jar ~/spotlight-jar/dbpedia-spotlight.jar \
  ~/spotlight-models/en http://0.0.0.0:2221/rest &
SPOTLIGHT_PID=$!

echo "Waiting for Spotlight to come up on port 2221..."
for i in $(seq 1 90); do
  (echo > /dev/tcp/localhost/2221) 2>/dev/null && break
  sleep 10
done

python napoleon_in.py
python napoleon_out.py
