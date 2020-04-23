#!/bin/bash
# Move files from Windows 10 filesystem to Linux subsystem
#
# Matt Nicholson
# 22 April 2020

ORIGIN="/mnt/c/Users/nich980/data/emip/model-output"
DEST="/home/nich980/emip/model-output/AerChemMIP/NASA-GISS/GISS-E2-1-G/piClim-SO2"

for ARCHIVE in r1i1p5f101 r1i1p5f102 r1i1p5f103 r1i1p5f104
do
  cp -rv "$ORIGIN/$ARCHIVE/." "$DEST/$ARCHIVE/AERmon/"
done
