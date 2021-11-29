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

## Linux commands
For copying files recursively from one directory to another:
