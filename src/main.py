"""
Main for development & testing.

Matt Nicholson
13 April 2020
"""
import netcdf
import netcdf_variable
import date_utils
import var_funcs
import plotting

nc_filename = 'tests/dryso4_AERmon_GISS-E2-1-G_piClim-SO2_r1i1p5f103_gn_200001-201412.nc'
nc_obj = netcdf.Netcdf(nc_filename)


plotting.plot_global_mean_annual('dryso4', nc_obj)