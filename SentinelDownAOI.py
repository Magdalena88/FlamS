import KMLtoGeoJason
import SentinelDownload
import os
import urllib
import FloodedAreaExtraction
# Insert AOI.kml:
##usr = raw_input("Username: ")
##pss = raw_input("Password: ")
##AOI = raw_input("Insert AOI.kml path: ")
##start = raw_input("Sensing period from (ex. 20151231):")
##stop = raw_input("to (ex. 20151231): ")

usr = "magdalena88"
pss = "magicaroma88"
AOI = "C:\Users\ithaca\Documents\Magda\Tool_MIE\SENTINEL-1_TOOL\AOI\AOI.kml"
start = "20151201"
stop = "20151231"

##s1 = SentinelDownload.downloadSentinel(usr, pss, AOI, start, stop)
##os.system("start \"\" http://geojson.io")
##image_path = os.path.realpath(s1)
##image = os.path.join(image_path, 'measurement',os.listdir(image_path)[0])

image_path = os.path.join("C:\Users\ithaca\Documents\Magda\Tool_MIE\SENTINEL-1_TOOL\Immagini_grandi\S1A_IW_GRDH_1SSV_20151223T035219_20151223T035248_009164_00D308_101C.SAFE", "measurement")
image_file = os.listdir(image_path)
image = os.path.join(image_path, image_file[1])
print image
##inRaster=str(raw_input("Paste the raster file path and name: "))
factor=int(raw_input("Insert resampling factor: "))
cl=int(raw_input("Insert number of classes: "))
it=int(raw_input("Insert number of iterations: "))
FloodedAreaExtraction.flood(image, factor, cl, it)


