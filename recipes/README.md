# Emissions-MIP Initial Analysis Recipes
Initial analysis for EMIP is driven by the recipe files in this directory. These recipes use functions defined in files in the `src/` directory to process output variables and create plots.

## Usage
The recipes can be executed directly from the command line like so:
```
python plot_annual_means.py
```

or submitted as batch jobs on the pic HPC cluster via their respective shell handler script:
```
sbatch plot_annual_means.sh
```
