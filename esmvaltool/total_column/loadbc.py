"""Derivation of variable ``loadbc``."""

import warnings

import cf_units
import iris
from scipy import constants

from .._regrid import extract_levels, regrid
from ._baseclass import DerivedVariableBase
from ._shared import pressure_level_widths

# Constants
STANDARD_GRAVITY = constants.value('standard acceleration of gravity')
STANDARD_GRAVITY_UNIT = constants.unit('standard acceleration of gravity')


def ensure_correct_lon(mmrbc_cube, ps_cube=None):
    """Ensure that ``mmrbc`` cube contains ``longitude`` and adapt ``ps`` cube."""
    if mmrbc_cube.coords('longitude'):
        return (mmrbc_cube, ps_cube)

    # Get zonal mean ps if necessary
    if ps_cube is not None:
        ps_cube = ps_cube.collapsed('longitude', iris.analysis.MEAN)
        ps_cube.remove_coord('longitude')

    # Add longitude dimension to mmrbc (and ps if necessary) with length 1
    cubes = (mmrbc_cube, ps_cube)
    new_cubes = []
    lon_coord = iris.coords.DimCoord([180.0], bounds=[[0.0, 360.0]],
                                     var_name='lon',
                                     standard_name='longitude',
                                     long_name='longitude',
                                     units='degrees_east')
    for cube in cubes:
        if cube is None:
            new_cubes.append(None)
            continue
        new_dim_coords = [(c, cube.coord_dims(c)) for c in cube.dim_coords]
        new_dim_coords.append((lon_coord, cube.ndim))
        new_aux_coords = [(c, cube.coord_dims(c)) for c in cube.aux_coords]
        new_cube = iris.cube.Cube(cube.core_data()[..., None],
                                  dim_coords_and_dims=new_dim_coords,
                                  aux_coords_and_dims=new_aux_coords)
        new_cube.metadata = cube.metadata
        new_cubes.append(new_cube)

    return tuple(new_cubes)


def interpolate_hybrid_plevs(cube):
    """Interpolate hybrid pressure levels."""
    # Use CMIP6's plev19 target levels (in Pa)
    target_levels = [
        100000.0,
        92500.0,
        85000.0,
        70000.0,
        60000.0,
        50000.0,
        40000.0,
        30000.0,
        25000.0,
        20000.0,
        15000.0,
        10000.0,
        7000.0,
        5000.0,
        3000.0,
        2000.0,
        1000.0,
        500.0,
        100.0,
    ]
    cube.coord('air_pressure').convert_units('Pa')
    cube = extract_levels(cube, target_levels, 'linear',
                          coordinate='air_pressure')
    return cube


class DerivedVariable(DerivedVariableBase):
    """Derivation of variable ``loadbc``."""

    @staticmethod
    def required(project):
        """Declare the variables needed for derivation."""
        # TODO: make get_required _derive/__init__.py use variables as argument
        # and make this dependent on mip
        if project == 'CMIP6':
            required = [
                {'short_name': 'mmrbc', 'mip': 'AERmon'},
                {'short_name': 'ps', 'mip': 'Amon'},
            ]
        else:
            required = [
                {'short_name': 'mmrbc'},
                {'short_name': 'ps'},
            ]
        return required

    @staticmethod
    def calculate(cubes):
        """Compute total column black carbon.

        Note
        ----
        The surface pressure is used as a lower integration bound. A fixed
        upper integration bound of 0 Pa is used.

        """
        mmrbc_cube = cubes.extract_strict(
            iris.Constraint(name='mass_fraction_of_elemental_carbon_dry_aerosol_particles_in_air'))
        ps_cube = cubes.extract_strict(
            iris.Constraint(name='surface_air_pressure'))

        # If mmrbc is given on hybrid pressure levels (e.g., from Table AERmon),
        # interpolate it to regular pressure levels
        if len(mmrbc_cube.coord_dims('air_pressure')) > 1:
            mmrbc_cube = interpolate_hybrid_plevs(mmrbc_cube)

        # To support zonal mean mmrbc (e.g., from Table AERmon), add longitude
        # coordinate if necessary and ensure that ps has correct shape
        (mmrbc_cube, ps_cube) = ensure_correct_lon(mmrbc_cube, ps_cube=ps_cube)

        # If the horizontal dimensions of ps and mmrbc differ, regrid ps
        # Note: regrid() checks if the regridding is really necessary before
        # running the actual interpolation
        ps_cube = regrid(ps_cube, mmrbc_cube, 'linear')

        # Actual derivation of loadbc using black carbon mass fraction and pressure level
        # widths
        p_layer_widths = pressure_level_widths(mmrbc_cube,
                                               ps_cube,
                                               top_limit=0.0)
        loadbc_cube = (mmrbc_cube * p_layer_widths / STANDARD_GRAVITY)
        with warnings.catch_warnings():
            warnings.filterwarnings(
                'ignore', category=UserWarning,
                message='Collapsing a non-contiguous coordinate')
            loadbc_cube = loadbc_cube.collapsed('air_pressure', iris.analysis.MEAN)
        loadbc_cube.units = (mmrbc_cube.units * p_layer_widths.units /
                          STANDARD_GRAVITY_UNIT)

        return loadbc_cube
