# A brief description of the NASA-GISS model outputs



|   Run   |   Archive  |  Base/Perturb. | Wind Nudging | Seasonality | Modified Model Name | Experiment Name |
| :------ |:---------- | :------------- |:------------ | :---------- | :-------------------| :-------------- |
| BNW1999 | r1i1p5f101 | base           | no           | yes         | GISS-base           | szn_so2         |
| PWN1999 | r1i1p5f102 | perturbation   | no           | no          | GISS-base           | reference       |
| PW1999  | r1i1p5f103 | perturbation   | yes          | no          | GISS-nudge          | reference       |
| BW1999  | r1i1p5f104 | base           | yes          | yes         | GISS-nudge          | szn_so2         |

## Notes
* "Seasonality" means varying SO2. No seasonality = fixed SO2.
* Valid for initial analysis only. Free-running or nudged wind configuration will be selected for GCMs in the second phase.
