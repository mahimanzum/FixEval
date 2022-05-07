#!/bin/bash

#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH -t 70:00:00
#SBATCH -p normal_q
#SBATCH --account=program_bugs
#SBATCH --mem-per-cpu=4G

module load Anaconda/2020.07
module load jdk/1.8.0
module list

cat evaluation/execution_evaluation_TC_arc_MP.py
echo start load env and run python

source activate python36
python evaluation/execution_evaluation_TC_arc_MP.py --references test_python2python_with_verdict_output.jsonl --language python --test_cases atcoder_test_ca$

exit;