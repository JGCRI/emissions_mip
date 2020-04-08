"""
Configuration file.

Matt Nicholson
8 April 2020
"""
import os

class DIRS:
    proj_root = '/pic/projects/GCAM/mnichol/emip'
    model_output = os.path.join(proj_root, 'model-output')
    prefix_colum = ('columbia/gpfsm/dnb53/projects/p117/pub/CMIP6/AerChemMIP/NASA-GISS'
                    'GISS-E2-1-G/piClim-SO2/r1i1p5f103/AERmon')
    suffix_colum = 'gn/v20191120'