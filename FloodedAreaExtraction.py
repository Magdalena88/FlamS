from osgeo import gdal,osr,ogr
import numpy as np
import os,sys
import scipy.ndimage.filters
from scipy.cluster.vq import kmeans2
import random
import gc
import time
import pdb
from subprocess import call


def Multilooking(newRaster,inputRaster,resize_factor):

    src = gdal.Open(inputRaster, gdal.GA_ReadOnly)
    src_proj = src.GetProjection()
    src_geotrans = src.GetGeoTransform()

    originX = src_geotrans[0]
    originY = src_geotrans[3]
    pixelWidth=(src_geotrans[1])*resize_factor
    pixelHeight=(src_geotrans[5])*resize_factor

    wide = (src.RasterXSize)/resize_factor
    high = (src.RasterYSize)/resize_factor

    # Output / destination

    dst = gdal.GetDriverByName('GTiff').Create(newRaster, wide, high, 1, gdal.GDT_Byte)
    dst.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    dst.SetProjection(src.GetProjection())

    # Do the work
    gdal.ReprojectImage(src, dst, None, None, gdal.GRA_Bilinear)
    return newRaster

def readGeotiff(newRaster):
    ds = gdal.Open(newRaster, gdal.GA_ReadOnly)
    array = ds.GetRasterBand(1).ReadAsArray()

    return array


def array2raster(newRaster,inputRaster,array):

    cols = array.shape[1]
    rows = array.shape[0]
    ds = gdal.Open(inputRaster, gdal.GA_ReadOnly)
    rasterOrigin=ds.GetGeoTransform()
    originX = rasterOrigin[0]
    originY = rasterOrigin[3]
    pixelWidth=rasterOrigin[1]
    pixelHeight=rasterOrigin[5]

    outRaster = gdal.GetDriverByName('GTiff').Create(newRaster, cols, rows, 1, gdal.GDT_Byte)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(4326)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()

def filtering(arr):
   a = (1.0/16)*np.array([[1,2,1],[2,4,2],[1,2,1]])
   filtro1 = scipy.ndimage.filters.convolve(arr,a)
   b = (1.0/9)*np.array([[1,1,1],[1,8,1],[1,1,1]])
   filtro2 = scipy.ndimage.filters.convolve(filtro1,b)
   return filtro2

def k_mean(filtro2, num_classi, num_iter):
   M=filtro2.flatten()
   Mfloat=M.astype(np.float)

# using as centroid initial uniform distribution:
   seeds=np.linspace(0, 255, num_classi).tolist()
   list_seeds=[]
   for e in seeds:
       e=int(e)
       list_seeds.append(e)

   k=np.asanyarray(list_seeds)
   num_classi_int=int(num_classi)

   Mclassi=kmeans2(Mfloat, k, iter=num_iter, minit='matrix', missing='warn')
   Mlable=Mclassi[1]
   Mseeds=Mclassi[0]
   print Mseeds
   return np.reshape(Mlable, filtro2.shape)

def flood_class(arr, str_classi):
    lista=str_classi.split(",")
    array=np.zeros(arr.shape, dtype=np.uint8)
    for e in lista:
      a=int(e)
      array[arr==a]=1
##    return array
    window = np.array([[1,1,1],[1,1,1],[1,1,1]])
    sieve = scipy.ndimage.filters.convolve(array,window)
    array2=np.zeros(arr.shape, dtype=np.uint8)
    a=sieve.max()
    print a
    array2[sieve==a]=1
    return array2


def raster2polygon(inRaster, outPoly):
    src_ds = gdal.Open(inRaster)
    srcband = src_ds.GetRasterBand(1)
    drv = ogr.GetDriverByName("ESRI Shapefile")
    dst_ds = drv.CreateDataSource( outPoly + ".shp" )
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)

# create the layer
    dst_layer = dst_ds.CreateLayer(outPoly, srs)
    gdal.Polygonize(srcband, srcband, dst_layer, -1, [], callback=None )

def flood(inRaster, factor, cl, it):
    print type(inRaster)
##    inRaster=str(raw_input("Paste the raster file path and name: "))
##    factor=int(raw_input("Insert resampling factor: "))
##    cl=int(raw_input("Insert number of classes: "))
##    it=int(raw_input("Insert number of iterations: "))
# outpurt raster and vector names:
    outRaster_mm=inRaster[:-4]+"_MM%d.tif" %factor
##    outRaster_filt=outRaster_mm[:-4]+"_filtr.tif"
    outRaster_class=outRaster_mm[:-4]+"_class%d.tif" %cl
    outRaster_flood=outRaster_class[:-4]+"_flood.tif"
    outShp_flood=outRaster_class[:-4]+"_flood"

# raster to array trasformation:
    img_mm=Multilooking(outRaster_mm, inRaster,factor)
    arr = readGeotiff(outRaster_mm)
##    img_filt=filtering(arr) -> if I want to apply a filter, ther I should  replace on the next step "arr" with "img_filt"
# Classification:
    img_class=k_mean(arr,cl,it)

# array to raster trasformation:
##    array2raster(outRaster_filt,outRaster_mm, arr)
    array2raster(outRaster_class, outRaster_mm, img_class)
# choose the classes which correspond to flooded areas:
    str_classi=raw_input("lista classi flood separati da virgola: ")
    flood=flood_class(img_class,str_classi)
    flood_raster=array2raster(outRaster_flood, outRaster_mm, flood)
# raseter to vector trasformation:
    flood_poly=raster2polygon(outRaster_flood,outShp_flood)


if __name__ == '__main__':

    # file paths:

    inRaster=str(raw_input("Paste the raster file path and name: "))
    factor=int(raw_input("Insert resampling factor: "))
    cl=int(raw_input("Insert number of classes: "))
    it=int(raw_input("Insert number of iterations: "))
    flood(inRaster, factor, cl, it)


