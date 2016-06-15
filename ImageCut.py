from osgeo import gdal
import numpy as np
import osr
# Read the input raster into a Numpy array
infile = "C:\Users\ithaca\Documents\Magda\Tool_MIE\SENTINEL-1_TOOL\Immagini_grandi\s1a-iw-grd-vv-20151223t035219-20151223t035248-009164-00d308-001.tif"
data   = gdal.Open(infile)
arr    = data.ReadAsArray()

# Do some processing....

# Save out to a GeoTiff

# First of all, gather some information from the original file
[cols,rows] = arr.shape
trans       = data.GetGeoTransform()
wgs84_wkt = """
GEOGCS["WGS 84",
    DATUM["WGS_1984",
        SPHEROID["WGS 84",6378137,298.257223563,
            AUTHORITY["EPSG","7030"]],
        AUTHORITY["EPSG","6326"]],
    PRIMEM["Greenwich",0,
        AUTHORITY["EPSG","8901"]],
    UNIT["degree",0.01745329251994328,
        AUTHORITY["EPSG","9122"]],
    AUTHORITY["EPSG","4326"]]"""
new_cs = osr.SpatialReference()
new_cs.ImportFromWkt(wgs84_wkt)
proj        = data.GetProjection()
outfile     = "C:\Users\ithaca\Documents\Magda\Tool_MIE\SENTINEL-1_TOOL\Immagini_grandi\s1a.tif"

# Create the file, using the information from the original file
outdriver = gdal.GetDriverByName("GTiff")
outdata   = outdriver.Create(str(outfile), rows, cols, 1, gdal.GDT_Float32)

# Write the array to the file, which is the original array in this example
outdata.GetRasterBand(1).WriteArray(arr)

# Georeference the image
outdata.SetGeoTransform(new_cs )
##
### Write projection information
##outdata.SetProjection(proj)