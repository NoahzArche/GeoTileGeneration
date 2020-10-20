#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 19:37:31 2020
@author: noahzr
"""

# Syntax:
# Gda.GeoTransform( xmin, xpixelsize, x skew (=0), ymax, yskew (=0), -ypixelsize )
# Transform in .mod file of wedge data ( x-axis min, y-axis min, map scale x, 0, 0, map scale y )
# spatial_values = ( height, width, x-axis min, y-axis min, map scale x, map scale y )


import numpy as np
from osgeo import osr, gdal

# change filename 
filename = "/Users/noahzr/Downloads/NLB_539621449RASLF0603162NCAM00260M1.ht"

spatial_values = np.load(filename + "_transform.npy")
dtm_array = np.load(filename + ".npy")
geotiff_filename = filename + ".tif"

# replacing previous nodata values with 0
dtm_array[dtm_array == np.amax(dtm_array)] = 0

fileformat = "GTiff"

driver = gdal.GetDriverByName(fileformat)

metadata = driver.GetMetadata()
# checking if format support Create()
if metadata.get(gdal.DCAP_CREATE) == "YES":
    print("Driver {} supports Create() method.".format(fileformat))

if metadata.get(gdal.DCAP_CREATE) == "No":
    print("Driver {} does not support the Create() method. Cannot proceed".format(fileformat))


# xsize, ysize: size of output geotiff file
dst_ds = driver.Create(geotiff_filename, xsize=1000, ysize=1000,
                    bands=1, eType=gdal.GDT_Float64)


dst_ds.SetGeoTransform([float(spatial_values[2]), float(spatial_values[4]), 0, float(spatial_values[3]) + (float(spatial_values[0])-1) * float(spatial_values[5]), 0, -float(spatial_values[5])])
srs = osr.SpatialReference()

dst_ds.GetRasterBand(1).WriteArray(dtm_array)

dst_ds.GetRasterBand(1).SetNoDataValue(0)

# closing the generated dataset
dst_ds = None




