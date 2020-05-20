Dev Notes for the Emissions-MIP project and [ESMValTool](https://github.com/ESMValGroup/ESMValTool) software package.

Last updated 20 May 2020.

Matt Nicholson

# Emissions-MIP

## Phase 1 Model Configurations

|   Run   |   Archive  |  Base/Perturb. | Wind Nudging | Seasonality | Modified Model Name    | Experiment Name |
| :------ |:---------- | :------------- |:------------ | :---------- | :--------------------- | :-------------- |
| BNW1999 | r1i1p5f101 | base           | no           | yes         | GISS-base              | season-so2      |
| PWN1999 | r1i1p5f102 | perturbation   | no           | no          | GISS-pert              | reference       |
| PW1999  | r1i1p5f103 | perturbation   | yes          | no          | GISS-pert-nudge        | reference       |
| BW1999  | r1i1p5f104 | base           | yes          | yes         | GISS-base-nudge        | season-so2      |
