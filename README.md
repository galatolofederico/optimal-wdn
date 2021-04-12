# Optimal Management of Water Distribution Networks

Repository for the paper [Multi-objective optimization of water distribution networks via NSGA-II and Pseudo-Weights]()

## Installation

Clone this repository

```
git clone https://github.com/galatolofederico/optimal-wdn && cd optimal-wdn
```

Create a virtual environment and install the requirements

```
virtualenv --python=python3.7 env && . ./env/bin/activate
pip install -r requirements.txt
```

## Usage

To run the optimization :

```
python optimize.py
```

You can specify these arguments

|    Argument   |          Description         |           Default          |
|:-------------:|:----------------------------:|:--------------------------:|
|   --problem   |    The problem to optimize   | WaterDemandSequenceProblem |
|  --algorithm  | The Genetic Algorithm to use |            nsga2           |
| --generations |     Number of generations    |            1000            |
|     --save    |   Folder to save results to  |             100            |


To export an excel file with the results saved by `optimize.py`:

```
python export_results.py --folder <save-folder>
```

You can pass `--export-pseudo-weights` to export the pseudo weights.

This script will create `results.xlsx` in `<save-folder>`

To run the decision making on the results saved by `optimize.py`:

```
python decision_making.py --folder <save-folder>
```

## Replicate Results

For your convenience if you want to replicate the experiments proposed in the paper just run

```
./run_experiments.sh
```


## Acknowledgments and licensing

All my original work is released under the terms of the [GNU/GPLv3](https://choosealicense.com/licenses/gpl-3.0/) license. Copying, adapting and republishing it is not only consent but also encouraged. 

## Citing

If you want to cite use you can use this BibTeX

```
@article{galatolo_wdn
,	author	= {Ben Ammar, Samar and Cimino, Mario G.C.A and Foglia, Pierfrancesco and Galatolo, Federico A. and Nouiri, Issam}
,	title	= {Multi-objective optimization of water distribution networks via NSGA-II and Pseudo-Weights}
,	year	= {2021}
}
```

## Contacts

For any further question feel free to reach me at  [federico.galatolo@ing.unipi.it](mailto:federico.galatolo@ing.unipi.it) or on Telegram  [@galatolo](https://t.me/galatolo)
