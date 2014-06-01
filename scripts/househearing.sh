#!/bin/bash

#tell grid engine to use current directory
#$ -cwd

#tell grid engine to email on job begin and end
#$ -M jfortuna@stanford.edu
#$ -m be

python househearing.py
