#!/bin/bash
#
# This script copies files from the main emips repo directory
# on the Win10 filesystem to the operational emips esmvaltool directory
# on the Win10 Linux Subsystem file system.
#
# Only newer versions of the "origin", or source, files will be copied
# 
# Win10 Linux Susbsytem info
# ---------------------------
# Distro: Ubuntu
# Release: 18.04
# Description: 18.04.3 LTS Bionic Beaver
# ID: Ubuntu
# ID_Like: Debian

# ============================ Variable Definitions ============================
DIR_BASE_WIN="/mnt/c/Users/nich980/code/emip"
DIR_BASE_LINUX="~/esmvaltool"

EXT_YML="*.yml"
EXT_SH="*.sh"

# =========================== Copy config .yml files  ==========================
# Origin: /mnt/c/Users/nich980/code/emip/config/local
# Dest: ~/esmvaltool/config
echo "Copying new config files..."

dir_origin="$DIR_BASE_WIN/config/local/$EXT_YML"
dir_dest="$DIR_BASE_LINUX/config"

cp -uv $dir_origin $dir_dest

# ====================== Copy .sh files from emip/scripts ======================
# Origin: /mnt/c/Users/nich980/code/emip/scripts
# Dest: ~/esmvaltool/scripts
echo "Copying new bash scripts..."

dir_origin="$DIR_BASE_WIN/scripts/run/$EXT_SH"
dir_dest="$DIR_BASE_LINUX/scripts/run"

cp -uv $dir_origin $dir_dest
