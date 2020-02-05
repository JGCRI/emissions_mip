# ESMValTool
[ESMValTool](https://github.com/ESMValGroup/ESMValTool) is a software package that provides diagnostic and performance metrics tools for evaluating Earth system models in CMIP. However, the current version of ESMValTool only supports Unix(-like) operating systems. If you aren't provided easy access to an Unix-based system, but have Windows 10, there is still hope. 

# Installing on NERSC Cori
PNNL's CESM run outputs are located on the National Energy Research Scientific Computing Center's (NERSC) [Cori supercomputer](https://www.nersc.gov/systems/cori/). Since the directory holding the output for all four EMIP experiments is ~90 GB and Cori has much more computing power than your local machine, it's best to set up ESMValTool on Cori and run it from there.

## 1. Configure Conda
The most straight-forward installation method for ESMValTool is through [Conda](https://esmvaltool.readthedocs.io/en/latest/getting_started/install.html#conda-installation). Both Python and Conda are already [installed on Cori](https://docs.nersc.gov/programming/high-level-environments/python/#anaconda-python).

Below is a quick walkthrough of how to create a Conda environment on Cori:

* Load the Python module
  ```
  module load python
  ```
  The default Python module is `python/3.7-anaconda-2019.10`, so loading the Python module loads Conda as well.
  
* Create a new Conda environment (see [Conda docs](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands) for more details)
  ```
  conda create -n emip python=3.6
  ```
  
* Activating your new `emip` Conda environment
  ```
  source activate emip
  ```
  
  **Note**: Normally, Conda environments are activated by the `conda activate <env>` command. However, due to extra security on Cori, Conda environments can only be activated through the `source activate <env>` command. See the [Cori Python docs](https://docs.nersc.gov/programming/high-level-environments/python/#conda-environments) for details
  
* Deactivating your `emip` Conda environment
  ```
  conda deactivate
  ```
  
  **Note**: Unlike above, once a Conda environment is activated, it *can* be deactivated via the normal `conda deactivate` command. This command is preferred over `source deactivate`. See the [Cori Python docs](https://docs.nersc.gov/programming/high-level-environments/python/#conda-environments) for details

## 2. Install Julia
ESMValTool uses [Julia](https://julialang.org), which is not currently installed as a module on Cori, so we'll have to install it ourselves.

1. To download the Julia installation package, navigate to the [Julia downloads page](https://julialang.org/downloads/). Cori runs SUSE Linux Enterprise Server 15, but the `Generic Linux Binaries for x86` installation package will work just fine. Right-click the link and select `copy link address` from the dropdown menu.
![julia download](imgs/julia-dl.png)

2. On Cori, navigate to the directory where you wish to install the Julia package (I chose `mnichol3/misc`). Download the Julia installation package from the Linux command prompt using `wget`:
   ```
   wget <copied-julia-url>
   ```
   
3. Unzip the downloaded Julia package with the following command:
   ```
   tar -xvzf julia_installation_package.tar.gz
   ```
   
4. Add Julia to your `PATH` variable. The most straight-forward way to do this is by adding Julia's `bin` directory path to your system `PATH` environment variable via your `~/.bash_profile` or `~/.bashrc` file. 
  Open your `~/.bash_profile` or `~/.bashrc` file in your editor-of-choice and enter the following:
    ```
    export PATH=“$PATH:/path/to/bin”
    ```
    For example, I placed my Julia package into `/global/.../mnichol3/misc`, so I added the following line to my `~/.bash_profile` file:
    ```
    export PATH=“$PATH:/global/.../mnichol3/misc/julia-1.3.1/bin”
    ```
    For other ways to add Julia to your PATH variable, see [their docs](https://julialang.org/downloads/platform/).
    
5. Restart bash. This can be accomplished with the command `exec bash`. If `which julia` fails, restart your SSH session.


## 3. Install ESMValTool - Conda
Once you have Conda and Julia installed on your Linux subsystem, you can install ESMValTool via the [Conda installation method](https://esmvaltool.readthedocs.io/en/latest/getting_started/install.html#conda-installation).

From your Linux command prompt, run the following command to install ESMValTool:
```
conda install -c esmvalgroup -c conda-forge esmvaltool
```



# Installing ESMValTool on Windows 10
Since ESMValTool only supports Unix-based systems, you'll have to install and activate the Windows 10 Linux Subsystem on your machine, then use that to install ESMValTool.

## 1. Install the Windows 10 Linux Subsystem
See these articles for how to install and activate the Windows 10 Linux Subsystem:
* [Windows Subsystem for Linux Installation Guide for Windows 10](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
* [How to install Windows 10’s Linux Subsystem on your PC](https://www.onmsft.com/how-to/how-to-install-windows-10s-linux-subsystem-on-your-pc)

## 2. Install Anaconda 
Once you have your Windows 10 Linux subsystem up and running, you'll need to install [Anaconda](https://www.anaconda.com/distribution/) on to it

1. Navigate to the [Anaconda download page](https://www.anaconda.com/distribution/) page and select `Linux`. Right-click the appropriate download link for your system's hardware, and select `Copy link address` from the dropdown menu (see image below; I'm running 64-bit Windows so I selected `64-Bit x86 Installer`).
![conda download](imgs/cond-dl.png)

2. Open a Linux command prompt and enter the following:
   ```
   wget <copied-conda-url>
   ```

   This will download the conda installation `.sh` script into your current working directory on your Linux subsystem. 

3. Run the Conda installation script:
   ```
   ./Anaconda3-2019.10-Linux-x86_64.sh
   ```
   An in-depth guide for installing Conda on Linux can be found [here](https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart).
   
## 3. Install Julia
See the [Install Julia](#install-julia) section above.


## 4. Install ESMValTool - Conda
See [Install ESMValTool - Conda](#3-install-esmvaltool---conda) above.



# Troubleshooting

## ESMValCore Distribution Error
Checking the ESMValTool installation (from your activated Conda env) with `esmvaltool -h` yields the following error:
```
pkg_resources.DistributionNotFound: The 'ESMValCore==2.0.0b1' distribution was not found and is required by the application
```

### Possible Causes
1. The `ESMValCore` package is not installed in your current Conda environment
2. The version of the `ESMValCore` package installed in your current environment is not compatible with your environment's version of `ESMValTool`. For example, you could have `ESMValCore v2.0.0b1` installed while the `ESMValTool` package wants `ESMValCore v2.0.0b5`. Yes, that miniscule version difference can make it break (speaking from experience).

### Solutions
1. Check that the `ESMValCore` package is installed with `conda list`. If the package is installed in your active Conda environment, the following row should appear in the list of packages:
    ```
    esmvalcore                2.0.0b5                    py_0    esmvalgroup
    ```
    If the `ESMValCore` package is not present in your environment, install it via:
    ```
    conda install -c esmvalgroup -c conda-forge esmvalcore
    ```
 2. Create a new Conda environment for `ESMValTool`. Clone the [GitHub repo](https://github.com/ESMValGroup/ESMValTool) and create a new Conda environment from the included `environment.yml` file. 
     
     From the root `ESMValTool` directory:
     ```
     conda env create --name <env_name> --file environment.yml
     ```
     Once your new environment is created, activate it and re-install `ESMValTool` via the [Conda method](#3-install-esmvaltool---conda)
