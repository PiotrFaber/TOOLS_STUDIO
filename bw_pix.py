# Copyright (C) 2023 Łebi

import os
import shutil
import fnmatch
from osgeo_utils import gdal_calc


def process(path_input, path_output, file):
    gdal_calc.Calc(A=os.path.join(path_input, file), allBands="A", overwrite=True, format="GTiff",
                   creation_options=["BIGTIFF=IF_NEEDED"], quiet=True, outfile=os.path.join(path_output, file),
                   calc="(A!=255)*(A!=0)*A + (A==0)*1 + (A==255)*254")
    tfw_file = file[:-4] + ".tfw"
    for file in os.listdir(path_input):
        if fnmatch.fnmatch(file, tfw_file):
            shutil.copy(os.path.join(path_input, file), path_output)
