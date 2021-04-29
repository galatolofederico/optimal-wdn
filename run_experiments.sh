#!/bin/sh

generations=200

rm -rf results/*

./run.sh results/toy_seq --experiment SequencePrototypeExperiment --generations $generations
./run.sh results/toy_th --experiment ThresholdPrototypeExperiment --generations $generations
./run.sh results/casestudy_th --experiment ThresholdCaseStudyExperiment --generations $generations

python static_results.py --experiment ThresholdPrototypeExperiment --save results/static_toy_th
python static_results.py --experiment ThresholdCaseStudyExperiment --save results/static_casestudy_th
