#!/bin/sh

rm -rf results/*

./run.sh results/toy_seq --experiment SequencePrototypeExperiment --generations 100
./run.sh results/toy_th --experiment ThresholdPrototypeExperiment --generations 100
./run.sh results/casestudy_th --experiment ThresholdCaseStudyExperiment --generations 100

python static_results.py --experiment ThresholdPrototypeExperiment --save results/static_toy_th
python static_results.py --experiment ThresholdCaseStudyExperiment --save results/static_casestudy_th
