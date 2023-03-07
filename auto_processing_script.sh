#!/bin/bash
#!/usr/bin/env python3
#SBATCH -A ceds
#SBATCH -t 50:00:00
#SBATCH -N 1
#SBATCH -p shared
#SBATCH -n 1
#SBATCH --mail-user <your_email_here>
#SBATCH --mail-type END

User="such559"
years_per_file="6"
input_file="EmissMIP_CESM1_FAMIPC5_NUG_SHP-30P-RED"
input_variables="bc_a1DDF,bc_a4DDF,bc_c1DDF,bc_c4DDF,bc_a1SFWET,bc_a4SFWET,bc_c1SFWET,bc_c4SFWET,so4_a1DDF,so4_a2DDF,so4_a3DDF,so4_c1DDF,so4_c2DDF,so4_c3DDF,so4_a1SFWET,so4_a2SFWET,so4_a3SFWET,so4_c1SFWET,so4_c2SFWET,so4_c3SFWET,SFbc_a4,bc_a4_CLXF,SFSO2,SO2_CLXF,FSNTOA,FSNT,FLNT,FSUTOA,SOLIN,FLUTC,FSNTOAC,CLDTOT,AODVIS,TGCLDIWP,PS,PBLH,SFDMS,CLOUD,DMS"
CESM_variables="drybc, e3sm_wetbc, dryso4, e3sm_wetso4, dryso2, wetso2, emibc, emiso2, rlut, rsut, rsdt, rlutcs, rsutcs, clt, cltc, od550aer, clivi, ps, bldep, emidms, cl, srf_dms"
CURRENT_SCENARIO="nudge-shp-30p-red"
start_year="1999"
end_year="2004"

cd /pic/projects/GCAM/Emissions-MIP/e3sm_to_cmip

cp cesm_user_config_draft_blank.json cesm_user_config_draft_current.json
sed -i "s/current_scenario/$CURRENT_SCENARIO/g" cesm_user_config_draft_current.json 

module purge
module load python/miniconda3.8
source /share/apps/python/miniconda3.8/etc/profile.d/conda.sh
conda activate cmorize
export TMPDIR=/qfs/people/$User/e3sm_to_cmip/e3sm_to_cmip/temp

ncclimo -7 --dfl_lvl=1 --ypf=$years_per_file --var=$input_variables -c $input_file --yr_srt=$start_year --yr_end=$end_year --input=/pic/dtn/ahsa361/CESM_runs/$input_file/run/atm --output=native_grid

cd native_grid

for fl in `ls *.nc` ; do
  ncap2 -O -s ' defdim("vrt_nbr",2); lon_bnds=make_bounds(lon,$vrt_nbr); lat_bnds=make_bounds(lat,$vrt_nbr);' ${fl} ../native_add_bounds/${fl}
done

cd /pic/projects/GCAM/Emissions-MIP/e3sm_to_cmip/e3sm_to_cmip

python -m e3sm_to_cmip -v $CESM_variables -u /pic/projects/GCAM/Emissions-MIP/e3sm_to_cmip/cesm_user_config_draft_current.json -i /pic/projects/GCAM/Emissions-MIP/e3sm_to_cmip/native_add_bounds -o /pic/projects/GCAM/Emissions-MIP/e3sm_to_cmip/CMIP6 -t /pic/projects/GCAM/Emissions-MIP/e3sm_to_cmip/cmip6-cmor-tables/Tables -H /pic/projects/GCAM/Emissions-MIP/e3sm_to_cmip/e3sm_to_cmip/e3sm_to_cmip/cmor_handlers
