from osgeo import ogr
import json
from json import dumps


def kml2geojson(kml_file):
    json_file = ''
    drv = ogr.GetDriverByName('KML')  ## This determines the format of the created file
    kml_ds = drv.Open(kml_file)
    for kml_lyr in kml_ds:
        for feat in kml_lyr:
           json_file += feat.ExportToJson()

    name = kml_file[:-4]+".geojson"
    output_dict = json.loads(json_file.replace("'", "\""))
    #if there is, delete the height value from geojson file
    try:
     for element in output_dict['geometry']['coordinates'][0]:
      del element[2]
    except:
      pass
    geojson = open(name, "w")
    geojson.write(dumps({"type": "FeatureCollection","crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },\
"features": [output_dict]}, indent=2) + "\n")
    geojson.close()
    return name

if __name__ == "__main__":
    kml_input = raw_input("KML path: ")
    json_output = kml2geojson(kml_input)


