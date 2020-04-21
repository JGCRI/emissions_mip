"""
Plotting functions.

Matt Nicholson
8 April 2020
"""
import matplotlib.pyplot as plt
import numpy as np
import os

import var_funcs
import date_utils
import path_funcs

class PLT_CONFIG:
    """
    Simple class of pyplot style configuration.
    
    colors : line colors.
        Values are names of pyplot colors.
    styles : line styles.
        '-'  : solid
        ':'  : dotted
        '-.' : dashed-dotted
        '--' : dashed
    markers : line markers.
        '.' : point
        '^' : triangle
        '2' : tri-up
        's' : square
        '+' : plus
    """
    colors  = ['red', 'orange', 'green', 'yellow', 'violet', 'cyan', 'royalblue',
               'fuschia', 'lime', 'black']
    styles  = ['-', ':', '-.', '--']
    markers = ['.', '^', '2', 's', '+']


def plot_global_mean_monthly(var_name, netcdf_objs, start_date=None, end_date=None):
    """
    Plot the global monthly mean for timeseries variable(s).
    
    Parameters
    ----------
    var_name : str
        Name of the variable to plot.
    netcdf_objs : list of Netcdf objects
        List of Netcdf objects containing the variable to plot.
    start_date : str, optional
        Date defining the beginning of a subset of the timeseries variable to plot.
        If not given, the entire timeseries for all variables will be plotted.
        Format: YYYY-MM.
    end_date : str, optional
        Date defining the end of a subset of the timeseries variable to plot.
        If not given, the entire timeseries for all variables will be plotted.
        Format: YYYY-MM.
        
    Returns
    -------
    None
    """
    plt.style.use('ggplot')
    fig, ax = plt.subplots()
    
    #TODO: Add time subset capabilities
    #   * Create a copy of the Netcdf object
    #   * Create a copy of its variables with adjusted timeseries
    
    # Check that the variables all have the same time series dates.
    if not isinstance(netcdf_objs, list):
        netcdf_objs = [netcdf_objs]
    else:
        date_check = all(netcdf.date_first == netcdf_objs[0].date_first and
            netcdf.date_last == netcdf_objs[0].date_last for netcdf in netcdf_objs)
        if not date_check:
            raise ValueError('Some Netcdf objects have mis-matched date values')
        
    units = netcdf_objs[0].get_var(var_name).units
    for idx, curr_nc in enumerate(netcdf_objs):
        line_color = PLT_CONFIG.colors[idx]
        curr_avg = var_funcs.global_mean_monthly(curr_nc, var_name)
        ax.plot(curr_avg, marker='.', color=PLT_CONFIG.colors[idx],
                label='{}-{}'.format(curr_nc.institution_id, curr_nc.forcing_index))
    # Set the number of x-ticks to (# monthly averages / 12) + 1, add appropriate
    # year labels. The result is an x-tick every 12 months plus the very last month.
    x_ticks = [t for t in range(netcdf_objs[0].get_var('time').shape[0])]
    x_tick_last = x_ticks[-1]
    x_ticks = x_ticks[0::12]
    x_ticks.append(x_tick_last)
    # Create the x-tick labels. Format: YYYY-MM
    x_tick_labels = date_utils.time_var_to_year_month(netcdf_objs[0].get_var('time'))
    x_tick_labels_last = x_tick_labels[-1]
    x_tick_labels = x_tick_labels[0::12]
    x_tick_labels.append(x_tick_labels_last)
    # Set the x ticks & their labels
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_tick_labels)
    # Set other axis attributes
    ax.set(xlabel='Date', ylabel=units,
       title='Global Monthly Means - {}'.format(var_name))
    ax.legend(loc='lower right')
    plt.show()
        

def plot_global_mean_annual(var_name, netcdf_objs, start_date=None, end_date=None):
    """
    Plot the global annual mean for timeseries variable(s).
    
    Parameters
    ----------
    var_name : str
        Name of the variable to plot.
    netcdf_objs : list of Netcdf objects
        List of Netcdf objects containing the variable to plot.
    start_date : str, optional
        Date defining the beginning of a subset of the timeseries variable to plot.
        If not given, the entire timeseries for all variables will be plotted.
        Format: YYYY-MM.
    end_date : str, optional
        Date defining the end of a subset of the timeseries variable to plot.
        If not given, the entire timeseries for all variables will be plotted.
        Format: YYYY-MM.
        
    Returns
    -------
    None
    """
    plt.style.use('ggplot')
    fig, ax = plt.subplots()
    fig.set_size_inches((8, 5))#, forward=False)
    
    #TODO: Add time subset capabilities
    #   * Create a copy of the Netcdf object
    #   * Create a copy of its variables with adjusted timeseries
    
    # Check that the variables all have the same time series dates.
    if not isinstance(netcdf_objs, list):
        netcdf_objs = [netcdf_objs]
    else:
        date_check = all(netcdf.date_first == netcdf_objs[0].date_first and
            netcdf.date_last == netcdf_objs[0].date_last for netcdf in netcdf_objs)
        if not date_check:
            raise ValueError('Some Netcdf objects have mis-matched date values')
        
    units = netcdf_objs[0].get_var(var_name).units
    for idx, curr_nc in enumerate(netcdf_objs):
        line_color = PLT_CONFIG.colors[idx]
        curr_avg = var_funcs.global_mean_annual(curr_nc, var_name)
        ax.plot(curr_avg, marker='.', color=PLT_CONFIG.colors[idx],
                label='{}-{}'.format(curr_nc.institution_id, curr_nc.forcing_index))
    # Set the number of x-ticks to (# monthly averages / 12) + 1, add appropriate
    # year labels. The result is an x-tick every 12 months plus the very last month.
    x_ticks = [x for x in range(curr_avg.shape[0])]
    # Create the x-tick labels. Format: YYYY-MM
    x_tick_labels = date_utils.time_var_to_years(netcdf_objs[0].get_var('time'))
    # Set the x ticks & their labels
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_tick_labels)
    # Set other axis attributes
    ax.set(xlabel='Year', ylabel=units,
       title='Global Annual Means - {}'.format(var_name))
    ax.legend()
    # plt.show()
    out_dir = os.path.join(path_funcs.get_root(), 'output')
    out_file = 'annual_mean-{}-{}_{}.pdf'.format(var_name, x_tick_labels[0],
                                                 x_tick_labels[-1])
    out_path = os.path.join(out_dir, out_file)
    plt.savefig(out_path, dpi=500)
    