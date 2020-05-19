# ESMValTool Notes
## General  
* Need to replace `-` with `_` in dataset names.
  * From [ESMValCore dataset documentation](https://esmvaltool.readthedocs.io/projects/esmvalcore/en/latest/develop/fixing_data.html):
    ```
    Be careful to replace any - with _ in your dataset name.
    We need this replacement to have proper python module names.
    ```
## Diagnostic Scripts
### Handling Multiple Ensembles of the Same Dataset
When given multiple 'ensembles' belonging to the same dataset, the preprocessor returns a data dictionary with a single dataset key and a value that constists of a list of multiple dictionaries, one for each 'ensemble'.

For example, given this `dataset` section in a recipe:
```YAML
datasets:
  - {dataset: GISS-E2-1-G, project: CMIP6, mip: AERmon, exp: piClim-SO2, ensemble: r1i1p5f101, grid: gn}
  - {dataset: GISS-E2-1-G, project: CMIP6, mip: AERmon, exp: piClim-SO2, ensemble: r1i1p5f102, grid: gn}
  - {dataset: GISS-E2-1-G, project: CMIP6, mip: AERmon, exp: piClim-SO2, ensemble: r1i1p5f103, grid: gn}
  - {dataset: GISS-E2-1-G, project: CMIP6, mip: AERmon, exp: piClim-SO2, ensemble: r1i1p5f104, grid: gn}
```
will yield a data dictionary with a single key, `GISS-E2-1-G`, and a value consisting of a list containing four dictionaries containing metadata for each of the four ensembles defined. 

---

### `initial_analysis.py`
* By default, the area-averages surface temperature data is returned as a monthly average.
* Compute annual average via `esmvalcore.preprocessor.annual_statistics(cube, operator='mean')`?
  * Params
    * `cube`: *iris.cube.Cube* - input cube.
    * `operator`: *str, optional* - Select operator to apply. Available operators: ‘mean’, ‘median’, ‘std_dev’, ‘sum’, ‘min’, ‘max’.
  * Returns
    * *iris.cube.Cube* - Annual statistics cube.
