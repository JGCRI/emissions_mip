# Emissions-MIP Guide: Working with NetCDF Files
This guide will cover useful NCO, CDO and Linux commands for organizing and modifying NetCDF files, as well as more comprehensive sets of commands used for preparing specific model files. This step is generally performed prior to or in conjunction with running the ESMValTool, depending on the extent of file modifications required to successfully run through the ESMValTool workflow.

ESMValTool requires input files that are CMIP compatible. We can generally pass most model NetCDF files through ESMValTool, but there are cases where the files do not adhere to the correct CMIP format (e.g. variable attributes missing, 3D coordinate poorly defined, files containing only monthly data). A couple of very useful toolkits for modifying NetCDF files are NCO and CDO. These tools are standalone command-line programs that manipulate and analyze data on NetCDF files. They are preloaded on Constance and ready to use. To learn more about these tools and view detailed documentation, visit the links below.

NCO (NetCDF Operators): http://nco.sourceforge.net/

CDO (Climate Data Operators): https://code.mpimet.mpg.de/projects/cdo

## Model File Treatment
The table below provides a high-level overview of the steps taken to prepare model files for analysis by ESMValTool.
<table>
  <thead>
    <tr>
      <th>Model</th>
      <th>File location</th>
      <th>CMORize</th>
      <th>Model-specific steps</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan=1>CESM1</td>
      <td rowspan=2>Raw: /pic/dtn/ahsa361 <br> Backup: /pithos/projects/ceds/emissions-mip/rawdata_phase1 <br> Final: /pic/projects/GCAM/Emissions-MIP/models
      </td>
      <td rowspan=3>Yes</td>
      <td>
        <ul>
          <li>Multiplied <i>wetbc</i> and <i>wetso4</i> by -1 to get correct sign (currently applied in cmor handler but could be done in the R plotting scripts instead)</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>E3SM</td>
      <td>
        <ul>
          <li>Multiplied <i>wetbc</i> and <i>wetso4</i> by -1 to get correct sign (currently applied in cmor handler but could be done in the R plotting scripts instead)</li>
          <li><i>wetso2</i> was originally in units of kg/s so needed to divide by a 1&#176; area grid cell NetCDF file to get flux</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td rowspan=1>CESM2-WACCM</td>
      <td rowspan=8>Raw: /pic/dtn/observers <br> Backup: /pithos/projects/ceds/emissions-mip/rawdata_phase1 <br> Final: /pic/projects/GCAM/Emissions-MIP/models</td>
      <td>
        <ul>
          <li>Multiplied <i>wetbc</i>, <i>wetso2</i>, and <i>wetso4</i> by -1 to get correct sign (currently handled in the R plotting scripts)</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td rowspan=1>MIROC-SPRINTARS</td>
      <td rowspan=8>No</td>
      <td>
        <ul>
          <li>Organized files by experiment and renamed files for ESMValTool compatibility (e.g., &lt;variable&gt;_&lt;model&gt;_&lt;experiment&gt;_&lt;years&gt;.nc)</li>
          <li>Renamed convclt to cltc</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td rowspan=1>NorESM2</td>
      <td>
        <ul>
          <li>Renamed files for ESMValTool compatibility</li>
          <li>All variables needed to have their time axis reset to start from 2001 </li>
          <li>Changed units of <i>od550aer</i> from null (i.e., “”) to “1”</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td rowspan=1>OsloCTM3</td>
      <td>
        <ul>
          <li>emibc_OsloCTM3v1.02-EmiMIP_SO2-NO-SEASON is actually the BC-NO-SEASON file</li>
          <li>Added units of “kg m-2 s-1” to <i>emibc</i></li>
          <li>Removed ncomp dimension from <i>emibc</i> and <i>emiso2</i></li>
          <li>For 3D variables (<i>so2</i>, <i>mmrso4</i>, <i>mmrbc</i>):
            <ul>
              <li>changed ps long_name to "Surface Air Pressure"</li>
              <li>changed lev formula to "p(n,k,j,i) = ap(k) + b(k)*ps(n,j,i)"</li>
              <li>changed lev formula_terms to "ap: ap b: b ps: ps"</li>
              <li>changed lev standard_name to “atmosphere_hybrid_sigma_pressure_coordinate”</li>
              <li>changed ap_bnd to ap_bnds and b_bnd to b_bnds</li>
              <li>changed ap and ap_bnds units to "hPa"</li>
              <li>added positive = "down" to lev</li>
            </ul>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <td rowspan=1>GFDL</td>
      <td>
        <ul>
          <li>Organized files by experiment and renamed files for ESMValTool compatibility</li>
          <li>Renamed variable <i>wetso4_old</i> to <i>wetso4</i> and <i>dryso4_old</i> to <i>dryso4</i></li>
          <li>Added <i>ps</i> to all 3D variables (i.e., <i>so2</i>, <i>mmrbc</i>, and <i>mmrso4</i>)</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td rowspan=1>GISS</td>
      <td>
        <ul>
          <li>Made minor file name change (experiment) for consistency</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td rowspan=1>UKESM</td>
      <td>
        <ul>
          <li>See entire list of commands below</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td rowspan=1>GEOS</td>
      <td>
        <ul>
          <li>See entire list of commands below</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td rowspan=1>All (except E3SM/CESM1/CESM2-WACCM)</td>
      <td><i>See above</i></td>
      <td>
        <ul>
          <li>Added wavelength variable to <i>od550aer</i> (extracted from E3SM using <code>ncks</code>)</li>
          <li>Added attribute name "coordinates" called "wavelength" to <i>od550aer</i> (used <code>ncatted</code>)</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

Continue below for further details on specific commands used to perform the operations mentioned in the table.

## Useful Linux commands
For copying files recursively from one directory to another:\
`cp -R /path/to/folder /destination/path`

Copy only the directory content into another directory:\
`cp -R /path/to/folder/* /destination/path`

For copying large files (in size and amount) use `rsync` rather than `cp`. In case your connection fails, `rsync` is good at resuming the operations. The `-a` flag syncs recursively and keeps all permission and file settings. The `-v` flag will print information about files transferred and a brief summary at the end. Be aware of the need for a trailing slash in the source directory.\
`rsync -av /path/to/folder /destination/path`

List files in directory and output to a text file:\
`ls /dir > file.txt`

To view the header information, or metadata, of a NetCDF file:\
`ncdump -h /dir/file.nc`

It may also be useful to print the metadata to a text file:\
`ncdump -h /dir/file.nc > file.txt`

To rename part of a file recursively (e.g. replace NEW with OLD for all files in current directory and below):
```
find . -name "*OLD*" -type f -print0 | xargs -0 -I {} sh -c 'mv "{}" "$(dirname "{}")/`echo $(basename "{}") | sed 's/OLD/NEW/g'`"'
```

Replace dots with underscores in filenames, leaving extension intact:
```
perl -e '
         @files = grep {-f} glob "*";
         @old_files = @files;
         map {
              s!(.*)\.!$1/!;
              s!\.!_!g;
              s!/!.!
             } @files;
         rename $old_files[$_] => $files[$_] for (0..$#files)
        '
```

Print nth segment (e.g. 4th) of filename from all files in directory to a text file (filtered to unique):\
`ls | awk -F'[_]' '{print $4}' | sort | uniq > var.txt`

Generate directories based on list contained in text file:
```
mkdir `cat var.txt`
```

Move all files into corresponding directory (e.g. moving no-SO4 experiment files into folder):
```
awk -F[_] '{print "mv " $0 " /pithos/projects/ceds/emissions-mip/rawdata_phase1/miroc/SO4N/" $4 "/"}' < file.txt | sh -v
```

Execute command in text file line by line:\
`cat file.txt | sh -v`

To copy certain file extension (e.g. .csv files) from one directory to another:\
`scp -r /path/to/folder/*.csv /destination/path`

List file content in .zip file:\
`zipinfo -1 file.zip`

To zip a folder:\
`cd /folder`\
`zip -r ../zipped_dir.zip *`

Compress certain file extension (e.g. .csv files):\
`zip file.zip *.csv`

To delete a whole folder and its content recursively (WARNING – this deletes permanently):\
`rm -rf /path/to/folder`

To delete all files/folders in current directory without deleting the directory itself (WARNING – this deletes permanently):\
`rm -rf /path/to/folder/*`

## NCO commands
Extract a single variable (e.g. SO2):\
`ncks -v SO2 input.nc output.nc`

Extract certain dimensions (e.g. sector=7 (shipping) and time=599 (194912)):\
`ncks -d sector,7 SO2-em-anthro_190001-194912.nc CEDS_SO2_190001-194912.nc`\
`ncks -d time,599 CEDS_SO2_190001-194912.nc CEDS_SO2_194912.nc`

Replace certain variable values (e.g. replace emiss_ship<0 with 1):\
`ncap2 -s 'where(emiss_shp<0) emiss_shp=1;' RCP_shp_emiss.nc -O RCP_shp_emiss_new.nc`

Append variables from one file to another file:\
`ncks -A file1.nc file2.nc`

Change variable, dimension, or attribute names, where:
* h: do not add to the history variable
* O: (upper case) overwrite the file.
* d oldname,newname: to change a dimension name
* a oldname,newname: to change an attribute name

`ncrename -h -O -v old_variable_name,new_variable_name filename.nc`

Edit attributes where `-a` is followed by "attribute name, variable name, mode (append, create, delete, modify, overwrite), attribute variable type (float, character, ...), attribute value":\
`ncatted -O -a units,air,c,c,"units goes here" filename.nc`

Loop through all NetCDF files in current directory and edit a global attribute (e.g. references):
```
for fl in `ls *.nc` ; do
  ncatted -O -h -a references,global,c,c,"https://doi.org/10.25584/PNNLDataHub/1779095" ${fl}
done
```

## CDO commands
Merge multiple NetCDF files into a single file (e.g. three datasets with same timesteps and different variables in each dataset):\
`cdo merge infile1.nc infile2.nc infile3.nc outfile.nc`

Merge multiple NetCDF files into a single file if input files follow a naming convention or pattern:\
`cdo merge data_*.nc outfile.nc`

Extract a single variable from a NetCDF file:\
`cdo selvar,variable_name file.nc variable.nc`

Reset time start to specific year (e.g. 2001):\
`cdo settunits,days -settaxis,2001-01-01,00:00,1month infile.nc outfile.nc`

Divide first file by the second file (similarly with add, sub, mul):\
`cdo div infile1.nc infile2.nc outfile.nc`

Multiply a certain variable with a constant:\
`cdo aexpr,"myvar=myvar*3.14" infile.nc outfile.nc`

## Model-specific instructions
Below are examples of model-specific fixes needed prior to running through ESMValTool.

### NorESM2
For variable `od550aer`, change units from null to 1:
```
for fl in `ls /pithos/projects/ceds/emissions-mip/rawdata_phase1/NorESM2/base/od550aer_*.nc` ; do
  ncatted -O -a units,ap_bnds,m,c,"1" ${fl}
done
```

### OsloCTM3
For 3D variables, change lev formula to "p(n,k,j,i) = ap(k) + b(k)*ps(n,j,i)":
```
for fl in `ls /pithos/projects/ceds/emissions-mip/rawdata_phase1/OsloCTM3/base/mmrbc_*.nc` ; do
  ncatted -O -a formula,lev,m,c,"p(n,k,j,i) = ap(k) + b(k)*ps(n,j,i)" ${fl}
done
```

### GFDL
Replace dots with underscores in filenames, leaving extension intact:
```
perl -e '
         @files = grep {-f} glob "*";
         @old_files = @files;
         map {
              s!(.*)\.!$1/!;
              s!\.!_!g;
              s!/!.!
             } @files;
         rename $old_files[$_] => $files[$_] for (0..$#files)
        '
```

Print filenames and then rename:\
`ls *.nc > names.txt`\
`awk -F[_.] '{print "mv " $0 " " $4 "_GFDL_[experiment]_" $3 ".nc"}' < names.txt | sh -v`

For 3D variables, add variable `ps` (surface air pressure):
```
for fl in `ls /pithos/projects/ceds/emissions-mip/rawdata_phase1/GFDL/base/mmrbc_*.nc` ; do
  ncks -A ps.nc ${fl}
done
```

Rename variable `dryso4_old` to `dryso4`:
```
for fl in `ls /pithos/projects/ceds/emissions-mip/rawdata_phase1/GFDL/base/dryso4_*.nc` ; do
  ncrename -h -O -v dryso4_old,dryso4 ${fl}
done
```

### UKESM
This section includes the entire routine needed to modify any given set of UKESM model files.

Change current directory to /UKESM and make new directories:\
`mkdir base_merge base_mergefix base_timefix base_dimfix base_final`

Change directory to experiment folder:\
`cd base`

Generate a file with unique variable names (manually remove 3D and extraneous variables – only need to do this once, then use the same file for the other experiments):\
`ls | awk -F'[_.]' '{print $3}' | sort | uniq > 2D_vars.txt`

Feed each variable into the cdo merge command for each year:
```
awk -F[_] '{print "cdo merge 2000jan_UKESM1_" $0 ".nc 2000feb_UKESM1_" $0 ".nc 2000mar_UKESM1_" $0 ".nc 2000apr_UKESM1_" $0 ".nc 2000may_UKESM1_" $0 ".nc 2000jun_UKESM1_" $0 ".nc 2000jul_UKESM1_" $0 ".nc 2000aug_UKESM1_" $0 ".nc 2000sep_UKESM1_" $0 ".nc 2000oct_UKESM1_" $0 ".nc 2000nov_UKESM1_" $0 ".nc 2000dec_UKESM1_" $0 ".nc ../base_merge/" $0 "_UKESM_EmiMIP_base_2000_monthly.nc"}' < ../2D_vars.txt | sh -v

awk -F[_] '{print "cdo merge 2001jan_UKESM1_" $0 ".nc 2001feb_UKESM1_" $0 ".nc 2001mar_UKESM1_" $0 ".nc 2001apr_UKESM1_" $0 ".nc 2001may_UKESM1_" $0 ".nc 2001jun_UKESM1_" $0 ".nc 2001jul_UKESM1_" $0 ".nc 2001aug_UKESM1_" $0 ".nc 2001sep_UKESM1_" $0 ".nc 2001oct_UKESM1_" $0 ".nc 2001nov_UKESM1_" $0 ".nc 2001dec_UKESM1_" $0 ".nc ../base_merge/" $0 "_UKESM_EmiMIP_base_2001_monthly.nc"}' < ../2D_vars.txt | sh -v

awk -F[_] '{print "cdo merge 2002jan_UKESM1_" $0 ".nc 2002feb_UKESM1_" $0 ".nc 2002mar_UKESM1_" $0 ".nc 2002apr_UKESM1_" $0 ".nc 2002may_UKESM1_" $0 ".nc 2002jun_UKESM1_" $0 ".nc 2002jul_UKESM1_" $0 ".nc 2002aug_UKESM1_" $0 ".nc 2002sep_UKESM1_" $0 ".nc 2002oct_UKESM1_" $0 ".nc 2002nov_UKESM1_" $0 ".nc 2002dec_UKESM1_" $0 ".nc ../base_merge/" $0 "_UKESM_EmiMIP_base_2002_monthly.nc"}' < ../2D_vars.txt | sh -v

awk -F[_] '{print "cdo merge 2003jan_UKESM1_" $0 ".nc 2003feb_UKESM1_" $0 ".nc 2003mar_UKESM1_" $0 ".nc 2003apr_UKESM1_" $0 ".nc 2003may_UKESM1_" $0 ".nc 2003jun_UKESM1_" $0 ".nc 2003jul_UKESM1_" $0 ".nc 2003aug_UKESM1_" $0 ".nc 2003sep_UKESM1_" $0 ".nc 2003oct_UKESM1_" $0 ".nc 2003nov_UKESM1_" $0 ".nc 2003dec_UKESM1_" $0 ".nc ../base_merge/" $0 "_UKESM_EmiMIP_base_2003_monthly.nc"}' < ../2D_vars.txt | sh -v

awk -F[_] '{print "cdo merge 2004jan_UKESM1_" $0 ".nc 2004feb_UKESM1_" $0 ".nc 2004mar_UKESM1_" $0 ".nc 2004apr_UKESM1_" $0 ".nc 2004may_UKESM1_" $0 ".nc 2004jun_UKESM1_" $0 ".nc 2004jul_UKESM1_" $0 ".nc 2004aug_UKESM1_" $0 ".nc 2004sep_UKESM1_" $0 ".nc 2004oct_UKESM1_" $0 ".nc 2004nov_UKESM1_" $0 ".nc 2004dec_UKESM1_" $0 ".nc ../base_merge/" $0 "_UKESM_EmiMIP_base_2004_monthly.nc"}' < ../2D_vars.txt | sh -v
```

Change directory to experiment merge folder:\
`cd ../base_merge`

Rename sfc to time:
```
for fl in `ls *.nc` ; do
  ncrename -d sfc,time ${fl}
done
```

Remove sfc variable:
```
for fl in `ls *.nc` ; do
  ncks -O -x -v sfc ${fl} ../base_mergefix/${fl}
done
```

Format time dimension correctly for each year:
```
cd ../base_mergefix

for fl in `ls *2000_monthly.nc` ; do
  cdo -L settunits,days -settaxis,2000-01-01,00:00,1month ${fl} ../base_timefix/${fl}
done

for fl in `ls *2001_monthly.nc` ; do
  cdo -L settunits,days -settaxis,2001-01-01,00:00,1month ${fl} ../base_timefix/${fl}
done

for fl in `ls *2002_monthly.nc` ; do
  cdo -L settunits,days -settaxis,2002-01-01,00:00,1month ${fl} ../base_timefix/${fl}
done

for fl in `ls *2003_monthly.nc` ; do
  cdo -L settunits,days -settaxis,2003-01-01,00:00,1month ${fl} ../base_timefix/${fl}
done

for fl in `ls *2004_monthly.nc` ; do
  cdo -L settunits,days -settaxis,2004-01-01,00:00,1month ${fl} ../base_timefix/${fl}
done
```

Convert to netCDF3 to avoid dimension renaming bug:
```
cd ../base_timefix

for fl in `ls *.nc` ; do
  ncks -3 ${fl} ../base_dimfix/${fl}
done
```

Rename dimension names:
```
cd ../base_dimfix

for fl in `ls *.nc` ; do
  ncrename -O -v longitude,lon -v latitude,lat -d longitude,lon -d latitude,lat ${fl}
done
```

Convert back to netCDF4:
```
for fl in `ls *.nc` ; do
ncks -4 ${fl} ../base_final/${fl}
done
```

Add wavelength variable to `od550aer`:
```
cd ../base_final

for fl in `ls od550aer*.nc` ; do
  ncks -A ../wavelength.nc ${fl}
done

for fl in `ls od550aer*.nc` ; do
  ncatted -O -a coordinates,od550aer,c,c,"wavelength" ${fl}
done
```

Change current directory to /UKESM and make new directories:
```
cd ../
mkdir base_3D_time base_3D_merge base_3D_timefix base_3D_dimfix base_3D_dimfix2 base_3D_final
```

Add time dimension to 3D variables:
```
cd base

for fl in `ls *mmrbc_3D.nc` ; do
  ncecat -O -u time ${fl} ../base_3D_time/${fl}
done

for fl in `ls *mmrso4_3D.nc` ; do
  ncecat -O -u time ${fl} ../base_3D_time/${fl}
done

for fl in `ls *so2_3D.nc` ; do
  ncecat -O -u time ${fl} ../base_3D_time/${fl}
done
```

Merge files together:
```
cd ../base_3D_time

cdo mergetime 2000jan_UKESM1_mmrbc_3D.nc 2000feb_UKESM1_mmrbc_3D.nc 2000mar_UKESM1_mmrbc_3D.nc 2000apr_UKESM1_mmrbc_3D.nc 2000may_UKESM1_mmrbc_3D.nc 2000jun_UKESM1_mmrbc_3D.nc 2000jul_UKESM1_mmrbc_3D.nc 2000aug_UKESM1_mmrbc_3D.nc 2000sep_UKESM1_mmrbc_3D.nc 2000oct_UKESM1_mmrbc_3D.nc 2000nov_UKESM1_mmrbc_3D.nc 2000dec_UKESM1_mmrbc_3D.nc ../base_3D_merge/mmrbc_UKESM_EmiMIP_base_2000_monthly.nc

cdo mergetime 2001jan_UKESM1_mmrbc_3D.nc 2001feb_UKESM1_mmrbc_3D.nc 2001mar_UKESM1_mmrbc_3D.nc 2001apr_UKESM1_mmrbc_3D.nc 2001may_UKESM1_mmrbc_3D.nc 2001jun_UKESM1_mmrbc_3D.nc 2001jul_UKESM1_mmrbc_3D.nc 2001aug_UKESM1_mmrbc_3D.nc 2001sep_UKESM1_mmrbc_3D.nc 2001oct_UKESM1_mmrbc_3D.nc 2001nov_UKESM1_mmrbc_3D.nc 2001dec_UKESM1_mmrbc_3D.nc ../base_3D_merge/mmrbc_UKESM_EmiMIP_base_2001_monthly.nc

cdo mergetime 2002jan_UKESM1_mmrbc_3D.nc 2002feb_UKESM1_mmrbc_3D.nc 2002mar_UKESM1_mmrbc_3D.nc 2002apr_UKESM1_mmrbc_3D.nc 2002may_UKESM1_mmrbc_3D.nc 2002jun_UKESM1_mmrbc_3D.nc 2002jul_UKESM1_mmrbc_3D.nc 2002aug_UKESM1_mmrbc_3D.nc 2002sep_UKESM1_mmrbc_3D.nc 2002oct_UKESM1_mmrbc_3D.nc 2002nov_UKESM1_mmrbc_3D.nc 2002dec_UKESM1_mmrbc_3D.nc ../base_3D_merge/mmrbc_UKESM_EmiMIP_base_2002_monthly.nc

cdo mergetime 2003jan_UKESM1_mmrbc_3D.nc 2003feb_UKESM1_mmrbc_3D.nc 2003mar_UKESM1_mmrbc_3D.nc 2003apr_UKESM1_mmrbc_3D.nc 2003may_UKESM1_mmrbc_3D.nc 2003jun_UKESM1_mmrbc_3D.nc 2003jul_UKESM1_mmrbc_3D.nc 2003aug_UKESM1_mmrbc_3D.nc 2003sep_UKESM1_mmrbc_3D.nc 2003oct_UKESM1_mmrbc_3D.nc 2003nov_UKESM1_mmrbc_3D.nc 2003dec_UKESM1_mmrbc_3D.nc ../base_3D_merge/mmrbc_UKESM_EmiMIP_base_2003_monthly.nc

cdo mergetime 2004jan_UKESM1_mmrbc_3D.nc 2004feb_UKESM1_mmrbc_3D.nc 2004mar_UKESM1_mmrbc_3D.nc 2004apr_UKESM1_mmrbc_3D.nc 2004may_UKESM1_mmrbc_3D.nc 2004jun_UKESM1_mmrbc_3D.nc 2004jul_UKESM1_mmrbc_3D.nc 2004aug_UKESM1_mmrbc_3D.nc 2004sep_UKESM1_mmrbc_3D.nc 2004oct_UKESM1_mmrbc_3D.nc 2004nov_UKESM1_mmrbc_3D.nc 2004dec_UKESM1_mmrbc_3D.nc ../base_3D_merge/mmrbc_UKESM_EmiMIP_base_2004_monthly.nc

cdo mergetime 2000jan_UKESM1_mmrso4_3D.nc 2000feb_UKESM1_mmrso4_3D.nc 2000mar_UKESM1_mmrso4_3D.nc 2000apr_UKESM1_mmrso4_3D.nc 2000may_UKESM1_mmrso4_3D.nc 2000jun_UKESM1_mmrso4_3D.nc 2000jul_UKESM1_mmrso4_3D.nc 2000aug_UKESM1_mmrso4_3D.nc 2000sep_UKESM1_mmrso4_3D.nc 2000oct_UKESM1_mmrso4_3D.nc 2000nov_UKESM1_mmrso4_3D.nc 2000dec_UKESM1_mmrso4_3D.nc ../base_3D_merge/mmrso4_UKESM_EmiMIP_base_2000_monthly.nc

cdo mergetime 2001jan_UKESM1_mmrso4_3D.nc 2001feb_UKESM1_mmrso4_3D.nc 2001mar_UKESM1_mmrso4_3D.nc 2001apr_UKESM1_mmrso4_3D.nc 2001may_UKESM1_mmrso4_3D.nc 2001jun_UKESM1_mmrso4_3D.nc 2001jul_UKESM1_mmrso4_3D.nc 2001aug_UKESM1_mmrso4_3D.nc 2001sep_UKESM1_mmrso4_3D.nc 2001oct_UKESM1_mmrso4_3D.nc 2001nov_UKESM1_mmrso4_3D.nc 2001dec_UKESM1_mmrso4_3D.nc ../base_3D_merge/mmrso4_UKESM_EmiMIP_base_2001_monthly.nc

cdo mergetime 2002jan_UKESM1_mmrso4_3D.nc 2002feb_UKESM1_mmrso4_3D.nc 2002mar_UKESM1_mmrso4_3D.nc 2002apr_UKESM1_mmrso4_3D.nc 2002may_UKESM1_mmrso4_3D.nc 2002jun_UKESM1_mmrso4_3D.nc 2002jul_UKESM1_mmrso4_3D.nc 2002aug_UKESM1_mmrso4_3D.nc 2002sep_UKESM1_mmrso4_3D.nc 2002oct_UKESM1_mmrso4_3D.nc 2002nov_UKESM1_mmrso4_3D.nc 2002dec_UKESM1_mmrso4_3D.nc ../base_3D_merge/mmrso4_UKESM_EmiMIP_base_2002_monthly.nc

cdo mergetime 2003jan_UKESM1_mmrso4_3D.nc 2003feb_UKESM1_mmrso4_3D.nc 2003mar_UKESM1_mmrso4_3D.nc 2003apr_UKESM1_mmrso4_3D.nc 2003may_UKESM1_mmrso4_3D.nc 2003jun_UKESM1_mmrso4_3D.nc 2003jul_UKESM1_mmrso4_3D.nc 2003aug_UKESM1_mmrso4_3D.nc 2003sep_UKESM1_mmrso4_3D.nc 2003oct_UKESM1_mmrso4_3D.nc 2003nov_UKESM1_mmrso4_3D.nc 2003dec_UKESM1_mmrso4_3D.nc ../base_3D_merge/mmrso4_UKESM_EmiMIP_base_2003_monthly.nc

cdo mergetime 2004jan_UKESM1_mmrso4_3D.nc 2004feb_UKESM1_mmrso4_3D.nc 2004mar_UKESM1_mmrso4_3D.nc 2004apr_UKESM1_mmrso4_3D.nc 2004may_UKESM1_mmrso4_3D.nc 2004jun_UKESM1_mmrso4_3D.nc 2004jul_UKESM1_mmrso4_3D.nc 2004aug_UKESM1_mmrso4_3D.nc 2004sep_UKESM1_mmrso4_3D.nc 2004oct_UKESM1_mmrso4_3D.nc 2004nov_UKESM1_mmrso4_3D.nc 2004dec_UKESM1_mmrso4_3D.nc ../base_3D_merge/mmrso4_UKESM_EmiMIP_base_2004_monthly.nc

cdo mergetime 2000jan_UKESM1_so2_3D.nc 2000feb_UKESM1_so2_3D.nc 2000mar_UKESM1_so2_3D.nc 2000apr_UKESM1_so2_3D.nc 2000may_UKESM1_so2_3D.nc 2000jun_UKESM1_so2_3D.nc 2000jul_UKESM1_so2_3D.nc 2000aug_UKESM1_so2_3D.nc 2000sep_UKESM1_so2_3D.nc 2000oct_UKESM1_so2_3D.nc 2000nov_UKESM1_so2_3D.nc 2000dec_UKESM1_so2_3D.nc ../base_3D_merge/so2_UKESM_EmiMIP_base_2000_monthly.nc

cdo mergetime 2001jan_UKESM1_so2_3D.nc 2001feb_UKESM1_so2_3D.nc 2001mar_UKESM1_so2_3D.nc 2001apr_UKESM1_so2_3D.nc 2001may_UKESM1_so2_3D.nc 2001jun_UKESM1_so2_3D.nc 2001jul_UKESM1_so2_3D.nc 2001aug_UKESM1_so2_3D.nc 2001sep_UKESM1_so2_3D.nc 2001oct_UKESM1_so2_3D.nc 2001nov_UKESM1_so2_3D.nc 2001dec_UKESM1_so2_3D.nc ../base_3D_merge/so2_UKESM_EmiMIP_base_2001_monthly.nc

cdo mergetime 2002jan_UKESM1_so2_3D.nc 2002feb_UKESM1_so2_3D.nc 2002mar_UKESM1_so2_3D.nc 2002apr_UKESM1_so2_3D.nc 2002may_UKESM1_so2_3D.nc 2002jun_UKESM1_so2_3D.nc 2002jul_UKESM1_so2_3D.nc 2002aug_UKESM1_so2_3D.nc 2002sep_UKESM1_so2_3D.nc 2002oct_UKESM1_so2_3D.nc 2002nov_UKESM1_so2_3D.nc 2002dec_UKESM1_so2_3D.nc ../base_3D_merge/so2_UKESM_EmiMIP_base_2002_monthly.nc

cdo mergetime 2003jan_UKESM1_so2_3D.nc 2003feb_UKESM1_so2_3D.nc 2003mar_UKESM1_so2_3D.nc 2003apr_UKESM1_so2_3D.nc 2003may_UKESM1_so2_3D.nc 2003jun_UKESM1_so2_3D.nc 2003jul_UKESM1_so2_3D.nc 2003aug_UKESM1_so2_3D.nc 2003sep_UKESM1_so2_3D.nc 2003oct_UKESM1_so2_3D.nc 2003nov_UKESM1_so2_3D.nc 2003dec_UKESM1_so2_3D.nc ../base_3D_merge/so2_UKESM_EmiMIP_base_2003_monthly.nc

cdo mergetime 2004jan_UKESM1_so2_3D.nc 2004feb_UKESM1_so2_3D.nc 2004mar_UKESM1_so2_3D.nc 2004apr_UKESM1_so2_3D.nc 2004may_UKESM1_so2_3D.nc 2004jun_UKESM1_so2_3D.nc 2004jul_UKESM1_so2_3D.nc 2004aug_UKESM1_so2_3D.nc 2004sep_UKESM1_so2_3D.nc 2004oct_UKESM1_so2_3D.nc 2004nov_UKESM1_so2_3D.nc 2004dec_UKESM1_so2_3D.nc ../base_3D_merge/so2_UKESM_EmiMIP_base_2004_monthly.nc
```

Generate time variable:
```
cd ../base_3D_merge

for fl in `ls *.nc` ; do
  ncap2 -O -s 'time[time]=1' ${fl} ${fl}
done
```

Reset time axis to change to correct format:
```
cdo -L settunits,days -settaxis,2000-01-01,00:00,1month mmrbc_UKESM_EmiMIP_base_2000_monthly.nc ../base_3D_timefix/mmrbc_UKESM_EmiMIP_base_2000_monthly.nc

cdo -L settunits,days -settaxis,2001-01-01,00:00,1month mmrbc_UKESM_EmiMIP_base_2001_monthly.nc ../base_3D_timefix/mmrbc_UKESM_EmiMIP_base_2001_monthly.nc

cdo -L settunits,days -settaxis,2002-01-01,00:00,1month mmrbc_UKESM_EmiMIP_base_2002_monthly.nc ../base_3D_timefix/mmrbc_UKESM_EmiMIP_base_2002_monthly.nc

cdo -L settunits,days -settaxis,2003-01-01,00:00,1month mmrbc_UKESM_EmiMIP_base_2003_monthly.nc ../base_3D_timefix/mmrbc_UKESM_EmiMIP_base_2003_monthly.nc

cdo -L settunits,days -settaxis,2004-01-01,00:00,1month mmrbc_UKESM_EmiMIP_base_2004_monthly.nc ../base_3D_timefix/mmrbc_UKESM_EmiMIP_base_2004_monthly.nc

cdo -L settunits,days -settaxis,2000-01-01,00:00,1month mmrso4_UKESM_EmiMIP_base_2000_monthly.nc ../base_3D_timefix/mmrso4_UKESM_EmiMIP_base_2000_monthly.nc

cdo -L settunits,days -settaxis,2001-01-01,00:00,1month mmrso4_UKESM_EmiMIP_base_2001_monthly.nc ../base_3D_timefix/mmrso4_UKESM_EmiMIP_base_2001_monthly.nc

cdo -L settunits,days -settaxis,2002-01-01,00:00,1month mmrso4_UKESM_EmiMIP_base_2002_monthly.nc ../base_3D_timefix/mmrso4_UKESM_EmiMIP_base_2002_monthly.nc

cdo -L settunits,days -settaxis,2003-01-01,00:00,1month mmrso4_UKESM_EmiMIP_base_2003_monthly.nc ../base_3D_timefix/mmrso4_UKESM_EmiMIP_base_2003_monthly.nc

cdo -L settunits,days -settaxis,2004-01-01,00:00,1month mmrso4_UKESM_EmiMIP_base_2004_monthly.nc ../base_3D_timefix/mmrso4_UKESM_EmiMIP_base_2004_monthly.nc

cdo -L settunits,days -settaxis,2000-01-01,00:00,1month so2_UKESM_EmiMIP_base_2000_monthly.nc ../base_3D_timefix/so2_UKESM_EmiMIP_base_2000_monthly.nc

cdo -L settunits,days -settaxis,2001-01-01,00:00,1month so2_UKESM_EmiMIP_base_2001_monthly.nc ../base_3D_timefix/so2_UKESM_EmiMIP_base_2001_monthly.nc

cdo -L settunits,days -settaxis,2002-01-01,00:00,1month so2_UKESM_EmiMIP_base_2002_monthly.nc ../base_3D_timefix/so2_UKESM_EmiMIP_base_2002_monthly.nc

cdo -L settunits,days -settaxis,2003-01-01,00:00,1month so2_UKESM_EmiMIP_base_2003_monthly.nc ../base_3D_timefix/so2_UKESM_EmiMIP_base_2003_monthly.nc

cdo -L settunits,days -settaxis,2004-01-01,00:00,1month so2_UKESM_EmiMIP_base_2004_monthly.nc ../base_3D_timefix/so2_UKESM_EmiMIP_base_2004_monthly.nc
```

Convert to netCDF3 to avoid dimension renaming bug:
```
cd ../base_3D_timefix

for fl in `ls *.nc` ; do
  ncks -3 ${fl} ../base_3D_dimfix/${fl}
done
```

Rename dimension names:
```
cd ../base_3D_dimfix

for fl in `ls *.nc` ; do
  ncrename -O -v longitude,lon -v latitude,lat -v level_height,alt16 -d longitude,lon -d latitude,lat -d level_height,alt16 ${fl}
done
```

Convert back to netCDF4:
```
for fl in `ls *.nc` ; do
  ncks -4 ${fl} ../base_3D_dimfix2/${fl}
done
```

Overwrite z-axis with height level in descending order starting from surface (i.e. 85, 84, 83,..., 1). This is not physically accurate but allows for consistency in ESMValTool pressure level extraction protocol.
```
cd ../base_3D_dimfix2

for fl in `ls *.nc` ; do
  cdo setzaxis,../UKESM_zaxis ${fl} ../base_3D_final/${fl}
done
```

Correct the standard name for alt16 coordinate:
```
cd ../base_3D_final

for fl in `ls *.nc` ; do
  ncatted -O -a standard_name,alt16,m,c,"altitude" ${fl}
done
```

Remove intermediate folders, combine base_final with base_3D_final, then rename to base:
```
cd ../
rm -rf base
rm -rf base_merge 
rm -rf base_mergefix 
rm -rf base_timefix 
rm -rf base_dimfix
rm -rf base_3D_time 
rm -rf base_3D_merge 
rm -rf base_3D_timefix 
rm -rf base_3D_dimfix 
rm -rf base_3D_dimfix2
cp -R /base_3D_final/* /base_final
rm -rf base_3D_final
mv base_final base 
```

### GEOS
This section includes the entire routine needed to modify any given set of GEOS model files.

Changes the names from SUexp# to the respective scenario name (each number has a respective scenario it is associated with):
```
for f in aerocom3_GEOS-i33p2_Emission-MIP-SUexp/*; do mv "$f" $(echo "$f" | sed 's/^aerocom3_GEOS-i33p2_Emission-MIP-SUexp/aerocom3_GEOS-i33p2_Emission-MIP-base_/g'); done
for f in aerocom3_GEOS-i33p2_Emission-MIP-SUexp_base*; do mv "$f" $(echo "$f" | sed 's/^aerocom3_GEOS-i33p2_Emission-MIP-SUexp_base/aerocom3_GEOS-i33p2_Emission-MIP-base_/g'); done
for f in aerocom3_GEOS-i33p2_Emission-MIP-SUexp2*; do mv "$f" $(echo "$f" | sed 's/^aerocom3_GEOS-i33p2_Emission-MIP-SUexp2/aerocom3_GEOS-i33p2_Emission-MIP-so2-no-season/g'); done
for f in aerocom3_GEOS-i33p2_Emission-MIP-SUexp3*; do mv "$f" $(echo "$f" | sed 's/^aerocom3_GEOS-i33p2_Emission-MIP-SUexp3/aerocom3_GEOS-i33p2_Emission-MIP-bc-no-season/g'); done
for f in aerocom3_GEOS-i33p2_Emission-MIP-SUexp4*; do mv "$f" $(echo "$f" | sed 's/^aerocom3_GEOS-i33p2_Emission-MIP-SUexp4/aerocom3_GEOS-i33p2_Emission-MIP-so2-at-height/g'); done
for f in aerocom3_GEOS-i33p2_Emission-MIP-SUexp5*; do mv "$f" $(echo "$f" | sed 's/^aerocom3_GEOS-i33p2_Emission-MIP-SUexp5/aerocom3_GEOS-i33p2_Emission-MIP-no-so4/g'); done
for f in aerocom3_GEOS-i33p2_Emission-MIP-SUexp6*; do mv "$f" $(echo "$f" | sed 's/^aerocom3_GEOS-i33p2_Emission-MIP-SUexp6/aerocom3_GEOS-i33p2_Emission-MIP-high-so4/g'); done
```

Create folders for each scenario and sort the files:
```
mkdir base so2-no-season bc-no-season so2-at-height no-so4 high-so4
mv aerocom3_GEOS-i33p2_Emission-MIP-base* base
mv aerocom3_GEOS-i33p2_Emission-MIP-so2-no-season* so2-no-season
mv aerocom3_GEOS-i33p2_Emission-MIP-bc-no-season* bc-no-season
mv aerocom3_GEOS-i33p2_Emission-MIP-so2-at-height* so2-at-height
mv aerocom3_GEOS-i33p2_Emission-MIP-no-so4* no-so4
mv aerocom3_GEOS-i33p2_Emission-MIP-high-so4* high-so4
```

Go into each folder separately and do the following (so if there are six folders, you would need to do the following steps six times and change the commands accordingly)

Create names file and load all filenames into it as text:
```
touch names.txt
for FILE in *; do echo "$FILE" >> names.txt; done
```

Reformat the names into CMIP6 form (`sh -v` actually runs it, the former gives a preview):\
Make sure that the scenario name, following "EmiMIP_", is consistent with the folder that you are in
```
awk -F[_] '{print "mv " $0 " " $5 "_GEOS_EmiMIP_[scenarioName]_" $6 "_" $7 "_" $8}' < names.txt
awk -F[_] '{print "mv " $0 " " $5 "_GEOS_EmiMIP_[scenarioName]_" $6 "_" $7 "_" $8}' < names.txt | sh -v
```

Convert *clt* from 3hr timesteps to monthly, then move them back to the base folder and delete "hourly":
```
mkdir hourly
mv *hourly.nc hourly
cd hourly
for FILE in *; do ncra --mro -O -d time,,,244,244 $FILE $FILE; done
rename 3hourly monthly *
mv *monthly.nc ..
cd ..
rm -r hourly
```

Move the 3D variables into their own folder:
```
mkdir 3D_var
mv mmrso4* 3D_var
mv mmrbc* 3D_var
mv so2* 3D_var
```

set the time axis for all the non 3D variables, since the original time axis form was incompatible with esmValTool:
```
for FILE in *2000_monthly.nc; do cdo settunits,days -settaxis,2000-01-01,00:00,1month $FILE $FILE; done 
for FILE in *2001_monthly.nc; do cdo settunits,days -settaxis,2001-01-01,00:00,1month $FILE $FILE; done
for FILE in *2002_monthly.nc; do cdo settunits,days -settaxis,2002-01-01,00:00,1month $FILE $FILE; done
for FILE in *2003_monthly.nc; do cdo settunits,days -settaxis,2003-01-01,00:00,1month $FILE $FILE; done
for FILE in *2004_monthly.nc; do cdo settunits,days -settaxis,2004-01-01,00:00,1month $FILE $FILE; done
for FILE in *2005_monthly.nc; do cdo settunits,days -settaxis,2005-01-01,00:00,1month $FILE $FILE; done
```

navigate to the 3D_var folder and edit the 3D variables by defining and adding "standard_name", "long_name", "formula", and "formula_terms" variables. This also makes the time and z axis variables consistent with EsmValTool. The commands must be executed in the order specified below or else some variables will be deleted and you will need to start over:
```

cd 3D_var
mkdir Final

for file in mmrso4*; do ncap2 -O -s "lev=0" $file $file; done
for file in mmrso4*; do ncap2 -O -s 'lev[lev]=lev' $file $file; done
for file in mmrso4*; do ncatted -O -a standard_name,lev,c,c,"atmosphere_hybrid_sigma_pressure_coordinate" $file $file; done
for file in mmrso4*; do ncatted -O -a long_name,lev,c,c,"hybrid sigma pressure coordinate" $file $file; done
for file in mmrso4*; do ncatted -O -a formula,lev,c,c,"p(n,k,j,i) = hyam(k)*p0 + hybm(k)*ps(n,j,i)" $file $file; done
for file in mmrso4*; do ncatted -O -a formula_terms,lev,c,c,"a: hyam b: hybm ps: ps p0: p0" $file $file; done

cdo settunits,days -settaxis,2000-01-01,00:00,1month -setzaxis,../../GEOS_zaxis mmrso4_GEOS_EmiMIP_[scenarioName]_Modellevel_2000_monthly.nc Final/mmrso4_GEOS_EmiMIP_[scenarioName]_Modellevel_2000_monthly.nc
cdo settunits,days -settaxis,2001-01-01,00:00,1month -setzaxis,../../GEOS_zaxis mmrso4_GEOS_EmiMIP_[scenarioName]_Modellevel_2001_monthly.nc Final/mmrso4_GEOS_EmiMIP_[scenarioName]_Modellevel_2001_monthly.nc
cdo settunits,days -settaxis,2002-01-01,00:00,1month -setzaxis,../../GEOS_zaxis mmrso4_GEOS_EmiMIP_[scenarioName]_Modellevel_2002_monthly.nc Final/mmrso4_GEOS_EmiMIP_[scenarioName]_Modellevel_2002_monthly.nc
cdo settunits,days -settaxis,2003-01-01,00:00,1month -setzaxis,../../GEOS_zaxis mmrso4_GEOS_EmiMIP_[scenarioName]_Modellevel_2003_monthly.nc Final/mmrso4_GEOS_EmiMIP_[scenarioName]_Modellevel_2003_monthly.nc
cdo settunits,days -settaxis,2004-01-01,00:00,1month -setzaxis,../../GEOS_zaxis mmrso4_GEOS_EmiMIP_[scenarioName]_Modellevel_2004_monthly.nc Final/mmrso4_GEOS_EmiMIP_[scenarioName]_Modellevel_2004_monthly.nc
cdo settunits,days -settaxis,2005-01-01,00:00,1month -setzaxis,../../GEOS_zaxis mmrso4_GEOS_EmiMIP_[scenarioName]_Modellevel_2005_monthly.nc Final/mmrso4_GEOS_EmiMIP_[scenarioName]_Modellevel_2005_monthly.nc

for file in mmrbc*; do ncap2 -O -s "lev=0" $file $file; done
for file in mmrbc*; do ncap2 -O -s 'lev[lev]=lev' $file $file; done
for file in mmrbc*; do ncatted -O -a standard_name,lev,c,c,"atmosphere_hybrid_sigma_pressure_coordinate" $file $file; done
for file in mmrbc*; do ncatted -O -a long_name,lev,c,c,"hybrid sigma pressure coordinate" $file $file; done
for file in mmrbc*; do ncatted -O -a formula,lev,c,c,"p(n,k,j,i) = hyam(k)*p0 + hybm(k)*ps(n,j,i)" $file $file; done
for file in mmrbc*; do ncatted -O -a formula_terms,lev,c,c,"a: hyam b: hybm ps: ps p0: p0" $file $file; done

cdo settunits,days -settaxis,2000-01-01,00:00,1month -setzaxis,../../GEOS_zaxis mmrbc_GEOS_EmiMIP_[scenarioName]_Modellevel_2000_monthly.nc Final/mmrbc_GEOS_EmiMIP_[scenarioName]_Modellevel_2000_monthly.nc
cdo settunits,days -settaxis,2001-01-01,00:00,1month -setzaxis,../../GEOS_zaxis mmrbc_GEOS_EmiMIP_[scenarioName]_Modellevel_2001_monthly.nc Final/mmrbc_GEOS_EmiMIP_[scenarioName]_Modellevel_2001_monthly.nc
cdo settunits,days -settaxis,2002-01-01,00:00,1month -setzaxis,../../GEOS_zaxis mmrbc_GEOS_EmiMIP_[scenarioName]_Modellevel_2002_monthly.nc Final/mmrbc_GEOS_EmiMIP_[scenarioName]_Modellevel_2002_monthly.nc
cdo settunits,days -settaxis,2003-01-01,00:00,1month -setzaxis,../../GEOS_zaxis mmrbc_GEOS_EmiMIP_[scenarioName]_Modellevel_2003_monthly.nc Final/mmrbc_GEOS_EmiMIP_[scenarioName]_Modellevel_2003_monthly.nc
cdo settunits,days -settaxis,2004-01-01,00:00,1month -setzaxis,../../GEOS_zaxis mmrbc_GEOS_EmiMIP_[scenarioName]_Modellevel_2004_monthly.nc Final/mmrbc_GEOS_EmiMIP_[scenarioName]_Modellevel_2004_monthly.nc
cdo settunits,days -settaxis,2005-01-01,00:00,1month -setzaxis,../../GEOS_zaxis mmrbc_GEOS_EmiMIP_[scenarioName]_Modellevel_2005_monthly.nc Final/mmrbc_GEOS_EmiMIP_[scenarioName]_Modellevel_2005_monthly.nc

for file in so2*; do ncap2 -O -s "lev=0" $file $file; done
for file in so2*; do ncap2 -O -s 'lev[lev]=lev' $file $file; done
for file in so2*; do ncatted -O -a standard_name,lev,c,c,"atmosphere_hybrid_sigma_pressure_coordinate" $file $file; done
for file in so2*; do ncatted -O -a long_name,lev,c,c,"hybrid sigma pressure coordinate" $file $file; done
for file in so2*; do ncatted -O -a formula,lev,c,c,"p(n,k,j,i) = hyam(k)*p0 + hybm(k)*ps(n,j,i)" $file $file; done
for file in so2*; do ncatted -O -a formula_terms,lev,c,c,"a: hyam b: hybm ps: ps p0: p0" $file $file; done

cdo settunits,days -settaxis,2000-01-01,00:00,1month -setzaxis,../GEOS_zaxis so2_GEOS_EmiMIP_[scenarioName]_Modellevel_2000_monthly.nc Final/so2_GEOS_EmiMIP_[scenarioName]_Modellevel_2000_monthly.nc
cdo settunits,days -settaxis,2001-01-01,00:00,1month -setzaxis,../GEOS_zaxis so2_GEOS_EmiMIP_[scenarioName]_Modellevel_2001_monthly.nc Final/so2_GEOS_EmiMIP_[scenarioName]_Modellevel_2001_monthly.nc
cdo settunits,days -settaxis,2002-01-01,00:00,1month -setzaxis,../GEOS_zaxis so2_GEOS_EmiMIP_[scenarioName]_Modellevel_2002_monthly.nc Final/so2_GEOS_EmiMIP_[scenarioName]_Modellevel_2002_monthly.nc
cdo settunits,days -settaxis,2003-01-01,00:00,1month -setzaxis,../GEOS_zaxis so2_GEOS_EmiMIP_[scenarioName]_Modellevel_2003_monthly.nc Final/so2_GEOS_EmiMIP_[scenarioName]_Modellevel_2003_monthly.nc
cdo settunits,days -settaxis,2004-01-01,00:00,1month -setzaxis,../GEOS_zaxis so2_GEOS_EmiMIP_[scenarioName]_Modellevel_2004_monthly.nc Final/so2_GEOS_EmiMIP_[scenarioName]_Modellevel_2004_monthly.nc
cdo settunits,days -settaxis,2005-01-01,00:00,1month -setzaxis,../GEOS_zaxis so2_GEOS_EmiMIP_[scenarioName]_Modellevel_2005_monthly.nc Final/so2_GEOS_EmiMIP_[scenarioName]_Modellevel_2005_monthly.nc
```

Remove unnecessary directories
```
cd Final
mv *monthly.nc ../..
rm -r 3D_var
```

Fix `od550aer` (repeat for each experiment):
```
for fl in `ls od550aer*.nc`; do ncks -A ../wavelength.nc ${fl}; done
for fl in `ls od550aer*.nc`; do ncatted -O -a coordinates,od550aer,c,c,"wavelength" ${fl}; done
```
