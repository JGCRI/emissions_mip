#!/bin/bash
#
# This script copies files from the main emips repo directory
# on NERSC Cori to the operational emips esmvaltool directory.
#
# Only newer versions of the "origin", or source, files will be copied 

# ============================ Variable Definitions ============================
DIR_BASE_REPO=~/"emip"
DIR_BASE_EVT=~/"emip-evt"

EXT_YML="*.yml"
EXT_SH="*.sh"

# =========================== Copy config .yml files  ==========================
# Origin: ~/emip/config/nersc
# Dest: ~/emip-evt/config
echo "Copying new config files..."

dir_origin="$DIR_BASE_REPO/config/nersc/$EXT_YML"
dir_dest="$DIR_BASE_EVT/config/"

cp -uv $dir_origin $dir_dest

# ====================== Copy .sh files from emip/scripts ======================
# Origin: /mnt/c/Users/nich980/code/emip/scripts
# Dest: ~/esmvaltool/scripts
echo "Copying new bash scripts..."

dir_origin="$DIR_BASE_REPO/scripts/nersc/run/$EXT_SH"
dir_dest="$DIR_BASE_EVT/scripts/run/"

cp -uv $dir_origin $dir_dest
