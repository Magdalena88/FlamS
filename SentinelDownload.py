from sentinelsat.sentinel import SentinelAPI
from sentinelsat.sentinel import get_coordinates

##from sentinelsat.sentinel import get_footprints
import KMLtoGeoJason
import pycurl
import certifi
import shapefile
import simplejson as json
from json import dumps
import os
import zipfile
from geojsonio import display

def downloadSentinel(user, pw, aoi, start, stop):
    # For image before November 16th, 2015
    curl = pycurl.Curl()
    curl.setopt(pycurl.CAINFO, certifi.where())
    curl.setopt(pycurl.URL, 'https://scihub.copernicus.eu/dhus')
    curl.perform()
    # For image before November 16th, 2015
    api = SentinelAPI(user, pw, 'https://scihub.copernicus.eu/dhus')
    AOI = KMLtoGeoJason.kml2geojson(aoi)
    api.query(get_coordinates(AOI), start, stop, producttype='GRD')
# footprint generation of all found images:
    a=api.get_footprints()
    name = AOI[:-8]+"_S1footprint.geojson"
    foot = open(name, "w")
    foot.write(dumps(a, indent=2) + "\n")
    foot.close()
##
##    with open(name) as f:
##      contents = f.read()
##      display(contents)
# selected image download and unzip:
    imageId = raw_input("Insert Sentinel-1 image id: ")
    output_img = 'C:\Users\ithaca\Documents\Magda\Tool_MIE\SENTINEL-1_TOOL\Immagini_grandi'
    s1 = api.download(imageId, output_img)
    path = os.path.dirname(s1)
    with zipfile.ZipFile(s1, "r") as z:
        z.extractall(path)

if __name__ == "__main__":
    AOI_kml = str(raw_input("Insert aoi.kml: "))
    downloadSentinel("magdalena88", "magicaroma88", AOI_kml, "20151201", "20160412")

