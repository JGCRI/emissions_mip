from itertools import groupby, chain

metadata = {'GISS-base':
                [{'activity': 'AerChemMIP', 'alias': 'GISS-base_season-so2',
                  'dataset': 'GISS-base', 'diagnostic': 'diagnostic1', 'end_year': 2014,
                  'ensemble': 'r1i1p5f101', 'exp': 'season-so2',
                  'filename': '/home/nich980/emip/output/recipe-intial_analysis-giss/recipe-initial_analysis-giss_20200522_205555/preproc/diagnostic1/dryso4/CMIP6_GISS-base_AERmon_season-so2_r1i1p5f101_dryso4_2000-2014.nc',
                  'frequency': 'mon', 'grid': 'gn', 'institute': 'NASA-GISS',
                  'long_name': 'Dry Deposition Rate of SO4', 'mip': 'AERmon',
                  'modeling_realm': ['aerosol'], 'preprocessor': 'preproc_nolev',
                  'project': 'CMIP6', 'recipe_dataset_index': 0, 'short_name': 'dryso4',
                  'standard_name': 'minus_tendency_of_atmosphere_mass_content_of_sulfate_dry_aerosol_particles_due_to_dry_deposition',
                  'start_year': 2000, 'units': 'kg m-2 s-1', 'variable_group': 'dryso4'},
                 {'activity': 'AerChemMIP', 'alias': 'GISS-base_reference',
                  'dataset': 'GISS-base', 'diagnostic': 'diagnostic1', 'end_year': 2014,
                  'ensemble': 'r1i1p5f102', 'exp': 'reference',
                  'filename': '/home/nich980/emip/output/recipe-intial_analysis-giss/recipe-initial_analysis-giss_20200522_205555/preproc/diagnostic1/dryso4/CMIP6_GISS-base_AERmon_reference_r1i1p5f102_dryso4_2000-2014.nc',
                  'frequency': 'mon', 'grid': 'gn', 'institute': 'NASA-GISS',
                  'long_name': 'Dry Deposition Rate of SO4', 'mip': 'AERmon',
                  'modeling_realm': ['aerosol'], 'preprocessor': 'preproc_nolev',
                  'project': 'CMIP6', 'recipe_dataset_index': 1, 'short_name': 'dryso4',
                  'standard_name': 'minus_tendency_of_atmosphere_mass_content_of_sulfate_dry_aerosol_particles_due_to_dry_deposition',
                  'start_year': 2000, 'units': 'kg m-2 s-1', 'variable_group': 'dryso4'},
                 {'activity': 'AerChemMIP', 'alias': 'GISS-base_season-so2',
                  'dataset': 'GISS-base', 'diagnostic': 'diagnostic1', 'end_year': 2014,
                  'ensemble': 'r1i1p5f101', 'exp': 'season-so2',
                  'filename': '/home/nich980/emip/output/recipe-intial_analysis-giss/recipe-initial_analysis-giss_20200522_205555/preproc/diagnostic1/emiso2/CMIP6_GISS-base_AERmon_season-so2_r1i1p5f101_emiso2_2000-2014.nc',
                  'frequency': 'mon', 'grid': 'gn', 'institute': 'NASA-GISS',
                  'long_name': 'Total Emission Rate of SO2', 'mip': 'AERmon',
                  'modeling_realm': ['aerosol'], 'preprocessor': 'preproc_nolev',
                  'project': 'CMIP6', 'recipe_dataset_index': 0, 'short_name': 'emiso2',
                  'standard_name': 'tendency_of_atmosphere_mass_content_of_sulfur_dioxide_due_to_emission',
                  'start_year': 2000, 'units': 'kg m-2 s-1', 'variable_group': 'emiso2'},
                 {'activity': 'AerChemMIP', 'alias': 'GISS-base_reference',
                  'dataset': 'GISS-base', 'diagnostic': 'diagnostic1', 'end_year': 2014,
                  'ensemble': 'r1i1p5f102', 'exp': 'reference',
                  'filename': '/home/nich980/emip/output/recipe-intial_analysis-giss/recipe-initial_analysis-giss_20200522_205555/preproc/diagnostic1/emiso2/CMIP6_GISS-base_AERmon_reference_r1i1p5f102_emiso2_2000-2014.nc',
                  'frequency': 'mon', 'grid': 'gn', 'institute': 'NASA-GISS',
                  'long_name': 'Total Emission Rate of SO2', 'mip': 'AERmon',
                  'modeling_realm': ['aerosol'], 'preprocessor': 'preproc_nolev',
                  'project': 'CMIP6', 'recipe_dataset_index': 1, 'short_name': 'emiso2',
                  'standard_name': 'tendency_of_atmosphere_mass_content_of_sulfur_dioxide_due_to_emission',
                  'start_year': 2000, 'units': 'kg m-2 s-1', 'variable_group': 'emiso2'},
                 {'activity': 'AerChemMIP', 'alias': 'GISS-base_season-so2',
                  'dataset': 'GISS-base', 'diagnostic': 'diagnostic1', 'end_year': 2014,
                  'ensemble': 'r1i1p5f101', 'exp': 'season-so2',
                  'filename': '/home/nich980/emip/output/recipe-intial_analysis-giss/recipe-initial_analysis-giss_20200522_205555/preproc/diagnostic1/emiso4/CMIP6_GISS-base_AERmon_season-so2_r1i1p5f101_emiso4_2000-2014.nc',
                  'frequency': 'mon', 'grid': 'gn', 'institute': 'NASA-GISS',
                  'long_name': 'Total Direct Emission Rate of SO4', 'mip': 'AERmon',
                  'modeling_realm': ['aerosol'], 'preprocessor': 'preproc_nolev',
                  'project': 'CMIP6', 'recipe_dataset_index': 0, 'short_name': 'emiso4',
                  'standard_name': 'tendency_of_atmosphere_mass_content_of_sulfate_dry_aerosol_particles_due_to_emission',
                  'start_year': 2000, 'units': 'kg m-2 s-1', 'variable_group': 'emiso4'},
                 {'activity': 'AerChemMIP', 'alias': 'GISS-base_reference', 'dataset': 'GISS-base',
                  'diagnostic': 'diagnostic1', 'end_year': 2014, 'ensemble': 'r1i1p5f102', 'exp': 'reference',
                  'filename': '/home/nich980/emip/output/recipe-intial_analysis-giss/recipe-initial_analysis-giss_20200522_205555/preproc/diagnostic1/emiso4/CMIP6_GISS-base_AERmon_reference_r1i1p5f102_emiso4_2000-2014.nc',
                  'frequency': 'mon', 'grid': 'gn', 'institute': 'NASA-GISS', 'long_name': 'Total Direct Emission Rate of SO4',
                  'mip': 'AERmon', 'modeling_realm': ['aerosol'], 'preprocessor': 'preproc_nolev',
                  'project': 'CMIP6', 'recipe_dataset_index': 1, 'short_name': 'emiso4',
                  'standard_name': 'tendency_of_atmosphere_mass_content_of_sulfate_dry_aerosol_particles_due_to_emission',
                  'start_year': 2000, 'units': 'kg m-2 s-1', 'variable_group': 'emiso4'},
                 {'activity': 'AerChemMIP', 'alias': 'GISS-base_season-so2', 'dataset': 'GISS-base',
                  'diagnostic': 'diagnostic1', 'end_year': 2014, 'ensemble': 'r1i1p5f101', 'exp': 'season-so2',
                  'filename': '/home/nich980/emip/output/recipe-intial_analysis-giss/recipe-initial_analysis-giss_20200522_205555/preproc/diagnostic1/mmrdust/CMIP6_GISS-base_AERmon_season-so2_r1i1p5f101_mmrdust_2000-2014.nc',
                  'frequency': 'mon', 'grid': 'gn', 'institute': 'NASA-GISS', 'long_name': 'Dust Aerosol Mass Mixing Ratio',
                  'mip': 'AERmon', 'modeling_realm': ['aerosol'], 'preprocessor': 'preproc_100hPa',
                  'project': 'CMIP6', 'recipe_dataset_index': 0, 'short_name': 'mmrdust',
                  'standard_name': 'mass_fraction_of_dust_dry_aerosol_particles_in_air',
                  'start_year': 2000, 'units': 'kg kg-1', 'variable_group': 'mmrdust'},
                 {'activity': 'AerChemMIP', 'alias': 'GISS-base_reference', 'dataset': 'GISS-base',
                  'diagnostic': 'diagnostic1', 'end_year': 2014, 'ensemble': 'r1i1p5f102', 'exp': 'reference',
                  'filename': '/home/nich980/emip/output/recipe-intial_analysis-giss/recipe-initial_analysis-giss_20200522_205555/preproc/diagnostic1/mmrdust/CMIP6_GISS-base_AERmon_reference_r1i1p5f102_mmrdust_2000-2014.nc',
                  'frequency': 'mon', 'grid': 'gn', 'institute': 'NASA-GISS', 'long_name': 'Dust Aerosol Mass Mixing Ratio',
                  'mip': 'AERmon', 'modeling_realm': ['aerosol'], 'preprocessor': 'preproc_100hPa',
                  'project': 'CMIP6', 'recipe_dataset_index': 1, 'short_name': 'mmrdust',
                  'standard_name': 'mass_fraction_of_dust_dry_aerosol_particles_in_air',
                  'start_year': 2000, 'units': 'kg kg-1', 'variable_group': 'mmrdust'}
                ],
            'GISS-nudge':
                [{'activity': 'AerChemMIP', 'alias': 'GISS-nudge_season-so2',
                  'dataset': 'GISS-nudge', 'diagnostic': 'diagnostic1', 'end_year': 2014,
                  'ensemble': 'r1i1p5f101', 'exp': 'season-so2',
                  'filename': '/home/nich980/emip/output/recipe-intial_analysis-giss/recipe-initial_analysis-giss_20200522_205555/preproc/diagnostic1/dryso4/CMIP6_GISS-nudge_AERmon_season-so2_r1i1p5f101_dryso4_2000-2014.nc',
                  'frequency': 'mon', 'grid': 'gn', 'institute': 'NASA-GISS',
                  'long_name': 'Dry Deposition Rate of SO4', 'mip': 'AERmon',
                  'modeling_realm': ['aerosol'], 'preprocessor': 'preproc_nolev',
                  'project': 'CMIP6', 'recipe_dataset_index': 0, 'short_name': 'dryso4',
                  'standard_name': 'minus_tendency_of_atmosphere_mass_content_of_sulfate_dry_aerosol_particles_due_to_dry_deposition',
                  'start_year': 2000, 'units': 'kg m-2 s-1', 'variable_group': 'dryso4'},
                 {'activity': 'AerChemMIP', 'alias': 'GISS-nudge_reference',
                  'dataset': 'GISS-nudge', 'diagnostic': 'diagnostic1', 'end_year': 2014,
                  'ensemble': 'r1i1p5f102', 'exp': 'reference',
                  'filename': '/home/nich980/emip/output/recipe-intial_analysis-giss/recipe-initial_analysis-giss_20200522_205555/preproc/diagnostic1/dryso4/CMIP6_GISS-nudge_AERmon_reference_r1i1p5f102_dryso4_2000-2014.nc',
                  'frequency': 'mon', 'grid': 'gn', 'institute': 'NASA-GISS',
                  'long_name': 'Dry Deposition Rate of SO4', 'mip': 'AERmon',
                  'modeling_realm': ['aerosol'], 'preprocessor': 'preproc_nolev',
                  'project': 'CMIP6', 'recipe_dataset_index': 1, 'short_name': 'dryso4',
                  'standard_name': 'minus_tendency_of_atmosphere_mass_content_of_sulfate_dry_aerosol_particles_due_to_dry_deposition',
                  'start_year': 2000, 'units': 'kg m-2 s-1', 'variable_group': 'dryso4'},
                 {'activity': 'AerChemMIP', 'alias': 'GISS-nudge_season-so2',
                  'dataset': 'GISS-nudge', 'diagnostic': 'diagnostic1', 'end_year': 2014,
                  'ensemble': 'r1i1p5f101', 'exp': 'season-so2',
                  'filename': '/home/nich980/emip/output/recipe-intial_analysis-giss/recipe-initial_analysis-giss_20200522_205555/preproc/diagnostic1/emiso2/CMIP6_GISS-nudge_AERmon_season-so2_r1i1p5f101_emiso2_2000-2014.nc',
                  'frequency': 'mon', 'grid': 'gn', 'institute': 'NASA-GISS',
                  'long_name': 'Total Emission Rate of SO2', 'mip': 'AERmon',
                  'modeling_realm': ['aerosol'], 'preprocessor': 'preproc_nolev',
                  'project': 'CMIP6', 'recipe_dataset_index': 0, 'short_name': 'emiso2',
                  'standard_name': 'tendency_of_atmosphere_mass_content_of_sulfur_dioxide_due_to_emission',
                  'start_year': 2000, 'units': 'kg m-2 s-1', 'variable_group': 'emiso2'},
                 {'activity': 'AerChemMIP', 'alias': 'GISS-nudge_reference',
                  'dataset': 'GISS-nudge', 'diagnostic': 'diagnostic1', 'end_year': 2014,
                  'ensemble': 'r1i1p5f102', 'exp': 'reference',
                  'filename': '/home/nich980/emip/output/recipe-intial_analysis-giss/recipe-initial_analysis-giss_20200522_205555/preproc/diagnostic1/emiso2/CMIP6_GISS-nudge_AERmon_reference_r1i1p5f102_emiso2_2000-2014.nc',
                  'frequency': 'mon', 'grid': 'gn', 'institute': 'NASA-GISS',
                  'long_name': 'Total Emission Rate of SO2', 'mip': 'AERmon',
                  'modeling_realm': ['aerosol'], 'preprocessor': 'preproc_nolev',
                  'project': 'CMIP6', 'recipe_dataset_index': 1, 'short_name': 'emiso2',
                  'standard_name': 'tendency_of_atmosphere_mass_content_of_sulfur_dioxide_due_to_emission',
                  'start_year': 2000, 'units': 'kg m-2 s-1', 'variable_group': 'emiso2'},
                 {'activity': 'AerChemMIP', 'alias': 'GISS-nudge_season-so2',
                  'dataset': 'GISS-nudge', 'diagnostic': 'diagnostic1', 'end_year': 2014,
                  'ensemble': 'r1i1p5f101', 'exp': 'season-so2',
                  'filename': '/home/nich980/emip/output/recipe-intial_analysis-giss/recipe-initial_analysis-giss_20200522_205555/preproc/diagnostic1/emiso4/CMIP6_GISS-nudge_AERmon_season-so2_r1i1p5f101_emiso4_2000-2014.nc',
                  'frequency': 'mon', 'grid': 'gn', 'institute': 'NASA-GISS',
                  'long_name': 'Total Direct Emission Rate of SO4', 'mip': 'AERmon',
                  'modeling_realm': ['aerosol'], 'preprocessor': 'preproc_nolev',
                  'project': 'CMIP6', 'recipe_dataset_index': 0, 'short_name': 'emiso4',
                  'standard_name': 'tendency_of_atmosphere_mass_content_of_sulfate_dry_aerosol_particles_due_to_emission',
                  'start_year': 2000, 'units': 'kg m-2 s-1', 'variable_group': 'emiso4'},
                 {'activity': 'AerChemMIP', 'alias': 'GISS-nudge_reference', 'dataset': 'GISS-nudge',
                  'diagnostic': 'diagnostic1', 'end_year': 2014, 'ensemble': 'r1i1p5f102', 'exp': 'reference',
                  'filename': '/home/nich980/emip/output/recipe-intial_analysis-giss/recipe-initial_analysis-giss_20200522_205555/preproc/diagnostic1/emiso4/CMIP6_GISS-nudge_AERmon_reference_r1i1p5f102_emiso4_2000-2014.nc',
                  'frequency': 'mon', 'grid': 'gn', 'institute': 'NASA-GISS', 'long_name': 'Total Direct Emission Rate of SO4',
                  'mip': 'AERmon', 'modeling_realm': ['aerosol'], 'preprocessor': 'preproc_nolev',
                  'project': 'CMIP6', 'recipe_dataset_index': 1, 'short_name': 'emiso4',
                  'standard_name': 'tendency_of_atmosphere_mass_content_of_sulfate_dry_aerosol_particles_due_to_emission',
                  'start_year': 2000, 'units': 'kg m-2 s-1', 'variable_group': 'emiso4'},
                 {'activity': 'AerChemMIP', 'alias': 'GISS-nudge_season-so2', 'dataset': 'GISS-nudge',
                  'diagnostic': 'diagnostic1', 'end_year': 2014, 'ensemble': 'r1i1p5f101', 'exp': 'season-so2',
                  'filename': '/home/nich980/emip/output/recipe-intial_analysis-giss/recipe-initial_analysis-giss_20200522_205555/preproc/diagnostic1/mmrdust/CMIP6_GISS-nudge_AERmon_season-so2_r1i1p5f101_mmrdust_2000-2014.nc',
                  'frequency': 'mon', 'grid': 'gn', 'institute': 'NASA-GISS', 'long_name': 'Dust Aerosol Mass Mixing Ratio',
                  'mip': 'AERmon', 'modeling_realm': ['aerosol'], 'preprocessor': 'preproc_100hPa',
                  'project': 'CMIP6', 'recipe_dataset_index': 0, 'short_name': 'mmrdust',
                  'standard_name': 'mass_fraction_of_dust_dry_aerosol_particles_in_air',
                  'start_year': 2000, 'units': 'kg kg-1', 'variable_group': 'mmrdust'},
                 {'activity': 'AerChemMIP', 'alias': 'GISS-nudge_reference', 'dataset': 'GISS-nudge',
                  'diagnostic': 'diagnostic1', 'end_year': 2014, 'ensemble': 'r1i1p5f102', 'exp': 'reference',
                  'filename': '/home/nich980/emip/output/recipe-intial_analysis-giss/recipe-initial_analysis-giss_20200522_205555/preproc/diagnostic1/mmrdust/CMIP6_GISS-nudge_AERmon_reference_r1i1p5f102_mmrdust_2000-2014.nc',
                  'frequency': 'mon', 'grid': 'gn', 'institute': 'NASA-GISS', 'long_name': 'Dust Aerosol Mass Mixing Ratio',
                  'mip': 'AERmon', 'modeling_realm': ['aerosol'], 'preprocessor': 'preproc_100hPa',
                  'project': 'CMIP6', 'recipe_dataset_index': 1, 'short_name': 'mmrdust',
                  'standard_name': 'mass_fraction_of_dust_dry_aerosol_particles_in_air',
                  'start_year': 2000, 'units': 'kg kg-1', 'variable_group': 'mmrdust'}
                ]
            }

def group_meta_by_var(meta_dict):
    # Get list of every value dictionary
    meta_list = list(chain.from_iterable(list(metadata.values())))

    # Get dict from list keyed on variable
    meta_list.sort(key=lambda x: x['short_name'])
    var_groups = {k: list(v) for k, v in groupby(meta_list, lambda d: d['short_name'])}
    
    for var, dict_list in var_groups .items():
        print('Key: {}'.format(var))
        print('Val: {}'.format(dict_list))
        print('-' * 60)
        
    # print(var_groups)



group_meta_by_var(metadata)

# datasets = [group_meta(metadata[dataset]) for dataset in list(metadata.keys())]

# for dataset in datasets:
    # for dataset_name, var_group in dataset:
        # print('Dataset: {}'.format(dataset_name))
        # print('Var group: {}'.format(list(var_group)))
        
        