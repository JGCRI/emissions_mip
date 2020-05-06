# ESMValTool Notes
## General
* Iris Cube latitude coordinate no longer accessible after arithmetic operation in `my_little_diagnostic.py`.
  * `diff_cube = cube[:, 0, :, :] - cube[:, 1, :, :]`
  * Might be due to preprocessor extracting 1000 hPa data, removing one of the four original dimensions.
  
* Need to replace `-` with `_` in dataset names.
  * From [ESMValCore dataset documentation](https://esmvaltool.readthedocs.io/projects/esmvalcore/en/latest/develop/fixing_data.html):
    ```
    Be careful to replace any - with _ in your dataset name.
    We need this replacement to have proper python module names.
    ```
## Diagnostic Scripts
### `initial_analysis.py`
* By default, the area-averages surface temperature data is returned as a monthly average.
* Compute annual average via `esmvalcore.preprocessor.annual_statistics(cube, operator='mean')`?
  * Params
    * `cube`: *iris.cube.Cube* - input cube.
    * `operator`: *str, optional* - Select operator to apply. Available operators: ‘mean’, ‘median’, ‘std_dev’, ‘sum’, ‘min’, ‘max’.
  * Returns
    * *iris.cube.Cube* - Annual statistics cube.
