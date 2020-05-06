# ESMVAlTool Notes
* Iris Cube latitude coordinate no longer accessible after arithmetic operation in `my_little_diagnostic.py`.
  * `diff_cube = cube[:, 0, :, :] - cube[:, 1, :, :]`
  
* Need to replace `-` with `_` in dataset names.
  * From [ESMValCore dataset documentation](https://esmvaltool.readthedocs.io/projects/esmvalcore/en/latest/develop/fixing_data.html):
    ```
    Be careful to replace any - with _ in your dataset name.
    We need this replacement to have proper python module names.
    ```
