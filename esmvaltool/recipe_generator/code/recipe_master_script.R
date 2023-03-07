#load required libraries
library(yaml)
library(dplyr)
library(purrr)

#set working directory to recipe generator folder 
setwd("C:/Users/such559/Documents/emissions-mip/esmvaltool/recipe_generator")

#input parameters
input_datasets <- read.csv('code/dataset_input.csv', stringsAsFactors = FALSE)
input_variables <- read.csv('code/variable_list.csv', stringsAsFactors = FALSE)
input_masking <- read.csv('code/masking_list.csv', stringsAsFactors = FALSE)
input_scenario <- read.csv('code/scenario_list.csv', stringsAsFactors = FALSE)
input_exp <- read.csv('code/exp_list.csv', stringsAsFactors = FALSE)

#make a list of the regions
region_list <- input_masking$region_list
masks <- input_masking$mask_list 

#-------------------------------------------------------------------------------
#create a function that makes the correct dataset strings
dataset_create <- function(index,dataset_input,exp_input,scenario,year_set){
  #match the current data to the dataset information from the input file
  #source the experiment data from the exp_input folder
  curr_dataset <- dataset_input$dataset[index]
  curr_project <- dataset_input$project[index]
  curr_activity <- dataset_input$activity[index]
  curr_institute <- dataset_input$institute[index]
  curr_exp <- exp_input[which(exp_input$model == curr_dataset), scenario]
  curr_ensemble <- dataset_input$ensemble[index]
  curr_grid <- dataset_input$grid[index]
  
  #determine the input start and end years and the reference experiment names
  if(year_set == 'modern'){
    curr_start <- dataset_input$start_year[index]
    curr_end <- dataset_input$end_year[index]
    ref_exp <- exp_input[which(exp_input$model == curr_dataset), 'reference']
  } else if(year_set == 'old'){
    curr_start <- dataset_input$fifties_start[index]
    curr_end <- dataset_input$fifties_end[index]
    ref_exp <- exp_input[which(exp_input$model == curr_dataset), 'reference_1950']
  }else{
    #errors if the year specifier is input wrong
    stop('did not enter correct classification for modern_or_old column in input_scenario dataframe')
  }
  #create the dataset strings and put them into a list 
  reference_string <- paste0('{dataset: ',curr_dataset,', ', 'project: ', curr_project,', ', 'activity: ',curr_activity,', ','institute: ',curr_institute,', ', 'exp: ',ref_exp,', ','ensemble: ',curr_ensemble,', ','grid: ',curr_grid,', ','start_year: ',curr_start,', ','end_year: ',curr_end,'}')
  dataset_string <- paste0('{dataset: ',curr_dataset,', ', 'project: ', curr_project,', ', 'activity: ',curr_activity,', ','institute: ',curr_institute,', ', 'exp: ',curr_exp,', ','ensemble: ',curr_ensemble,', ','grid: ',curr_grid,', ','start_year: ',curr_start,', ','end_year: ',curr_end,'}')
  #create a list for the datasets
  strings <- list(reference_string,dataset_string)
  return(strings)
}

#create a function that creates variable-specific recipes
var_create <- function(curr_preproc,curr_mip,curr_add_datasets){
  #add all the collected data from the variables and dataset (input) csv files into a list for each var
  
  #add the additional datasets to the list if they exist
  if(length(curr_add_datasets) > 0 ){
    curr_var <- list( preprocessor = curr_preproc,
                      mip = curr_mip,
                      additional_datasets = curr_add_datasets)
  }else{
    curr_var <- list( preprocessor = curr_preproc,
                      mip = curr_mip)
  }
  
  return(curr_var)
}
#-------------------------------------------------------------------------------

#begin looping through each scenario
for(i in 1:nrow(input_scenario)){

#define diff type, name, and years to source
diff_type <- input_scenario$diff_type[i]
scenario_name <- input_scenario$scenario_name[i]
modern_or_old <- input_scenario$modern_or_old[i]

for (region in region_list) { #all of the following script will take place in this loop
  

	#mask the region from the input parameters 
	mask <- masks[which(region_list == region)] 
	
	  # Compile each component of the yml recipe file
		header <- list(description = "Analysis of perturbation model outputs for Emissions-MIP",
                 authors = list('nicholson_matthew'),
                 maintainer = list('nicholson_matthew'),
                 references = list('esmvaltool'),
                 projects = list('esmval', 'emissions_mip'))
  
		header_nested <- header %>%
			list(documentation = .)
  
		part1 <- as.yaml(header_nested, indent.mapping.sequence=TRUE,line.sep = "\n")
	
	#filter all the datasets that are applied to all variables
	dataset_all <-input_datasets %>% filter(variables == 'all')
	
	#check if there are any datasets with all variables specified before running next step
	if(nrow(dataset_all) >0 ){
	#empty list to be populated
	datasets <- list()
	
	#create a lists of datasets that specify all variables
	all_var_datasets <- dataset_all
	
	#create the dataset strings
	for ( i in 1:nrow(all_var_datasets)){
    #use assign to put all datasets into a list
	  datasets[[i]] <- assign(paste0(all_var_datasets$dataset[i]),dataset_create(i,all_var_datasets,input_exp,scenario_name,modern_or_old))
	}
	#append the lists of datasets together
	datasets <- list(datasets = flatten(datasets))

	#create part two of datasets
  part2 <- as.yaml(datasets, indent = 8, indent.mapping.sequence=TRUE,line.sep = "\n")
  part2 <- gsub("'", '', part2)
	}
  
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

  #create an empty list for variables
  variable_list <- list()

  #assign (using assign function) variable values from the csv file into a variables list like is currently done in the file
  #will be indexing down the columns
  for( i in 1:nrow(input_variables)) {
    var_name <- input_variables$variable_name[i]
    var_preprocessor <- input_variables$preprocessor[i]
    var_mip <- input_variables$mip[i]
    
    #create a list of datasets that contain the current variable
    df_of_additional_datasets <- input_datasets %>% filter(grepl(var_name,input_datasets$variables) == TRUE)
    
    #remove E3SM from dms (E3SM only uses srfdms, but the grep function picks up both names)
    if (var_name == 'dms'){
      df_of_additional_datasets <- df_of_additional_datasets[!grepl('E3SM-1-0',df_of_additional_datasets$dataset),]
    }
    
    #only do the following processing if the variable exists in any of the additional datasets  
    if(nrow(df_of_additional_datasets) > 0){
    #create empty list
    additional_datasets_list <- list()
    
    #create the dataset strings
      for ( j in 1:nrow(df_of_additional_datasets)){
        #use assign to put all datasets into a list
        additional_datasets_list[[j]] <- assign(paste0(df_of_additional_datasets$dataset[j]),dataset_create(j,df_of_additional_datasets,input_exp,scenario_name,modern_or_old))
      }
    
    #flatten the dataset list into a singular list
    additional_datasets_list <- flatten(additional_datasets_list)
    }else{
      #if the variable is not present in any dataset, return an empty list
      additional_datasets_list <- list()
    }
    
    variable_list[[var_name]] <- assign(var_name,var_create(var_preprocessor,var_mip,additional_datasets_list))
    
  }
  
  #add a scripts list to the bottom of the variables list
  scripting <- list(initial_analysis_output = list(script = paste0('/pic/projects/GCAM/Emissions-MIP/ESMValTool/esmvaltool/diag_scripts/emissions_mip/initial_analysis-giss-', diff_type, '.py'),
                                                quickplot = list(plot_type = 'pcolormesh')))



#then create Emissions_MIP_analysis list
Emissions_MIP_analysis_list = list(description = 'Model variable outputs',
                              themes = list('phys'),
                              realms = list('atmos'),
                              variables = variable_list,
                              scripts = scripting)

#feed this into the as.yaml and diagnostics list
part4 <- as.yaml(list(diagnostics = list(Emissions_MIP_analysis = Emissions_MIP_analysis_list)),indent.mapping.sequence=TRUE,line.sep = "\n")
                      
                      part4 <- gsub("'", '', part4)
                      
                      # Write out yaml file. Making sure to get rid of part 2 if it was not generated
                      if(nrow(dataset_all) > 0){
                      write(c(part1, part2, part3, part4), paste0("Phase1bv1.1c/", region, "/", region, "_", diff_type, "_", scenario_name,".yml"))
                      }else{
                        write(c(part1, part3, part4), paste0("Phase1bv1.1c/", region, "/", region, "_", diff_type, "_", scenario_name,".yml"))
                      }
} #end of for loop for the region

}#end of loop for scenario