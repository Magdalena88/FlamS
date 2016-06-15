import shapefile
import simplejson as json
from json import dumps
# read the shapefile
shp = raw_input("Percoso e nome shapefile: ")
reader = shapefile.Reader(shp)
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
   atr = dict(zip(field_names, sr.record))
   geom = sr.shape.__geo_interface__
   buffer.append(dict(type="Feature", \
   geometry=geom, properties=atr))

# write the GeoJSON file
name = shp[:-3]+"json"
geojson = open(name, "w")
geojson.write(dumps({"type": "FeatureCollection",\
"features": buffer}, indent=2) + "\n")
geojson.close()