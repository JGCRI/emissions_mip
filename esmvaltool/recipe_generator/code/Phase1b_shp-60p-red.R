# ------------------------------------------------------------------------------
# Program Name: Phase1b_shp-60p-red-1950.R
# Authors: Hamza Ahsan
# Date Last Modified: October 27 2021
# Program Purpose: Produces recipes for Phase 1b to be used by ESMValTool. 
# Input Files: N/A
# Output Files: ~recipe_generator/Phase1b
# TODO:
# ------------------------------------------------------------------------------

# Load required libraries
library(yaml)
library(dplyr)

# Set working directory
#setwd("C:/Users/ahsa361/OneDrive - PNNL/Desktop/recipe_generator")
setwd("C:/Users/such559/Documents/emissions-mip/esmvaltool/recipe_generator")

# Specify absolute difference of percent difference (i.e., diff or per-diff)
diff_type <- ""

# Region list
region_list <- c('global', 'land', 'sea', 'arctic', 'NH-land', 'NH-sea', 
                 'SH-land', 'SH-sea', 'NH-pacific', 'NH-atlantic', 'NH-indian')

for (region in region_list) {
  
  # Define mask (inverse  of region)
  if(region == 'global') {
    mask <- NULL
  } else if(region == 'land') {
    mask <- 'sea'
  } else if(region == 'sea'){
    mask <- 'land'
  } else if(region == 'arctic'){
    mask <- 'non-arctic'
  } else if(region == 'NH-land'){
    mask <- 'sea_s-land'
  } else if(region == 'NH-sea'){
    mask <- 'land_s-sea'
  } else if(region == 'SH-land'){
    mask <- 'sea_n-land'
  } else if(region == 'SH-sea'){
    mask <- 'land_n-sea'
  } else if(region == 'NH-pacific'){
    mask <- 'non-pacific'
  } else if(region == 'NH-atlantic'){
    mask <- 'non-atlantic'
  } else if(region == 'NH-indian'){
    mask <- 'non-indian'
  } else(stop("The region specified is incorrect. Please check spelling."))
  
  # Compile each component of the yml recipe file
  header <- list(description = "Analysis of perturbation model outputs for Emissions-MIP",
                 authors = list('nicholson_matthew'),
                 maintainer = list('nicholson_matthew'),
                 references = list('esmvaltool'),
                 projects = list('esmval', 'emissions_mip'))
  
  header_nested <- header %>%
    list(documentation = .)
  
  part1 <- as.yaml(header_nested, indent.mapping.sequence=TRUE,line.sep = "\n")
  
  
  datasets <- list(datasets = list('{dataset: GISS-nudge, project: CMIP6, activity: AerChemMIP, institute: NASA-GISS, exp: reference, ensemble: r1i1p5f1, grid: gn}', 
                                   '{dataset: GISS-nudge, project: CMIP6, activity: AerChemMIP, institute: NASA-GISS, exp: 2000SHPdot4SO2, ensemble: r1i1p5f1, grid: gn}'))
  
  part2 <- as.yaml(datasets, indent = 8, indent.mapping.sequence=TRUE,line.sep = "\n")
  part2 <- gsub("'", '', part2)
  
  if(region == 'global'){
    part3 <- as.yaml(list(preprocessors = list(preproc_mask = list(mask_landsea = list(mask_out = mask)),
                                               preproc_sfc = list(extract_levels = list(levels = 100000,
                                                                                        scheme = 'linear_horizontal_extrapolate_vertical'),
                                                                  regrid = list(target_grid = '1x1',
                                                                                scheme = 'linear'),
                                                                  annual_statistics = list(operator = 'mean')),
                                               preproc_nolev = list(regrid = list(target_grid = '1x1',
                                                                                  scheme = 'linear'),
                                                                    annual_statistics = list(operator = 'mean')))),line.sep = "\n")
  } else {
    part3 <- as.yaml(list(preprocessors = list(preproc_sfc = list(extract_levels = list(levels = 100000,
                                                                                        scheme = 'linear_horizontal_extrapolate_vertical'),
                                                                  regrid = list(target_grid = '1x1',
                                                                                scheme = 'linear'),
                                                                  annual_statistics = list(operator = 'mean'),
                                                                  mask_landsea = list(mask_out = mask)),
                                               preproc_nolev = list(regrid = list(target_grid = '1x1',
                                                                                  scheme = 'linear'),
                                                                    annual_statistics = list(operator = 'mean'),
                                                                    mask_landsea = list(mask_out = mask)))),line.sep = "\n")
  }
  
  
  
  part4 <- as.yaml(list(diagnostics = list(Emissions_MIP_analysis = list(description = 'Model variable outputs',
                                                                        themes = list('phys'),
                                                                        realms = list('atmos'),
                                                                        variables = list(mmrso4 = list(preprocessor = 'preproc_sfc',
                                                                                                       mip = 'AERmon',
                                                                                                       start_year = as.integer(2000),
                                                                                                       end_year = as.integer(2004),
                                                                                                       additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         mmrbc = list(preprocessor = 'preproc_sfc',
                                                                                                      mip = 'AERmon',
                                                                                                      start_year = as.integer(2000),
                                                                                                      end_year = as.integer(2004),
                                                                                                      additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                 '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                 '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                 '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         so2 = list(preprocessor = 'preproc_sfc',
                                                                                                    mip = 'AERmon',
                                                                                                    start_year = as.integer(2000),
                                                                                                    end_year = as.integer(2004),
                                                                                                    additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                               '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                               '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                               '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         rlut = list(preprocessor = 'preproc_nolev',
                                                                                                     mip = 'Amon',
                                                                                                     start_year = as.integer(2000),
                                                                                                     end_year = as.integer(2004),
                                                                                                     additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         rsut = list(preprocessor = 'preproc_nolev',
                                                                                                     mip = 'Amon',
                                                                                                     start_year = as.integer(2000),
                                                                                                     end_year = as.integer(2004),
                                                                                                     additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         rsdt = list(preprocessor = 'preproc_nolev',
                                                                                                     mip = 'Amon',
                                                                                                     start_year = as.integer(2000),
                                                                                                     end_year = as.integer(2004),
                                                                                                     additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         rlutcs = list(preprocessor = 'preproc_nolev',
                                                                                                       mip = 'Amon',
                                                                                                       start_year = as.integer(2000),
                                                                                                       end_year = as.integer(2004),
                                                                                                       additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         rsutcs = list(preprocessor = 'preproc_nolev',
                                                                                                       mip = 'Amon',
                                                                                                       start_year = as.integer(2000),
                                                                                                       end_year = as.integer(2004),
                                                                                                       additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         emiso2 = list(preprocessor = 'preproc_nolev',
                                                                                                       mip = 'AERmon',
                                                                                                       start_year = as.integer(2000),
                                                                                                       end_year = as.integer(2004),
                                                                                                       additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         emibc = list(preprocessor = 'preproc_nolev',
                                                                                                      mip = 'AERmon',
                                                                                                      start_year = as.integer(2000),
                                                                                                      end_year = as.integer(2004),
                                                                                                      additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                 '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                 '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                 '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         drybc = list(preprocessor = 'preproc_nolev',
                                                                                                      mip = 'AERmon',
                                                                                                      start_year = as.integer(2000),
                                                                                                      end_year = as.integer(2004),
                                                                                                      additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                 '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                 '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                 '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         wetbc = list(preprocessor = 'preproc_nolev',
                                                                                                      mip = 'AERmon',
                                                                                                      start_year = as.integer(2000),
                                                                                                      end_year = as.integer(2004),
                                                                                                      additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                 '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                 '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                 '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         dryso2 = list(preprocessor = 'preproc_nolev',
                                                                                                       mip = 'AERmon',
                                                                                                       start_year = as.integer(2000),
                                                                                                       end_year = as.integer(2004)),
                                                                                         wetso2 = list(preprocessor = 'preproc_nolev',
                                                                                                       mip = 'AERmon',
                                                                                                       start_year = as.integer(2000),
                                                                                                       end_year = as.integer(2004)),
                                                                                         dryso4 = list(preprocessor = 'preproc_nolev',
                                                                                                       mip = 'AERmon',
                                                                                                       start_year = as.integer(2000),
                                                                                                       end_year = as.integer(2004),
                                                                                                       additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         wetso4 = list(preprocessor = 'preproc_nolev',
                                                                                                       mip = 'AERmon',
                                                                                                       start_year = as.integer(2000),
                                                                                                       end_year = as.integer(2004),
                                                                                                       additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         loadso2 = list(preprocessor = 'preproc_nolev',
                                                                                                        mip = 'Emon',
                                                                                                        start_year = as.integer(2000),
                                                                                                        end_year = as.integer(2004),
                                                                                                        additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                   '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                   '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                   '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         loadso4 = list(preprocessor = 'preproc_nolev',
                                                                                                        mip = 'Emon',
                                                                                                        start_year = as.integer(2000),
                                                                                                        end_year = as.integer(2004),
                                                                                                        additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                   '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                   '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                   '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         loadbc = list(preprocessor = 'preproc_nolev',
                                                                                                       mip = 'Emon',
                                                                                                       start_year = as.integer(2000),
                                                                                                       end_year = as.integer(2004),
                                                                                                       additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                  '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         dms = list(preprocessor = 'preproc_sfc',
                                                                                                    mip = 'AERmon',
                                                                                                    start_year = as.integer(2000),
                                                                                                    end_year = as.integer(2004)),
                                                                                         cl = list(preprocessor = 'preproc_sfc',
                                                                                                   mip = 'Amon',
                                                                                                   start_year = as.integer(2000),
                                                                                                   end_year = as.integer(2004),
                                                                                                   additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                              '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                              '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                              '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         clivi = list(preprocessor = 'preproc_nolev',
                                                                                                      mip = 'Amon',
                                                                                                      start_year = as.integer(2000),
                                                                                                      end_year = as.integer(2004),
                                                                                                      additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                 '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                 '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                 '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         od550aer = list(preprocessor = 'preproc_nolev',
                                                                                                         mip = 'AERmon',
                                                                                                         start_year = as.integer(2000),
                                                                                                         end_year = as.integer(2004),
                                                                                                         additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                    '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                    '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                                    '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         clt = list(preprocessor = 'preproc_nolev',
                                                                                                    mip = 'Amon',
                                                                                                    start_year = as.integer(2000),
                                                                                                    end_year = as.integer(2004),
                                                                                                    additional_datasets = list('{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                               '{dataset: CESM-1-0, project: CMIP6, activity: CMIP, institute: PNNL-WACCEM, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                               '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-ref, ensemble: r1i1p1f1, grid: gr}',
                                                                                                                               '{dataset: E3SM-1-0, project: CMIP6, activity: CMIP, institute: E3SM-Project, exp: nudge-shp-60p-red, ensemble: r1i1p1f1, grid: gr}')),
                                                                                         cltc = list(preprocessor = 'preproc_nolev',
                                                                                                     mip = 'AERmon',
                                                                                                     start_year = as.integer(2000),
                                                                                                     end_year = as.integer(2004))),
                                                                        scripts = list(initial_analysis_output = list(script = paste0('/pic/projects/GCAM/Emissions-MIP/ESMValTool/esmvaltool/diag_scripts/emissions_mip/initial_analysis-giss-', diff_type, '.py'),
                                                                                                                    quickplot = list(plot_type = 'pcolormesh')))))), indent.mapping.sequence=TRUE,line.sep = "\n")
  part4 <- gsub("'", '', part4)
  
  # Write out yaml file
  write(c(part1, part2, part3, part4), paste0("Phase1bv1.1/", region, "/", region, "_", diff_type, "_shp-60p-red.yml"))
}
