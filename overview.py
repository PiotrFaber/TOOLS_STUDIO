# Copyright (C) 2023 Łebi

import os
import shutil
import fnmatch
from osgeo_utils import gdal_edit
from tifftools import tiff_split

basedir = os.path.dirname(__file__)
gdal_translate = os.path.join(basedir, "osgeo", "gdal_translate.exe")
gdaladdo = os.path.join(basedir, "osgeo", "gdaladdo.exe")


def process(path_input, path_output, resampling, ov, tile, compress, file):
    if ov != "" and tile == "" and compress == "":
        if path_output == "":
            os.system(gdaladdo + ' --config BIGTIFF_OVERVIEW IF_NEEDED' + resampling + ' "'
                      + os.path.join(path_input, file) + '" ' + ov)
        else:
            shutil.copy(os.path.join(path_input, file), path_output)
            os.system(gdaladdo + ' --config BIGTIFF_OVERVIEW IF_NEEDED' + resampling + ' "'
                      + os.path.join(path_output, file) + '" ' + ov)
            copy_tfw(path_input, path_output, file)
    elif ov == "" and tile != "" and compress == "":
        if path_output == "":
            os.system(gdal_translate + ' -of "GTiff" -co "BIGTIFF=IF_NEEDED"' + tile + ' "'
                      + os.path.join(path_input, file) + '" "' + os.path.join(path_input, "TempT.tif") + '"')
            shutil.move(os.path.join(path_input, "TempT.tif"), os.path.join(path_input, file))
        else:
            os.system(gdal_translate + ' -of "GTiff" ' + tile + ' "' + os.path.join(path_input, file) + '" "'
                      + os.path.join(path_output, file) + '"')
            copy_tfw(path_input, path_output, file)
    elif ov == "" and tile == "" and compress != "":
        os.system(gdal_translate + ' -of "GTiff" -co "BIGTIFF=IF_NEEDED"' + compress + ' "'
                  + os.path.join(path_input, file) + '" "' + os.path.join(path_output, file) + '"')
        copy_tfw(path_input, path_output, file)
    elif ov != "" and tile != "" and compress == "":
        if path_output == "":
            os.system(gdal_translate + ' -of "GTiff" -co "BIGTIFF=IF_NEEDED"' + tile + ' "'
                      + os.path.join(path_input, file) + '" "' + os.path.join(path_input, "TempT.tif") + '"')
            os.system(gdaladdo + ' --config BIGTIFF_OVERVIEW IF_NEEDED' + resampling + ' "'
                      + os.path.join(path_input, "TempT.tif") + '" ' + ov)
            shutil.move(os.path.join(path_input, "TempT.tif"), os.path.join(path_input, file))
        else:
            os.system(gdal_translate + ' -of "GTiff" -co "BIGTIFF=IF_NEEDED"' + tile + ' "'
                      + os.path.join(path_input, file) + '" "' + os.path.join(path_output, file) + '"')
            os.system(gdaladdo + ' --config BIGTIFF_OVERVIEW IF_NEEDED' + resampling + ' "'
                      + os.path.join(path_output, file) + '" ' + ov)
            copy_tfw(path_input, path_output, file)
    elif ov != "" and tile == "" and compress != "":
        os.system(gdal_translate + ' -of "GTiff" -co "BIGTIFF=IF_NEEDED"' + compress + ' "'
                  + os.path.join(path_input, file) + '" "' + os.path.join(path_output, file) + '"')
        os.system(gdaladdo + ' --config BIGTIFF_OVERVIEW IF_NEEDED' + resampling + ' "'
                  + os.path.join(path_output, file) + '" ' + ov)
        copy_tfw(path_input, path_output, file)
    elif ov == "" and tile != "" and compress != "":
        os.system(gdal_translate + ' -of "GTiff" -co "BIGTIFF=IF_NEEDED"' + compress + tile + ' "'
                  + os.path.join(path_input, file) + '" "' + os.path.join(path_output, file) + '"')
        copy_tfw(path_input, path_output, file)
    elif ov != "" and tile != "" and compress != "":
        os.system(gdal_translate + ' -of "GTiff" -co "BIGTIFF=IF_NEEDED"' + compress + tile + ' "'
                  + os.path.join(path_input, file) + '" "' + os.path.join(path_output, file) + '"')
        os.system(gdaladdo + ' --config BIGTIFF_OVERVIEW IF_NEEDED' + resampling + ' "'
                  + os.path.join(path_output, file) + '" ' + ov)
        copy_tfw(path_input, path_output, file)


def copy_tfw(path_input, path_output, file):
    tfw_file = file[:-4] + ".tfw"
    for file in os.listdir(path_input):
        if fnmatch.fnmatch(file, tfw_file):
            shutil.copy(os.path.join(path_input, file), path_output)


def clean(path_input, clean_ov, clean_tile, clean_geometry, file):
    if clean_tile:
        os.system(gdal_translate + ' -of "GTiff" -co "BIGTIFF=IF_NEEDED" -co "TILED=NO" "'
                  + os.path.join(path_input, file) + '" "' + os.path.join(path_input, "TempT.tif") + '"')
        shutil.move(os.path.join(path_input, "TempT.tif"), os.path.join(path_input, file))
    else:
        if clean_ov:
            tiff_split(os.path.join(path_input, file), os.path.join(path_input, file))
            shutil.move(os.path.join(path_input, file + "aaa.tif"), os.path.join(path_input, file))
            for item in os.listdir(path_input):
                if fnmatch.fnmatch(item, file + "???.tif"):
                    os.remove(os.path.join(path_input, item))
    if clean_geometry:
        argv = "-unsetmd", "-a_srs", "", "-unsetgt", os.path.join(path_input, file)
        gdal_edit.gdal_edit(argv)
