# ENFORCE: FM-based Mission Planner for Robotic Applications

## Introduction

This repository contains a subset of the experiments reported in the verification chapter of Gabriele Belli's master thesis. 
In the thesis, the methodology is called MEMO, we have renamed it to Enforce for publication. A short vodeo of the experiments is available from https://www.youtube.com/watch?v=Q05MbCTeYxs

Each folder contains the experiments that answer the correspomding question described below:

RQ1. Does enforce effectively synthesize plans ensuring the satisfaction of the mission in a matter of minutes for single-robot applications? 

RQ2. Does enforce effectively synthesize plans ensuring the satisfaction in a matter of minutes for multi-robots applications? 

RQ3. Are the plans computed by enforce ensuring the mission satisfaction in simulated environments?

RQ4. Are the plans computed by enforce ensuring the mission satisfaction in real environments?

RQ3 has been adressed by running synthesized plans in RQ1 by Choreographe simulator.

## Reproducing Experiments
The scripts are executebale on linux using: Python (libraries: opencv, Pillow, numpy) and UPPAAL.

To avoid installation and configuration issues, we suggest to run the experiments using the provided docker file, as the following:

1. git clone
2. cd enforce
3. docker build -t enforce .
4. docker run -ti enforce .

Once you follow 1 - 4, then you could open each of the folders and run its sh scripts.

5. cd RQ1
6. ./test.sh

After termination of the script, you could find the generated files in the same folder.


