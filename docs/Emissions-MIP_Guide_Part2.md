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
